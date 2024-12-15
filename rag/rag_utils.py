from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_community.chat_message_histories import ChatMessageHistory
from .prompts import *
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

from .models import ChatbotResponse
import os
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from langchain_openai import OpenAIEmbeddings


store = {}


def get_llm():
    try:
        llm = ChatOpenAI(
            temperature=0.5,
            model_name='gpt-4o-mini',
            openai_api_key=os.getenv('OPENAI_API_KEY'),
        )
    except Exception as e:
        raise RuntimeError(f"Error initializing LLM: {e}")
    return llm


def get_session_history(custom_id: str):
    global store
    print(f"[DEBUG] store 상태 확인 전: {store}")  # 현재 store 상태 출력
    print(f"[DEBUG] {custom_id}에 대해 새로운 ChatMessageHistory 생성")  # 새로운 세션 생성 확인
    if custom_id not in store:
        store[custom_id] = ChatMessageHistory()
    else:
        print(f"[DEBUG] {custom_id}에 대한 기존 세션 로드")  # 기존 세션 로드 확인
    print(f"[DEBUG] store 상태 확인 후: {store}")  # store 상태 다시 출력
    return store[custom_id]


def get_conversational_rag_chain(custom_id):
    """
    사용자 데이터를 기반으로 RAG 체인을 생성
    """
    # 사용자 데이터 로드
    print("시작")
    try:
        # 가장 최신의 ChatbotResponse 가져오기 (생성 시간 기준)
        chatbot_response = ChatbotResponse.objects.filter(custom_id=custom_id).latest('created_at')
        user_data = chatbot_response.responses
    except ObjectDoesNotExist:
        return None
    print(f"user_data: {user_data}")
    # Vectorstore 로드
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.load_local(
            folder_path='faiss_index',
            embeddings=embeddings,
            index_name='index',
            allow_dangerous_deserialization=True
        )
        print(f"vectorstore: {vectorstore}")
    except Exception as e:
        print(f"Failed to load vectorstore: {e}")
    print(f"vectorstore: {vectorstore}")

    # Condense Retriever 생성
    llm = get_llm()
    print(f"llm: {llm}")
    condense_question_prompt = create_condense_question_prompt()
    print(f"condense_question_prompt: {condense_question_prompt}")
    try:
        condense_retriever = create_history_aware_retriever(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            prompt=condense_question_prompt,
        )
    except Exception as e:
        print(f"Failed to act create_history_aware_retriever: {e}")

    # QA Chain 생성
    qa_prompt = create_qa_prompt()
    qa_prompt = qa_prompt.partial(user_data=str(user_data))
    print(f"qa_prompt: {qa_prompt}")
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    # RAG Chain 생성
    rag_chain = create_retrieval_chain(condense_retriever, qa_chain)

    # Conversational RAG Chain 생성
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain
