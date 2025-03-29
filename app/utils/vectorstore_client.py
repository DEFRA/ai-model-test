from threading import Lock

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings


class VectorStoreClient:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.vector_store = InMemoryVectorStore(OpenAIEmbeddings())
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )

    def load_documents(self, urls):
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]
        print(f"docs_list {docs_list}")
        doc_splits = self.text_splitter.split_documents(docs_list)
        self.vector_store.add_documents(doc_splits)
        print(f"Loaded {len(doc_splits)} document splits.")

    def similarity_search(self, query, k=1):
        return self.vector_store.similarity_search(query=query, k=k)

    def clear_vector_store(self):
        self.vector_store = InMemoryVectorStore(OpenAIEmbeddings())
        print("Vector store cleared.")

    def as_retriever(self):
        return self.vector_store.as_retriever()

