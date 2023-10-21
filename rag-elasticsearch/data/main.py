from langchain.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.elasticsearch import ElasticsearchStore


# Metadata extraction function
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["name"] = record.get("name")
    metadata["summary"] = record.get("summary")
    metadata["url"] = record.get("url")
    metadata["category"] = record.get("category")
    metadata["updated_at"] = record.get("updated_at")

    return metadata


## Load Data
loader = JSONLoader(
    file_path="./data/documents.json",
    jq_schema=".[]",
    content_key="content",
    metadata_func=metadata_func,
)
# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=250)
all_splits = text_splitter.split_documents(loader.load())

# Add to vectorDB
vectorstore = ElasticsearchStore.from_documents(
    documents=all_splits,
    embedding=HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
    ),
    es_url="http://localhost:9200",
    index_name="workplace-search-example",
)
