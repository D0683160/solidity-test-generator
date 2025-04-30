from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

def retrieve_context(query: str, persist_directory: str = "./chroma_db") -> str:
    # 建立 embedding 模型
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 載入 ChromaDB
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    # 查詢最相關的3個文件
    docs = vectordb.similarity_search(query, k=3)

    if not docs:
        return ""

    # 把所有查到的結果拼起來
    context = "\n\n".join(doc.page_content for doc in docs)
    return context

