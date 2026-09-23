import os

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.9, max_tokens=300)

print("Choose your AI mode")
print("press 1 for angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice = int(input("Enter your response :-"))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggresively and imptiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are a Sad AI agent. You respond with sadness and empathy."
messages = [
    SystemMessage(content  = mode)
]
print("------------Welcome to the Chatbot Type 0 exit the apllication ------------")
while True:

    prompt = input("You : ")
    messages.append(HumanMessage(content = prompt))
    if prompt == "0":
        break;

    response = model.invoke(messages)
    messages.append(AIMessage(content = response.content))
    print("Bot :", response.content)

print(messages)
