from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph

from app.utils.langchain_bedrock_client import chat_bedrock
from app.utils.vectorstore_client import VectorStoreClient


class State(dict):
    question: str
    context: dict[Document]
    answer: str

def retrieve(state: State):
    client = VectorStoreClient()
    retriever = client.as_retriever()
    retrieved_docs = retriever.invoke(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    prompt = hub.pull("rlm/rag-prompt")
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = chat_bedrock(messages)
    return {"answer": response.content}

def run_rag_llm(query: str):
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    return graph.invoke({"question": query})

