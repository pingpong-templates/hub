from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant who translates {input_language} to {output_language}",
        ),
        ("human", "{text}"),
    ]
)
model = ChatOpenAI()

chain = prompt | model
