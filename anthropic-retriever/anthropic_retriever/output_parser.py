from langchain.schema.agent import AgentAction, AgentFinish

def extract_between_tags(tag: str, string: str, strip: bool = True) -> str:
    ext_list = re.findall(f"<{tag}\s?>(.+?)</{tag}\s?>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    if ext_list:
        if len(ext_list) != 1:
            raise ValueError
        # Only return the first one
        return ext_list[0]

def parse_output(outputs):
    partial_completion = outputs["partial_completion"]
    steps = outputs["intermediate_steps"]
    search_query = extract_between_tags('search_query', partial_completion + '</search_query>') 
    if search_query is None:
        return AgentFinish({"output": steps}, log=partial_completion)
    else:
        return AgentAction(tool="search", tool_input=search_query, log=partial_completion)
