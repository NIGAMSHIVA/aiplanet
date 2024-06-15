import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import google.generativeai as genai
from pydantic import BaseModel

import os
from dotenv import load_dotenv

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Print the API key to verify (optional)
print(f"Your API key is: {api_key}")

# Replace the google_api_key here

genai.configure(api_key=api_key)

## function to load Gemini Pro model and get repsonses
geminiModel = genai.GenerativeModel("gemini-pro")
chat = geminiModel.start_chat(history=[])


def get_gemini_response(query):
    # Sends the conversation history with the added message and returns the model's response.
    instantResponse = chat.send_message(query, stream=True)
    return instantResponse


# SQLAlchemy models
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()


# CRUD operations
# Create (Create)



@app.post("/question/")
async def answer_question(query: str):
    output = get_gemini_response(query)
    print(output)
    # for outputChunk in output:
    #     st.write(outputChunk.text)
    #     st.session_state['chat_history'].append(("Bot", outputChunk.text))
    result = ""
    for outputChunk in output:
        result = result + outputChunk.text
    return {"result": result}

class Story(BaseModel):
    title:str
    description:str


@app.post("/set_agent_context")
async def set_agent_context(story: Story):
    query="please answer next questions based on this text ----->"+story.description
    output=get_gemini_response(query)
    result = ""
    for outputChunk in output:
        result = result + outputChunk.text
    return {"result": result}




# @app.post("/items/")
# async def create_item(item: Item = Body(...)):
#   # Access data from the request body
#   print(f"Received item: {item.name}, {item.description}")
#   return {"message": "Item created successfully"}





if __name__ == "__main__":
    uvicorn.run(app)



