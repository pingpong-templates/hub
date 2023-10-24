from neo4j_cypher_ft.chain import chain

if __name__ == "__main__":
    original_query = "Who played in top gun?"
    print(chain.invoke({"question": original_query}))
