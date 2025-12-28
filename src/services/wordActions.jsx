/* global Word */

const GEMINI_KEY = "AIzaSyBEZ_zESRh-tRnBHmSxrX--rEd_pNsYtNs"; 
const MODEL_ID = "gemini-2.0-flash-lite"; 
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_ID}:generateContent?key=${GEMINI_KEY}`;

// AI Summarize
export const summarizeSelection = async () => {
  return Word.run(async (context) => {
    const selection = context.document.getSelection();
    selection.load("text");
    await context.sync();
    if (!selection.text) throw new Error("Please select text first.");

    const res = await fetch(GEMINI_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contents: [{ parts: [{ text: `Summarize this: ${selection.text}` }] }] })
    });
    const data = await res.json();
    const result = data.candidates[0].content.parts[0].text;
    selection.insertText(`\n[AI SUMMARY]: ${result}`, "After");
    await context.sync();
  });
};

// AI Grammar
export const autoCorrectGrammar = async () => {
  return Word.run(async (context) => {
    const selection = context.document.getSelection();
    selection.load("text");
    await context.sync();
    if (!selection.text) throw new Error("Please select text first.");

    const res = await fetch(GEMINI_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contents: [{ parts: [{ text: `Fix grammar: ${selection.text}` }] }] })
    });
    const data = await res.json();
    const result = data.candidates[0].content.parts[0].text;
    selection.insertText(result, "Replace");
    await context.sync();
  });
};

// Auto-Fill Template
export const autoFillTemplate = async () => {
  return Word.run(async (context) => {
    const body = context.document.body;
    const results = body.search("{{name}}", { matchCase: false });
    results.load("items");
    await context.sync();
    results.items.forEach(item => item.insertText("John Doe", "Replace"));
    await context.sync();
  });
};