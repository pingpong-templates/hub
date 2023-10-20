from langchain import hub
from langchain.chat_models import ChatAnthropic
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.schema.output_parser import StrOutputParser

# Load a paper to use
path = "docs/"
loader = UnstructuredPDFLoader(path+"LLaVA.pdf")
doc = loader.load()[0]

# Create chain
prompt = hub.pull("hwchase17/anthropic-paper-qa")
model = ChatAnthropic(model="claude-2", max_tokens=10000)
chain = prompt | model | StrOutputParser()

# # Invoke
# chain.invoke({"text": doc.page_content})