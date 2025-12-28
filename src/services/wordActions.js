/* global Word */

const API_URL = "https://python-3-cxjw.onrender.com"; 

export const summarizeSelection = async () => {
  return Word.run(async (context) => {
    const selection = context.document.getSelection();
    selection.load("text");
    await context.sync();

    if (!selection.text) {
      throw new Error("Selection is empty. Please highlight some text.");
    }

    const response = await fetch(`${API_URL}/api/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: selection.text }),
    });

    const data = await response.json();
    selection.insertText(`\n\nSummary: ${data.summary}`, "End");
    await context.sync();
  });
};

export const autoFillTemplate = async () => {
  return Word.run(async (context) => {
    const body = context.document.body;
    body.search("{{name}}").insertText("Client Name", "Replace");
    await context.sync();
  });
};