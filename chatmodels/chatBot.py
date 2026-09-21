import os

from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9, max_tokens=300)

message = []
print("------------Welcome to the Chatbot Type 0 exit the apllication ------------")
while True:

    prompt = input("You : ")
    message.append(prompt)
    if prompt == "0":
        break;

    response = model.invoke(message)
    message.append(response.content)
    print("Bot :", response.content)

print(message)
