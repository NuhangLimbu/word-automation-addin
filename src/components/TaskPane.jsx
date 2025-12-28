/* global Office */
import React, { useEffect, useState } from "react";
import { summarizeSelection, autoFillTemplate } from "../services/wordActions";

export default function TaskPane() {
  const [isReady, setIsReady] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Office.onReady((info) => {
      if (info.host === Office.HostType.Word) setIsReady(true);
    });
  }, []);

  const handleAction = async (actionFn) => {
    setLoading(true);
    try {
      await actionFn();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!isReady) return <div className="p-10 text-center font-sans">Connecting to Word...</div>;

  return (
    <div className="p-6 font-sans">
      <header className="mb-8">
        <h1 className="text-2xl font-black text-blue-700">Automator AI</h1>
        <p className="text-xs text-gray-500 uppercase tracking-widest">v1.0.4 - Production</p>
      </header>
      
      <div className="flex flex-col gap-4">
        <button 
          disabled={loading}
          onClick={() => handleAction(summarizeSelection)}
          className="w-full bg-blue-600 text-white font-bold py-4 rounded-xl shadow-lg hover:bg-blue-700 active:scale-95 transition-all disabled:opacity-50"
        >
          {loading ? "Processing..." : "✨ AI Summarize"}
        </button>

        <button 
          disabled={loading}
          onClick={() => handleAction(autoFillTemplate)}
          className="w-full bg-white text-gray-800 font-bold py-4 rounded-xl border-2 border-gray-200 hover:bg-gray-50 active:scale-95 transition-all"
        >
          📝 Fill {{name}}
        </button>
      </div>

      <footer className="mt-20 text-center border-t pt-4">
        <p className="text-[10px] text-gray-400">Deployed via Vercel & GitHub</p>
      </footer>
    </div>
  );
}