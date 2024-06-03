/* eslint-disable react/no-unescaped-entities */

import React, { useEffect, useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { testCode, submitCode } from '../api/db';

const CodeEditor: React.FC = () => {
  // State variables to manage code, flags for code modification, success status, and output/errors.
  const [code, setCode] = useState<string>('');
  const [isCodeModified, setIsCodeModified] = useState<boolean>(false);
  const [success, setSuccess] = useState<boolean>(false);
  const [output, setOutput] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isTesting, setIsTesting] = useState<boolean>(false);
  const [traceback, setTraceback] = useState<string>('');

  // Effect to mark code as modified when it changes.
  useEffect(() => {
    setIsCodeModified(true);
  }, [code]);

  // Handler for code changes in the CodeMirror editor.
  const handleCodeChange = (value: string) => {
    setCode(value);
    setIsCodeModified(true);
  };

  // Function to handle code testing
  const handleTestCode = async () => {
    setOutput('');
    setError('');
    setSuccess(false);
    setIsTesting(true);
    setTraceback('');
    try {
      // Call the testCode API and handle the result.
      const result = await testCode(code);
      console.log(result);
      setOutput(result.stdout);
      setError(result.error || '');
      setTraceback(result.traceback || '');
    } catch (err) {
      console.log(err);
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsTesting(false);
    }
  };

  // Function to handle code submission
  const handleSubmitCode = async () => {
    setOutput('');
    setError('');
    setSuccess(false);
    setIsSubmitting(true);
    setTraceback('');
    try {
      // Call the submitCode API and handle the result.
      const result = await submitCode(code);
      if (result.message) {
        setSuccess(true);
      }
      setOutput(result.stdout);
      setError(result.error || '');
      setTraceback(result.traceback || '');
    } catch (err) {
      if (err instanceof Error) {
        console.log(err);
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-4xl bg-white p-6 rounded-lg shadow-lg flex flex-col items-center mt-8">
      <h2 className="text-2xl font-bold mb-4 self-start">Code Editor</h2>
      <p className="text-gray-600 mb-4 self-start">Write Python code using pandas and scipy</p>
      
      <h4 className='font-bold self-start'>Example Input:</h4>
      <pre className='self-start mb-3'>print("Hello World")</pre>
      <CodeMirror
        className="w-full border border-gray-400 rounded-lg p-2"
        value={code}
        onChange={(value) => handleCodeChange(value)}
      />
      <div className="mt-4 flex justify-end w-full">
        <button
          className={`font-bold py-2 px-4 mr-3 rounded ${
            isCodeModified && !isSubmitting && !isTesting
              ? 'bg-blue-500 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          onClick={handleTestCode}
          disabled={!isCodeModified || isSubmitting || isTesting}
        >
          {isTesting ? 'Testing...' : 'Test Code'}
        </button>
        <button
          className={`font-bold py-2 px-4 rounded ${
            isCodeModified && !isSubmitting && !isTesting
              ? 'bg-blue-500 text-white hover:bg-blue-700'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          onClick={handleSubmitCode}
          disabled={!isCodeModified || isSubmitting || isTesting}
        >
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>
      </div>
      {success && (
        <div className="mt-4 p-4 w-full bg-green-100 text-green-700 rounded-lg">
          <h4 className="font-bold">Success:</h4>
          <p>Your code was successfully submitted!</p>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 w-full bg-red-100 text-red-700 rounded-lg">
          <h4 className="font-bold">Error:</h4>
          <pre>{error}</pre>
        </div>
      )}
      {traceback && (
        <div className="mt-4 p-4 w-full bg-red-100 text-red-700 rounded-lg ">
          <h4 className="font-bold">Traceback:</h4>
          <pre>{traceback}</pre>
        </div>
      )}
      {output && (
        <div className="mt-4 p-4 w-full bg-gray-100 rounded-lg">
          <h4 className="font-bold">Output:</h4>
          <pre>{output}</pre>
        </div>
      )}
    </div>
  );
};

export default CodeEditor;
