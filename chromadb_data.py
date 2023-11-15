from chromadb.config import Settings
import chromadb


class MyVectorDB:
    def __init__(self, collection_name, embedding_fn):
        chroma_client = chromadb.PersistentClient(path="data")

        # 创建一个 collection
        self.collection = chroma_client.get_or_create_collection(name=collection_name)
        self.embedding_fn = embedding_fn

    def add_documents(self, documents, metadata):
        '''向 collection 中添加文档与向量'''
        self.collection.add(
            embeddings=self.embedding_fn(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[f"id{i}" for i in range(len(documents))],  # 每个文档的 id
            metadatas=[metadata] * len(documents)
        )

    def search(self, query, top_n):
        '''检索向量数据库'''
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n
        )
        return results

if __name__ == "__main__":
    from pdf_to_paragraph import Paragraph
    from gpt_server import get_embeddings

    # paragraph = Paragraph()
    # chunks = paragraph.split_text("/Users/huangxinzhe/code/llm_note/zhihu_study_note/05_rag_embeddings/data/llama2.pdf",
    #                               page_numbers=[2, 3],
    #                               min_line_length=10,
    #                               chunk_size=300,
    #                               overlap_size=100)
    
    # 创建一个向量数据库对象
    vector_db = MyVectorDB("demo_text_split", get_embeddings)
    # 向向量数据库中添加文档
    # vector_db.add_documents(chunks, {"source": "llama2.pdf"})

    # 检索
    search_results = vector_db.search("llama 2有多少参数？", 2)
    print(search_results)
