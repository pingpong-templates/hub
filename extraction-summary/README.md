# Extraction

This template performs an extraction task on the input text per the Pydantic schema provided.

Under the hood, it will use OpenAI function calling to produce output that adheres to the schema.

##  LLM

Be sure that `OPENAI_API_KEY` is set in order to the OpenAI model(s) for embedding and answer synthesis.

## Installation

TO DO: Add clarification on how to spin this up.

```
from langserve.client import RemoteRunnable
from langchain.schema.messages import HumanMessage

# Model 
extraction_model = RemoteRunnable('localhost:8000/extraction-summary')

# Load a paper to use
path = "docs/"
loader = UnstructuredPDFLoader(path+"LLaVA.pdf")
doc = loader.load()[0]
messages = [HumanMessage(content=doc[0].page_content)]
extraction_model.invoke(messages)
```