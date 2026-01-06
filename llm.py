from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import OpenAIEmbeddings 
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate, FewShotChatMessagePromptTemplate

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import answer_examples

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def get_retriever():
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')
    index_name = 'tax-markdown-index'
    database = PineconeVectorStore.from_existing_index(index_name=index_name, embedding=embedding)
    retriever = database.as_retriever(search_kwargs={'k': 4})
    return retriever


def get_history_retriever():
    llm = get_llm()
    retriever = get_retriever() 

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever


def get_llm(model="gpt-4o"):
    llm = ChatOpenAI(model=model)
    return llm


def get_dictionary_chain():
    dictionary = {
        "주택": ["집", "아파트", "전세", "전세집", "빌라", "오피스텔", "원룸"],
        "임대인": ["집주인", "건물주"],
        "임차인": ["세입자", "전세입자", "월세입자"],
        "보증금 반환": ["보증금 돌려받기", "전세금 반환"],
    }

    dictionary_text = "\n".join(
        [f"- {', '.join(v)} → {k}" for k, v in dictionary.items()]
    )

    llm = get_llm()

    prompt = ChatPromptTemplate.from_template(
        """
        사용자의 질문을 보고 아래 사전을 참고하여
        법률 문서에서 사용하는 공식 용어로 질문을 정규화하세요.

        - 의미가 같은 경우에만 변경하세요.
        - 의미가 달라질 수 있으면 변경하지 마세요.
        - 질문의 의도는 절대 바꾸지 마세요.
        - 최종 결과는 수정된 질문 한 문장만 출력하세요.

        사전:
        {dictionary}

        사용자 질문:
        {question}
        """
    )

    dictionary_chain = prompt | llm | StrOutputParser()
    return dictionary_chain, dictionary_text



def get_rag_chain():
    llm = get_llm()

    # 퓨샷러닝
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{answer}"),
        ]
    )
    
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=answer_examples,
    )

    system_prompt = (
        "당신은 주택임대차보호법 전문가입니다. 사용자의 주택임대차보호법 관련 질문에 대해 답변해주세요. "
        "아래에 제공된 문서(주택임대차보호법)를 근거로만 답변해야 하며, "
        "문서에 근거가 없는 내용은 추측하지 말고 모른다고 답변해주세요. "
        "답변의 첫 문장은 반드시 '주택임대차보호법 제○조(조문명)에 따르면,'의 형식으로 시작해야 합니다. "
        "질문이 여러 법적 효과를 포함하는 경우(예: 대항력 + 임대인 지위 승계), 관련 항을 모두 명시해야 합니다. "
        "답변은 2~3문장의 간결한 설명으로 작성해주세요."
        "\n\n"
        "{context}"
    )
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = get_history_retriever()
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    ).pick('answer')

    return conversational_rag_chain


def get_ai_response(user_message):
    dictionary_chain, dictionary_text = get_dictionary_chain()
    rag_chain = get_rag_chain()
    tax_chain = {"input": dictionary_chain} | rag_chain
    ai_response = tax_chain.stream(
        {
            "question": user_message,
            "dictionary": dictionary_text,  
        }, 
        config={
            "configurable": {"session_id": "abc123"}
        }
        ,)
    
    return ai_response 
