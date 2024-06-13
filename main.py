import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import google.generativeai as genai

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
@app.post("/items/")
async def create_item(name: str, description: str):
    db = SessionLocal()
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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


# Read (GET)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    return item


# Update (PUT)
@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, description: str):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_item.name = name
    db_item.description = description
    db.commit()
    return db_item


# Delete (DELETE)
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app)


# if submitButton and inputText:
#     # calls the get_gemini_response function by passing the inputText as query and gets the response as output
#     output=get_gemini_response(inputText)
#     # Add user query and response to session state chat history
#     st.session_state['chat_history'].append(("You", inputText))
#     st.subheader("The Response is")
#     #Display the output in the app as Bot response
#     for outputChunk in output:
#         st.write(outputChunk.text)
#         st.session_state['chat_history'].append(("Bot", outputChunk.text))

# st.subheader("The Chat History is")
#  # Piece of code to show the chat history in the app
# for role, text in st.session_state['chat_history']:
#     st.write(f"{role}: {text}")

#     print(api_key)
