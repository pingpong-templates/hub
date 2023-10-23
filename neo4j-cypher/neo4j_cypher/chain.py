from langchain.chat_models import ChatOpenAI
from langchain.graphs import Neo4jGraph
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain.schema.runnable import RunnableLambda

# Connection to Neo4j
graph = Neo4jGraph()

# Cypher validation tool for relationship directions
corrector_schema = [
    Schema(el["start"], el["type"], el["end"])
    for el in graph.structured_schema.get("relationships")
]
cypher_validation = CypherQueryCorrector(corrector_schema)

# LLMs
cypher_llm = ChatOpenAI(model_name="gpt-4", temperature=0.0)
qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)

# Memory
memory = ConversationBufferWindowMemory(return_messages=True, k=5)

# Generate Cypher statement based on natural language input
cypher_template = """Based on the Neo4j graph schema below, write a Cypher query that would answer the user's question:
{schema}

Question: {question}
Cypher query:"""

cypher_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question, convert it to a Cypher query. No pre-amble.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", cypher_template),
    ]
)

cypher_chain = (
    RunnablePassthrough.assign(
        schema=lambda _: graph.get_schema,
        history=RunnableLambda(lambda x: memory.load_memory_variables(x)["history"]),
    )
    | cypher_prompt
    | cypher_llm.bind(stop=["\nCypherResult:"])
    | StrOutputParser()
)


# Handle Cypher query memory
def save(input_output):
    output = {"output": cypher_validation(input_output.pop("output"))}
    memory.save_context(input_output, output)
    return output["output"]


cypher_response_memory = RunnablePassthrough.assign(output=cypher_chain) | save

# Generate natural language response based on database results
response_template = """Based on the the question, Cypher query, and Cypher response, write a natural language response:
Question: {question}
Cypher query: {query}
Cypher Response: {response}"""

response_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question and Cypher response, convert it to a natural language answer. No pre-amble.",
        ),
        ("human", response_template),
    ]
)

response_chain = (
    RunnablePassthrough.assign(query=cypher_response_memory)
    | RunnablePassthrough.assign(
        response=lambda x: graph.query(x["query"]),
    )
    | response_prompt
    | qa_llm
)
