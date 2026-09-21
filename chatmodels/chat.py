from dotenv import load_dotenv
from httpx import HTTPStatusError

load_dotenv()  # Load environment variables from .env file

# from langchain.chat_models import init_chat_model
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chat_models import init_chat_model
from langchain_groq import ChatGroq

# from langchain_mistralai import ChatMistralAI

# model = init_chat_model("google_genai:gemini-3.7-flash")
# model = ChatGoogleGenerativeAI(	model="gemini-3.7-flash")
# model =   init_chat_model("groq:openai/gpt-oss-120b")
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9, max_tokens=300)

# model = ChatMistralAI(model = "labs-leanstral-1-5-1", temperature=0)


response = model.invoke("write a paragraph for job crisis ?")

print(response.content)
