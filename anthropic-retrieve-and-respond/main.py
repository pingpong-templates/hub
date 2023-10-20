from anthropic_retrieve_and_respond.chain import chain 


if __name__ == "__main__":
	query = "Which movie came out first: Oppenheimer, or Are You There God It's Me Margaret?"
	print(chain.invoke({"query": query}))
