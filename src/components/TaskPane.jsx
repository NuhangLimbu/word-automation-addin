import React, { useEffect, useState } from "react";

const API_URL = "https://word-automation-addin.onrender.com/rules";

const TaskPane = () => {
  const [rules, setRules] = useState([]);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => setRules(data))
      .catch((err) => console.error("Error fetching rules:", err));
  }, []);

  const applyRule = async (findText, replaceText) => {
    await Word.run(async (context) => {
      const body = context.document.body;
      const results = body.search(findText);
      results.load("items");
      await context.sync();

      results.items.forEach((item) => {
        item.insertText(replaceText, "Replace");
      });
      await context.sync();
    });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Word Automator</h1>
      {rules.length === 0 ? <p>No rules found.</p> : (
        rules.map((rule) => (
          <button 
            key={rule.id} 
            onClick={() => applyRule(rule.find_text, rule.replace_text)}
            style={{ display: "block", margin: "10px 0", width: "100%" }}
          >
            Fix: {rule.find_text} → {rule.replace_text}
          </button>
        ))
      )}
    </div>
  );
};

export default TaskPane;