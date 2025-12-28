/* global Office */
import React, { useEffect, useState } from "react";
// Go UP one level out of components, then INTO services
import { summarizeSelection, autoCorrectGrammar, autoFillTemplate } from "../services/wordActions";

export default function TaskPane() {
  const [isReady, setIsReady] = useState(false);
  const [status, setStatus] = useState("Initializing...");

  useEffect(() => {
    Office.onReady((info) => {
      if (info.host === Office.HostType.Word) {
        setIsReady(true);
        setStatus("Connected to Word");
      }
    });
  }, []);

  const handleAction = async (fn) => {
    setStatus("Working...");
    try {
      await fn();
      setStatus("Success!");
    } catch (err) {
      setStatus("Error: " + err.message);
    }
  };

  if (!isReady) return <div className="p-5">Connecting to Office...</div>;

  return (
    <div className="p-5 font-sans">
      <h2 className="text-xl font-bold mb-4 text-blue-800">Word Automator</h2>
      <p className="text-sm mb-4 text-gray-500">Status: {status}</p>

      <div className="flex flex-col gap-2">
        <button 
          onClick={() => handleAction(summarizeSelection)} 
          className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 font-bold"
        >
          ✨ AI Summarize
        </button>

        <button 
          onClick={() => handleAction(autoCorrectGrammar)} 
          className="bg-green-600 text-white p-2 rounded hover:bg-green-700 font-bold"
        >
          🪄 AI Grammar Fix
        </button>

        <button 
          onClick={() => handleAction(autoFillTemplate)} 
          className="bg-gray-600 text-white p-2 rounded hover:bg-gray-700 font-bold"
        >
          📝 Fill {{name}}
        </button>
      </div>
    </div>
  );
}