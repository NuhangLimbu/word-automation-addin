/* global Word */

/**
 * Summarizes the currently selected text in Word
 * by sending it to our secure Python backend.
 */
export const summarizeSelection = async () => {
  return Word.run(async (context) => {
    const selection = context.document.getSelection();
    selection.load("text");
    await context.sync();
    
    if (!selection.text || selection.text.trim() === "") {
      throw new Error("Please select some text in the document first!");
    }

    // 1. Send text to YOUR backend, not directly to Google
    // This protects your GEMINI_KEY
    const res = await fetch("/api/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: selection.text })
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || "AI Service failed.");
    }

    const data = await res.json();
    
    // 2. Extract the text from the response
    const result = data.candidates[0].content.parts[0].text;
    
    // 3. Insert the summary back into Word
    selection.insertText(`\n\n[AI Summary]: ${result}`, "After");
    await context.sync();
  });
};

/**
 * Replaces {{name}} placeholders with a specific name.
 */
export const autoFillTemplate = async () => {
  return Word.run(async (context) => {
    const body = context.document.body;
    const results = body.search("{{name}}", { matchCase: false });
    results.load("items");
    await context.sync();
    
    if (results.items.length === 0) {
        console.log("No {{name}} placeholders found.");
        return;
    }

    results.items.forEach(item => item.insertText("Nuhang Limbu", "Replace"));
    await context.sync();
  });
};