# Summarize PDFs with Anthropic

We can use Claude2, which has a long context window, to summarize PDFs.

To do this, we can use various promps from LangChain hub, such as:

* [Fun summarization prompt](https://smith.langchain.com/hub/hwchase17/anthropic-paper-qa)
* [Chain of density summarization prompt](https://smith.langchain.com/hub/lawwu/chain_of_density)

Claude2 has a large (100k token) context window, allowing us to summarize documents over 100 pages.

# Invoke

You can call this summarization template.

TO DO: Add clarification on how to spin this up.

```
summarization_chain = RemoteRunnable('localhost:8000/anthropic-summarization')

# Load a paper to use
path = "docs/"
loader = UnstructuredPDFLoader(path+"LLaVA.pdf")
doc = loader.load()[0]

summarization_chain.invoke({"text": doc.page_content})
```