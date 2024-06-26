from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain, SequentialChain
from langchain.chains import RetrievalQA
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.retrievers import ContextualCompressionRetriever
from BCEmbedding.tools.langchain import BCERerank
from langchain_community.embeddings import HuggingFaceEmbeddings
import langchain
import warnings


warnings.filterwarnings('ignore')
langchain.debug = True

# Chinese
model_name = "./bge-large-zh-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}
bgeEmbeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

#English
embedding_model_name = './bce-embedding-base_v1/maidalun/bce-embedding-base_v1'
embedding_model_kwargs = {'device': 'cpu'}
embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True}

embed_model = HuggingFaceEmbeddings(
    model_name=embedding_model_name,
    model_kwargs=embedding_model_kwargs,
    encode_kwargs=embedding_encode_kwargs
)

reranker_args = {'model': './bce-embedding-base_v1/maidalun/bce-reranker-base_v1', 'top_n': 3, 'device': 'cpu'}
reranker = BCERerank(**reranker_args)

global_retriever = None
global_db = None
# 定义函数
def text_style_transformation(text, language,store_name):

    global global_retriever, global_db


    # 初始化ChatOpenAI
    base_url = 'http://10.244.197.144:6006/v1'
    api_key = 'sk-wovIqI54XskmjXUc76C534D913B04a3189C554C076F11067'
    llm = ChatOpenAI(temperature=0.0, base_url=base_url, api_key=api_key)

    # 构建完整的文件路径
    store_path = f"Faiss_Vector_Store/{store_name}_store"
    if language=='zh':
        global_db = FAISS.load_local(store_path, bgeEmbeddings, allow_dangerous_deserialization=True)
        global_retriever = global_db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    if language=='en':
        global_db = FAISS.load_local(store_path, embed_model, allow_dangerous_deserialization=True)
        global_retriever = global_db.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    retriever = global_retriever
    # 定义翻译提示模板
    # translate_prompt_template = """
    # Translate the following text into {language}:\n
    # {text}
    # Remember:you only need output the translated text.
    # """
    # translate_prompt = PromptTemplate(template=translate_prompt_template, input_variables=['language', 'text'])
    # translate_chain = LLMChain(llm=llm, prompt=translate_prompt, output_key='query', output_parser=StrOutputParser())

    similar_expressions_schema = ResponseSchema(name="similar_expressions",
                                                description="The similar expressions of the query")

    response_schemas = [similar_expressions_schema]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # 定义查询提示模板
    query_prompt_template = """
    Task: Find Similar Expressions For Query
    Objective: To find the similar expressions of the query based on [Reference].
    Use the following pieces of context to find at least 3 sentences or some words with similar expressions from [Reference] to [Query] at the end .
    If you don't sure the answer, just say that you don't know, don't try to make up an answer.
    [Reference]:{context}
    [Query]: {question}
    Please do not use ellipses instead of the content of the sentences.
    [Format_Instructions]: 
    The output should be a markdown code snippet formatted in the following schema, including the leading and trailing
    "\`\`\`json" and "\`\`\`":
    ```json
    {{
    "similar_expressions": ["sentence_1:string  // the first of the similar expressions of the query ",
                            "sentence_2:string  // the second of the similar expressions of the query", 
                            "sentence_3":string  // the third of the similar expressions of the query]
    }}
    ```
    """

    query_prompt = PromptTemplate(template=query_prompt_template, input_variables=['context', 'query'])
    chain_type_kwargs = {"prompt": query_prompt}

    # # 定义检索QA链



    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=retriever,
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=compression_retriever,
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
        output_key="query_result",
        verbose=True
    )


    # 定义文风转换prompt和文风链
    style_output_schema = ResponseSchema(name="style_output",
                                         description="The output of the style transformation")

    style_response_schemas = [style_output_schema]
    style_output_parser = StructuredOutputParser.from_response_schemas(style_response_schemas)

    style_prompt_template = """
    Task: Style Generation
    
    Objective: Generate style text based on [Source Text] by learning the style of [Reference Sentences]

    [Reference Sentences]: {query_result}

    [Source Text]: {query}

    [Guide]:
    1. Carefully analyze the stylistic features of the reference sentences, including vocabulary choice, sentence structure, tone, and manner of expression.
    2. Identify the elements in the source text that do not align with the style of the reference sentences.
    3. Rewrite the source text to harmonize with the vocabulary, syntax, tone, and other stylistic aspects of the reference sentences.
    4. Ensure that the core meaning and information of the source text remain unchanged, and that the transformed text is fluent and natural.
    5. Ensure that the transformed text not only matches the style but also preserves the original meaning.
    6. Feel free to be creative while maintaining the integrity of the original message.

    [Example]:
    Reference Sentences: “Sunlight filtered through the treetops, casting dappled shadows upon the winding path, creating a patchwork quilt of light and shade.”
    Source Text: “The sunlight came through the leaves and shone on the curvy path.”
    Transformed Text: “Golden rays of sunlight deftly weave through the foliage, gently caressing the meandering trail, painting an enchanting mosaic of light and dark.”
    
    [Format_Instructions]:
    The output should be a markdown code snippet formatted in the following schema, including the leading and trailing:
    "\`\`\`json" and "\`\`\`":
    ```json
    {{
    
    "style_output": "string  // The output of the style transformation "
    
    }}
    """
    style_prompt = PromptTemplate(template=style_prompt_template, input_variables=['query_result', 'query'])
    style_chain = LLMChain(llm=llm, prompt=style_prompt, output_key='style_output', output_parser=StrOutputParser())

    overall_chain = SequentialChain(
        chains=[qa, style_chain],
        input_variables=['query'],
        output_variables=['query_result', 'source_documents', 'style_output'],
        verbose=True
    )
    # 调用顺序链
    result = overall_chain({'query': text})


    # 检查输出并替换 "python" 为 "json"（如果存在的话）
    style_output_str = result['style_output']
    if '```python' in style_output_str:
        style_output_str = style_output_str.replace('```python', '```json')
    # 解析输出
    style_output_dict = style_output_parser.parse(style_output_str)
    return style_output_dict.get('style_output')


# 示例调用
# text = "今天阳光明媚,鸟儿在唱歌,微风拂面,我们可以在田野间自由地奔跑。"
text = "我想要挣脱枷锁"
store_name = "luxun"
language = 'zh'
style_output = text_style_transformation(text, language,store_name)
print(style_output)
