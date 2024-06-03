'use client';

import CodeEditor from './components/code_editor';

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen items-center justify-start p-20">
      <h1 className="text-4xl font-bold mb-8">Code Execution Website</h1>
        <CodeEditor />
      
    </main>
  );
}