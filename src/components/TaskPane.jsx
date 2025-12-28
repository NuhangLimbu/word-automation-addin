import React, { useEffect, useState } from "react";
import { summarizeSelection, autoCorrectDocument } from "./wordActions";

const API_URL = "https://word-automation-addin.onrender.com/rules";

const TaskPane = () => {
    const [rules, setRules] = useState([]);

    // Fetch Database Rules on Load
    useEffect(() => {
        fetch(API_URL)
            .then((res) => res.json())
            .then((data) => setRules(data))
            .catch((err) => console.error("Error fetching rules:", err));
    }, []);

    // Function for individual rule buttons
    const applySingleRule = async (pattern, replacement) => {
        await Word.run(async (context) => {
            const results = context.document.body.search(pattern, { matchCase: false });
            results.load("items");
            await context.sync();
            results.items.forEach(item => item.insertText(replacement, "Replace"));
            await context.sync();
        });
    };

    return (
        <div style={{ padding: "15px", fontFamily: "'Segoe UI', Tahoma, sans-serif" }}>
            <h2 style={{ color: "#2b579a", borderBottom: "2px solid #2b579a" }}>AI Assistant</h2>
            
            <div style={{ marginBottom: "20px" }}>
                <button 
                    onClick={summarizeSelection}
                    style={aiButtonStyle("#0078d4")}
                >
                    ✨ Summarize Selected
                </button>
                
                <button 
                    onClick={() => autoCorrectDocument(rules)}
                    style={aiButtonStyle("#107c10")}
                >
                    🪄 AI Auto-Correct (Full)
                </button>
            </div>

            <h2 style={{ color: "#2b579a", borderBottom: "2px solid #2b579a" }}>Quick Fixes</h2>
            {rules.length === 0 ? <p>Syncing rules...</p> : (
                rules.map((rule) => (
                    <button 
                        key={rule.id} 
                        onClick={() => applySingleRule(rule.pattern, rule.replacement)}
                        style={ruleButtonStyle}
                    >
                        {rule.label}
                    </button>
                ))
            )}
        </div>
    );
};

// --- Simple Styles ---
const aiButtonStyle = (color) => ({
    display: "block",
    width: "100%",
    padding: "12px",
    margin: "10px 0",
    backgroundColor: color,
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontWeight: "bold"
});

const ruleButtonStyle = {
    display: "block",
    width: "100%",
    padding: "10px",
    margin: "5px 0",
    backgroundColor: "#f3f2f1",
    border: "1px solid #d2d0ce",
    textAlign: "left",
    cursor: "pointer"
};

export default TaskPane;