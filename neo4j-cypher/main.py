from neo4j_cypher.chain import cypher_chain, response_chain


def generate_answer(input):
    cypher_chain.invoke({"question": input})
    return response_chain.invoke({"question": input})


if __name__ == "__main__":
    original_query = "Who played in Top Gun?"
    print(generate_answer(original_query))
