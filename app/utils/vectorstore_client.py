from threading import Lock

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_postgres import PGVector

from app.common.sql_engine import get_sql_engine

from app.utils.bedrock_embedding_client import embedding_bedrock

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
        self.vector_store = PGVector(
            embedding_bedrock(),
            collection_name="ai_model_test_vectors",
            connection=get_sql_engine(),
            use_jsonb=True,
        )

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
        self.vector_store.delete_collection()

    def as_retriever(self):
        return self.vector_store.as_retriever()

