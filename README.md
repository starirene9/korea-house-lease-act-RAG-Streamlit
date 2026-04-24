# Housing Lease Protection Act RAG Chatbot

주택임대차보호법 질의응답에 특화된 **RAG(Retrieval-Augmented Generation)** 챗봇입니다.  
`Streamlit + LangChain + OpenAI + Pinecone` 조합으로, 법률 문서 검색 결과를 근거로 답변을 생성합니다.

---

## 프로젝트 목적

이 프로젝트는 "모델이 아는 것"이 아니라 "검색된 법 조문"을 우선 근거로 답변하도록 설계되었습니다.

- 주택임대차보호법 관련 질문에 대한 신뢰도 높은 응답 제공
- 문서 근거 없는 추측성 답변 최소화
- 짧고 일관된 법률 답변 포맷 유지

---

## 주요 기능

- **법률 RAG 파이프라인**: 법 조문 검색 + 근거 기반 생성
- **질문 정규화(Dictionary Chain)**: 생활 용어를 법률 용어로 변환
- **히스토리 기반 질의 재작성**: 대화 문맥을 반영해 독립 질문으로 재구성
- **Few-shot 답변 제어**: 조문 중심 응답 스타일 유도
- **간결한 출력 형식**: 2~3문장 위주의 실무형 답변

---

## 기술 스택

- **UI**: Streamlit
- **LLM**: OpenAI Chat Models (`langchain-openai`)
- **Embedding**: OpenAI `text-embedding-3-large`
- **Vector DB**: Pinecone
- **Orchestration**: LangChain (retriever, retrieval chain, message history)

---

## 동작 흐름

1. 사용자가 질문 입력
2. 질문 정규화 체인에서 용어 정리
3. 히스토리 기반 질문 재작성
4. Pinecone에서 관련 문서 검색 (`top-k`)
5. 검색 문맥을 근거로 최종 답변 생성

---

## 프로젝트 구조

- `chat.py`: Streamlit 챗 UI 엔트리포인트
- `llm.py`: RAG/체인 구성, 히스토리 관리, 응답 생성
- `config.py`: Few-shot 예시 질문/답변
- `requirements.txt`: 의존성 목록
- `documents/`: 문서 원본/관련 파일

---

## 빠른 시작

### 1) 가상환경 생성 및 활성화

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) 의존성 설치

```bash
pip install -r requirements.txt
```

### 3) 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들고 아래 값을 설정하세요.

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

> 현재 코드 기준 Pinecone 인덱스 이름은 `tax-markdown-index`입니다.

### 4) 앱 실행

```bash
source .venv/bin/activate
streamlit run chat.py
```

브라우저에서 기본 URL `http://localhost:8501`로 접속합니다.

---

## 보안 안내 (필수)

- `.env`는 API 키 등 민감정보를 포함하므로 **절대 커밋 금지**
- `.gitignore`에 아래 항목이 포함되어 기본적으로 Git 추적 제외
  - `.env`
  - `.venv/`
  - `.streamlit/secrets.toml`
- 푸시 전 `git status`로 커밋 대상 파일을 항상 확인하세요

---

## 향후 개선 아이디어

- 검색 정확도 향상을 위한 메타데이터/인덱스 설계 개선
- 조문 출처 표시 포맷 및 인용 체계 강화
- 세션 히스토리 영속화(Redis/DB)
- 체인/프롬프트 회귀 테스트 자동화
