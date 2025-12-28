/* global Word */

const GEMINI_KEY = "AIzaSyBEZ_zESRh-tRnBHmSxrX--rEd_pNsYtNs"; 
const MODEL_ID = "gemini-2.0-flash-lite"; 
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_ID}:generateContent?key=${GEMINI_KEY}`;

// 1. AI Summarize
export const summarizeSelection = async () => {
  return Word.run(async (context) => {
    const selection = context.document.getSelection();
    selection.load("text");
    await context.sync();

    if (!selection.text) throw new Error("Select text first.");

    const response = await fetch(GEMINI_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: `Summarize this in 3 bullets: ${selection.text}` }] }]
      })
    });

    const data = await response.json();
    const summary = data.candidates[0].content.parts[0].text;

    selection.insertText(`\n\n[AI SUMMARY]:\n${summary}\n`, "After");
    await context.sync();
  });
};

// 2. Hybrid Auto-Correction (Rules + AI)
export const autoCorrectDocument = async (adminRules = []) => {
  return Word.run(async (context) => {
    const selection = context.document.getSelection();
    selection.load("text");
    await context.sync();

    if (!selection.text) throw new Error("Select text first.");

    let textToFix = selection.text;

    // Apply Admin Rules (from Python)
    adminRules.forEach(rule => {
      const regex = new RegExp(rule.find, "gi");
      textToFix = textToFix.replace(regex, rule.replace);
    });

    // Final AI Polish
    const response = await fetch(GEMINI_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: `Fix grammar and spelling: ${textToFix}` }] }]
      })
    });

    const data = await response.json();
    const result = data.candidates[0].content.parts[0].text;

    selection.insertText(result, "Replace");
    await context.sync();
  });
};

// 3. Template Filler
export const replacePlaceholders = async (data) => {
  return Word.run(async (context) => {
    const body = context.document.body;
    for (const key in data) {
      const searchResults = body.search(`{{${key}}}`, { matchCase: false });
      searchResults.load("items");
      await context.sync();
      searchResults.items.forEach(item => item.insertText(String(data[key]), "Replace"));
    }
    await context.sync();
  });
};