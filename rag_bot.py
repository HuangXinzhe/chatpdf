from sentence_transformers import CrossEncoder



class RAG_Bot:
    def __init__(self, vector_db, llm_api, n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results
    
    def build_prompt(self, prompt_template, **kwargs):
        '''将 Prompt 模板赋值'''
        prompt = prompt_template
        for k, v in kwargs.items(): 
            if isinstance(v,str):
                val = v
            elif isinstance(v, list) and all(isinstance(elem, str) for elem in v):
                val = '\n'.join(v)
            else:
                val = str(v)
            prompt = prompt.replace(f"__{k.upper()}__",val)
        return prompt

    def chat(self, user_query, prompt_template):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)
        model = CrossEncoder('/Users/huangxinzhe/code/llm_note/zhihu_study_note/05_rag_embeddings/chatpdf/models/ms-marco-MiniLM-L-6-v2',
                             max_length=512)
        scores = model.predict([(user_query, doc)
                               for doc in search_results['documents'][0]])
        # 按得分排序
        sorted_list = sorted(zip(scores,search_results['documents'][0]), key=lambda x: x[0], reverse=True)
        rerank_results = []
        for _, doc in sorted_list:
            rerank_results.append(doc)


        # 2. 构建 Prompt
        prompt = self.build_prompt(
            prompt_template, info=rerank_results, query=user_query)

        # 3. 调用 LLM
        response = self.llm_api(prompt)
        return response

if __name__ == "__main__":
    from chromadb_data import MyVectorDB
    from gpt_server import get_embeddings, get_completion

    vector_db = MyVectorDB("demo_text_split",get_embeddings)
    

    # 创建一个RAG机器人
    bot = RAG_Bot(
        vector_db,
        llm_api=get_completion
    )
    prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
__INFO__

用户问：
__QUERY__

请用中文回答用户问题。
"""

    user_query="llama 2有多少参数？"

    response = bot.chat(user_query, prompt_template=prompt_template)

    print(response)