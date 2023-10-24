# Conversational RAG 

`Context`
 
* LangServe apps gives you access to templates.
* Templates LLM pipeline (runnables or chains) end-points accessible via FastAPI.
* The environment for these templates is managed by Poetry.

`Create app`

* Install LangServe and create an app.
* This will create a new Poetry environment /
```
pip install < to add > 
langchain serve new my-app
cd my-app
```

`Add templates`

* When we add a template, we update the Poetry config file with the necessary dependencies.
* It also automatically installed these template dependencies in your Poetry environment
```
langchain serve add rag-conversation
```

`Start FastAPI server`

```
langchain start
```

See the notebook for various ways to interact with the template.
