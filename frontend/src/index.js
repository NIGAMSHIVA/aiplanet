import React, { useEffect, useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

const story = `One day, a hare was showing off how fast he could run. He laughed at the turtle for being so slow. After seeing the overconfidence, the turtle moved him to a race. The hare (rabbit) laughed at the turtle's test, and he accepted his demand.

As the race began, the rabbit ran extremely quickly and went far ahead of the turtle and got drained. He thought there was a lot of time to relax as the turtle was far away. Soon he slept, thinking he would win the race easily.

However, the turtle (tortoise) kept walking slowly until he arrived at the finish line. The rabbit sees the turtle on the opposite side of the finish line. The turtle had won the race`;

function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [rawText, setRawText] = useState(story);
  const [textChunks, setTextChunks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');

  const onDrop = (acceptedFiles) => {
    setUploadedFiles(acceptedFiles);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: '.pdf' });

  const handleProcessClick = async () => {
    setLoading(true);
    const formData = new FormData();
    uploadedFiles.forEach(file => {
      formData.append('pdf_files', file);
    });

    try {
      const response = await axios.post('http://localhost:8000/extract-text', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setRawText(response.data.text);

      const chunksResponse = await axios.post('http://localhost:8000/chunk-text', { text: response.data.text });
      setTextChunks(chunksResponse.data.chunks);

      setLoading(false);
    } catch (error) {
      console.error('Error processing PDF:', error);
      setLoading(false);
    }
  };

  const handleAskQuestion = async () => {
    try {
      const response = await axios.post('http://localhost:8000/question/', { query: question });
      setAnswer(response.data.result);
    } catch (error) {
      console.error('Error asking question:', error);
    }
  };

  const handleSetAgentContext = useCallback(async () => {
    try {
      const story = { title: 'Example Title', description: rawText }; // Use extracted text as description
      await axios.post('http://localhost:8000/set_agent_context', story);
    } catch (error) {
      console.error('Error setting agent context:', error);
    }
  }, [rawText]);

  useEffect(() => {
    // Runs only on the first render
    handleSetAgentContext();
  }, [handleSetAgentContext]); // Add handleSetAgentContext as a dependency

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
        {rawText && (
          <div>
            <h2>Extracted Text:</h2>
            <pre>{rawText}</pre>
          </div>
        )}
        {textChunks.length > 0 && (
          <div>
            <h2>Text Chunks:</h2>
            {textChunks.map((chunk, index) => (
              <pre key={index}>{chunk}</pre>
            ))}
          </div>
        )}
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
