# Function calling with OpenAI

This template enables OpenAI [function calling](https://python.langchain.com/docs/modules/chains/how_to/openai_functions).

Function calling can be used for various tasks, such as extraction or tagging. 

Specify the function you want to use in `chain.py`

By default, it will tag the input text using the following fields:

* summarize
* provide keywords
* provide language

##  LLM

This template will use `OpenAI` by default. 

Be sure that `OPENAI_API_KEY` is set in your enviorment.

## Adding the template

Create your LangServe app:
```
langchain serve new my-app
cd my-app
```

Add template:
```
langchain serve add openai-functions
```

Start server:
```
langchain start
```

You can use this template in the Playground:

http://127.0.0.1:8000/openai-functions/playground/

Also, see Jupyter notebook `openai_functions` for various other ways to connect to the template.