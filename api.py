from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from fastapi import FastAPI
import os
import uvicorn
from langserve import add_routes

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

app = FastAPI(
    title="Langchain Query helper",
    description="Query helper using langchain",
    version="1.0",
)

add_routes(
    app,
    ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True,
        verbose=True,
        max_tokens=1000,
        n=1,
    ),
    path="/openai",
)

model = ChatOpenAI()
# llm = ollama.Ollama(
#     model="llama2",
#     # model_params={
#     #     "n_gpu_layers": 0,
#     #     "n_ctx": 10000,
#     #     "f16": False,
#     #     "local_files_only": False,
#     # },
#     temperature=0.8,
# )

prompt_1 = ChatPromptTemplate.from_template(
    "Write an essay on the following context in minimum 250 words: {topic}"
)

prompt_2 = ChatPromptTemplate.from_template(
    "Write a blog post on the following context in minimum 800 words: {topic}"
)


prompt_3 = ChatPromptTemplate.from_template(
    "Here is my source text '{text}'. Please have a look at it and let mw know in which language it is and please translate it into {target_language} language but remember it must be in a friendly tone so that everyone can relate it."
)

add_routes(app, prompt_1 | model, path="/essay")
add_routes(app, prompt_2 | model, path="/blog")
add_routes(app, prompt_3 | model, path="/translate")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
