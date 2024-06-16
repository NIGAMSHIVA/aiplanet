## Chat with Multiple PDFs 📚
## Welcome to Chat with Multiple PDFs, an application designed to facilitate document interaction and querying through a web interface. This application allows you to upload multiple PDF documents, extract text from them, ask questions related to their content, and receive AI-generated responses.

### Features
1.Upload PDFs: Drag and drop PDF files directly into the application for processing.
2.Extract Text: Automatically extract text from uploaded PDFs.
3.Ask Questions: Enter questions related to the documents' content and receive instant answers using AI.
4.Interactive Interface: User-friendly interface with real-time updates for answers and document management.

### How to Use
#### Upload Documents:

1.Drag and drop your PDF files into the designated area or click to select files manually.

#### Process Documents:

1.Click on the Process button to extract text from uploaded PDFs. This action initiates text extraction and sets the context for subsequent queries.

#### Ask Questions:

1.Enter your questions about the uploaded documents into the text input field provided.
2.Click Ask Question to submit your query. The application sends your question to an AI model that analyzes the context set by the extracted text.

#### View Answers:

1.Upon receiving an answer, it is displayed immediately below the question interface.

### Technologies Used

#### Backend:

1.FastAPI for building the REST API.
2.SQLAlchemy for database management.
3.PyMuPDF for PDF text extraction.
4.Google GenerativeAI (Gemini) for generating AI responses.

#### Frontend:

1.React for building the interactive user interface.
2.Axios for making asynchronous HTTP requests.
3.react-dropzone for handling drag-and-drop file uploads.

### Getting Started
To run this application locally, follow these steps:

1.Clone the repository from [https://github.com/NIGAMSHIVA/aiplanet].

2.Install necessary dependencies:
```sh

npm install   # For frontend dependencies (React)
pip install -r requirements.txt   # For backend dependencies (Python)
```

3.Configure environment variables:

Obtain a Google API key for Google GenerativeAI and set it in your .env file.
Configure other necessary environment variables as per the .env.example

4.Start the backend server:
```sh
uvicorn backend:app --reload
```

5.Start the frontend development server:
```sh
npm start
```

6.Open your web browser and navigate to http://localhost:3000 to access the application.

### Notes
1.This application uses CORS middleware to enable cross-origin requests, allowing the frontend and backend to communicate seamlessly.
2.Ensure that all PDFs uploaded are valid and accessible for accurate text extraction.

## Application Architecture
aiplanet/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── ...
├── README.md
└── .env

## API DOCUMENTATION
### CHAT API
1.Endpoint: /api/chat
2.Method: POST

### Request:
{
  "message": "User's message"
}
### Response:
{
  "response": "AI's response"
}


