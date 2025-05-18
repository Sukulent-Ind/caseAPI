import uvicorn
from fastapi import FastAPI
from src.api import main_router


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app")