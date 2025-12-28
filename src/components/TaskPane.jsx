import React, { useEffect, useState } from "react";

const API_URL = "https://word-automation-addin.onrender.com/rules";

const TaskPane = () => {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setRules(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching rules:", err);
        setLoading(false);
      });
  }, []);

  const applyRule = async (pattern, replacement) => {
    try {
      await Word.run(async (context) => {
        const body = context.document.body;
        // search options can include ignore punctuation or case
        const results = body.search(pattern, { matchCase: false });
        results.load("items");
        await context.sync();

        results.items.forEach((item) => {
          item.insertText(replacement, "Replace");
          // Optional: item.font.highlightColor = "Yellow";
        });
        await context.sync();
      });
    } catch (error) {
      console.error("Word Error:", error);
    }
  };

  if (loading) return <div style={{ padding: "20px" }}>Loading rules...</div>;

  return (
    <div style={{ padding: "20px", fontFamily: "Segoe UI, sans-serif" }}>
      <h2 style={{ fontSize: "18px", color: "#2b579a" }}>Word Automator</h2>
      <p style={{ fontSize: "12px", color: "#666" }}>Select a correction below:</p>
      
      {rules.length === 0 ? (
        <p>No rules found in cloud.</p>
      ) : (
        rules.map((rule) => (
          <button 
            key={rule.id} 
            onClick={() => applyRule(rule.pattern, rule.replacement)}
            style={{ 
              display: "block", 
              margin: "8px 0", 
              width: "100%", 
              padding: "10px",
              backgroundColor: "#f3f2f1",
              border: "1px solid #8a8886",
              cursor: "pointer",
              textAlign: "left",
              fontWeight: "600"
            }}
          >
            {rule.label || `Replace "${rule.pattern}"`}
          </button>
        ))
      )}
    </div>
  );
};

export default TaskPane;