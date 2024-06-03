/* eslint-disable react/no-unescaped-entities */

import React, { useEffect, useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { testCode, submitCode } from '../api/db';

const CodeEditor: React.FC = () => {
  const [code, setCode] = useState<string>('');
  const [isCodeModified, setIsCodeModified] = useState<boolean>(false);
  const [output, setOutput] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isTesting, setIsTesting] = useState<boolean>(false);

  useEffect(() => {
    setIsCodeModified(true);
  }, [code]);

  const handleCodeChange = (value: string) => {
    setCode(value);
    setIsCodeModified(true);
  };

  const handleTestCode = async () => {
    setOutput('');
    setError('');
    setIsTesting(true);
    try {
      const result = await testCode(code);
      console.log(result);
      setOutput(result.stdout);
      setError(result.stderr || '');
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsTesting(false);
    }
  };

  const handleSubmitCode = async () => {
    setOutput('');
    setError('');
    setIsSubmitting(true);
    try {
      const result = await submitCode(code);
      setOutput(result.output);
      setError('');
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full max-w-md bg-white p-6 rounded-lg shadow-lg flex flex-col items-center mt-8">
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
      {output && (
        <div className="mt-4 p-4 w-full bg-gray-100 rounded-lg">
          <h4 className="font-bold">Output:</h4>
          <pre>{output}</pre>
        </div>
      )}
      {error && (
        <div className="mt-4 p-4 w-full bg-red-100 text-red-700 rounded-lg">
          <h4 className="font-bold">Error:</h4>
          <pre>{error}</pre>
        </div>
      )}
    </div>
  );
};

export default CodeEditor;
