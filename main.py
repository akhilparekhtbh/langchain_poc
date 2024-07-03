from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")

# Define the prompt template
prompt_1 = ChatPromptTemplate.from_template(
    "Here is my source text '{text}'. Please have a look at it and let me know in which language it is and please translate it into {target_language} language but remember it must be in a {tone} tone."
)

# Initialize the OpenAI LLM
openai_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True,
    verbose=True,
    max_tokens=1000,
    n=1,
)

# Streamlit app
st.title("Your Translator")
query = st.text_input("Enter your text")
target_language = st.text_input("Enter the target language")
tone = st.text_input("Enter the tone in which you want your text to be translated")

if st.button("Submit"):
    with st.spinner("Loading..."):
        # Format the prompt with the given variables
        formatted_prompt = prompt_1.format_messages(
            target_language=target_language, text=query, tone=tone
        )

        # Generate the response
        response = openai_llm(formatted_prompt)
        # Extract the text from the response
        response_text = response.content

        st.write(response_text)
        st.success("Done!")
