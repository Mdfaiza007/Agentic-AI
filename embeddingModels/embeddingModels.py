
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()  # Load environment variables from .env file

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True},
)

text = [
    "Hello My Name is Md Faizan",
    "I am a software engineer and I am working on Gen AI",
    "and nice to meet you"
]

# vector = embedding.embed_query("you are going to learn Gen Ai")
vector = embedding.embed_documents(text)

print(vector)

# from langchain_openai import OpenAIEmbeddings

# embedding = OpenAIEmbeddings(
#     model="text-embedding-3-large", 
#     dimensions=1536,
# )

# vector = embedding.embed_query("you are going to learn Gen Ai")
# print(vector)