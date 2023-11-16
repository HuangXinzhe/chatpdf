## Background
- 使用RAG针对特定文本进行问答
- 文本问答中的RAG的流程
    - 离线步骤：文档加载->切分->向量化->灌库
    - 在线步骤：问题->向量化->检索->Prompt->LLM->回复

## Usage
- 文件说明
    - gpt_server.py：提供Embedding与chat服务
    - pdf_to_paragraph.py：将PDF文档加载与切分
    - chromadb_data.py：将切分后的文档向量化并存储
    - rag_bot.py：提供问答服务（其中包含rerank）

- 文本问答
    - 运行rag_bot.py完成问答（目前仅有llama2.pdf数据）
    - 输入用例
        - user_query="llama 2有多少参数？"


## Requirement
- 项目依赖包  

    pip install -r requirements.txt


## 存在的问题
1. 每次上传一个文件都需要对上传的文本进行Embedding并存储
    - 花费大
    - 所需时间较长
    后续可以设置判断，如果文本已经存在，则不需要再次进行Embedding，可以节约Embedding的花费与时间