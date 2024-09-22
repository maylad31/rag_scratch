from fastapi import FastAPI,Response
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from data_schema import Query
from llm_utils import query_llm
from vector_utils import load_index
from process_data import process_query
from sqlite3 import Connection


connection = None
index = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection,index
    connection = Connection("demo.db",isolation_level=None,check_same_thread=False)
    index = load_index(index_name="demo")
    yield
    connection.close()
    index = None
    
    
app = FastAPI(lifespan=lifespan)

@app.post("/query")
async def answer_query(query: Query)-> Response:
    """process a query"""
    context =  process_query(query.query,connection=connection,index=index)
    response = await query_llm(query=query.query,context=context)
    return JSONResponse({"response":response,"retrieved_resumes":context},status_code=200)