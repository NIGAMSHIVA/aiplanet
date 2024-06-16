

import React, { useEffect, useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

const initialStory = ``;

function App() {
  // State to hold uploaded files
  const [uploadedFiles, setUploadedFiles] = useState([]);
  // State to handle loading state
  const [loading, setLoading] = useState(false);
  // State for the question input by the user
  const [question, setQuestion] = useState('');
  // State for the answer from the server
  const [answer, setAnswer] = useState('');

  // Function to handle file drop event
  const onDrop = (acceptedFiles) => {
    setUploadedFiles(acceptedFiles);
  };

  // useDropzone hook to handle file dropzone properties
  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: '.pdf' });

  // Function to handle process button click
  const handleProcessClick = async () => {
    setLoading(true);
    const formData = new FormData();
    uploadedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      // Post request to the server to extract text from PDFs
      const response = await axios.post('http://localhost:8000/extract-text', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      // Set agent context with extracted text
      await handleSetAgentContext(response.data.text);
      setLoading(false);
    } catch (error) {
      console.error('Error processing PDF:', error);
      setLoading(false);
    }
  };

  // Function to handle asking a question
  const handleAskQuestion = async () => {
    try {
      // Post request to the server with the user's question
      const response = await axios.post('http://localhost:8000/question/', { query: question });
      setAnswer(response.data.result);
    } catch (error) {
      console.error('Error asking question:', error);
    }
  };

  // Function to set agent context with extracted text
  const handleSetAgentContext = useCallback(async (text) => {
    try {
      const story = { title: 'Example Title', description: text }; // Use extracted text as description
      await axios.post('http://localhost:8000/set_agent_context', story);
    } catch (error) {
      console.error('Error setting agent context:', error);
    }
  }, []);

  // Use effect to set initial agent context on component mount
  useEffect(() => {
    handleSetAgentContext(initialStory);
  }, [handleSetAgentContext]);

  return (
    <div className="App">
      <header>
        <h1>Chat with Multiple PDFs 📚</h1>
        <input
          type="text"
          placeholder="Ask a question about your documents:"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleAskQuestion} disabled={loading}>
          Ask Question
        </button>
      </header>
      <aside>
        <h2>Your Documents</h2>
        <div {...getRootProps({ className: 'dropzone' })}>
          <input {...getInputProps()} />
          <p>Drag 'n' drop your PDFs here, or click to select files</p>
        </div>
        <button onClick={handleProcessClick} disabled={loading}>
          {loading ? 'Processing...' : 'Process'}
        </button>
        {uploadedFiles.length > 0 && (
          <div>
            <h3>Uploaded Files:</h3>
            <ul>
              {uploadedFiles.map((file) => (
                <li key={file.path}>{file.path}</li>
              ))}
            </ul>
          </div>
        )}
      </aside>
      <main>
        {answer && (
          <div>
            <h2>Answer:</h2>
            <p>{answer}</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

