

import os
from fastapi import FastAPI, UploadFile, File
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini AI
genai.configure(api_key=api_key)
geminiModel = genai.GenerativeModel("gemini-pro")
chat = geminiModel.start_chat(history=[])

# Middleware to handle CORS


def get_gemini_response(query):
    instantResponse = chat.send_message(query, stream=True)
    return instantResponse

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy models
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()

class Query(BaseModel):
    query: str

class Story(BaseModel):
    title: str
    description: str
    
origins = ["http://localhost:3000","localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/question/")
async def answer_question(query: Query):
    output = get_gemini_response(query.query)
    result = "".join([outputChunk.text for outputChunk in output])
    return {"result": result}

@app.post("/set_agent_context")
async def set_agent_context(story: Story):
    query = "please answer next questions based on this text ----->" + story.description
    output = get_gemini_response(query)
    result = "".join([outputChunk.text for outputChunk in output])
    return {"result": result}

@app.post("/extract-text")
async def extract_text(files: List[UploadFile] = File(...)):
    text = ""
    for file in files:
        pdf_data = await file.read()
        doc = fitz.open("pdf", pdf_data)
        for page in doc:
            text += page.get_text()

    return {"text": text}

@app.post("/chunk-text")
async def chunk_text(data: dict):
    text = data["text"]
    chunks = text.split()  # Dummy implementation
    return {"chunks": chunks}

@app.post("/knock_knock")
async def example():
    return {"hello":"hello"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# import os
# from fastapi import FastAPI, UploadFile, File
# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import google.generativeai as genai
# from pydantic import BaseModel
# from typing import List
# from fastapi.middleware.cors import CORSMiddleware
# import fitz  # PyMuPDF

# # Load environment variables from the .env file
# from dotenv import load_dotenv
# load_dotenv()

# # Get the API key from the environment variables
# api_key = os.getenv("GOOGLE_API_KEY")

# # Configure the Gemini AI with the API key
# genai.configure(api_key=api_key)
# geminiModel = genai.GenerativeModel("gemini-pro")
# chat = geminiModel.start_chat(history=[])

# # Middleware to handle CORS (Cross-Origin Resource Sharing)
# origins = ["http://localhost:3000", "localhost:3000"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Database configurations
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # SQLAlchemy models for the database
# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String, index=True)

# # Create all tables in the database
# Base.metadata.create_all(bind=engine)

# # FastAPI app instance
# app = FastAPI()

# # Pydantic models for request validation
# class Query(BaseModel):
#     query: str

# class Story(BaseModel):
#     title: str
#     description: str

# # Function to get response from Gemini AI based on the query
# def get_gemini_response(query):
#     instantResponse = chat.send_message(query, stream=True)
#     return instantResponse

# # API endpoint to handle questions and get responses from Gemini AI
# @app.post("/question/")
# async def answer_question(query: Query):
#     output = get_gemini_response(query.query)
#     result = "".join([outputChunk.text for outputChunk in output])
#     return {"result": result}

# # API endpoint to set the context for the Gemini AI agent
# @app.post("/set_agent_context")
# async def set_agent_context(story: Story):
#     query = "please answer next questions based on this text ----->" + story.description
#     output = get_gemini_response(query)
#     result = "".join([outputChunk.text for outputChunk in output])
#     return {"result": result}

# # API endpoint to extract text from uploaded PDF files
# @app.post("/extract-text")
# async def extract_text(files: List[UploadFile] = File(...)):
#     text = ""
#     for file in files:
#         pdf_data = await file.read()
#         doc = fitz.open("pdf", pdf_data)
#         for page in doc:
#             text += page.get_text()

#     return {"text": text}

# # API endpoint to chunk the extracted text (Dummy implementation)
# @app.post("/chunk-text")
# async def chunk_text(data: dict):
#     text = data["text"]
#     chunks = text.split()  # Dummy implementation
#     return {"chunks": chunks}

# # Example endpoint to test the server
# @app.post("/knock_knock")
# async def example():
#     return {"hello": "hello"}

# # Run the FastAPI application
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
