import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { summarizeSelection, autoCorrectDocument, replacePlaceholders } from "../services/wordActions";

export default function TaskPane() {
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [rules, setRules] = useState([]); 
  const [jsonInput, setJsonInput] = useState('{"name": "Nuhang", "date": "Dec 2025"}');

  // Fetch rules from your Python API (Server)
  useEffect(() => {
    fetch("http://localhost:8000/rules")
      .then((res) => res.json())
      .then((data) => setRules(data))
      .catch((err) => console.error("Could not fetch rules:", err));
  }, []);

  const handleAction = async (fn, name, params = null) => {
    setLoading(true);
    setStatus(`Processing ${name}...`);
    try {
      params ? await fn(params) : await fn();
      setStatus(`✅ ${name} complete!`);
    } catch (err) {
      setStatus(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 space-y-6 bg-slate-50 min-h-screen font-sans">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-slate-800">Word AI</h2>
        {loading && <div className="animate-spin">⏳</div>}
      </div>

      {/* SECTION 1: AUTO-FILL */}
      <Card>
        <CardHeader className="p-4 pb-2">
          <CardTitle className="text-sm">Template Auto-Fill</CardTitle>
          <CardDescription className="text-xs">Fills {"{{key}}"}</CardDescription>
        </CardHeader>
        <CardContent className="p-4 pt-0 space-y-3">
          <Textarea 
            value={jsonInput} 
            onChange={(e) => setJsonInput(e.target.value)}
            className="text-[11px] font-mono h-20"
          />
          <Button 
            className="w-full bg-blue-600"
            onClick={() => handleAction(replacePlaceholders, "Fill", JSON.parse(jsonInput))}
          >Fill Placeholders</Button>
        </CardContent>
      </Card>

      {/* SECTION 2: SMART CORRECTION */}
      <Card>
        <CardHeader className="p-4 pb-2">
          <CardTitle className="text-sm">AI & Admin Rules</CardTitle>
          <CardDescription className="text-xs">Applies Dashboard rules + AI</CardDescription>
        </CardHeader>
        <CardContent className="p-4 pt-0">
          <div className="flex flex-wrap gap-1 mb-3">
            {rules.map((r, i) => (
              <Badge key={i} variant="outline" className="text-[10px] bg-white">
                {r.find}→{r.replace}
              </Badge>
            ))}
          </div>
          <Button 
            variant="outline"
            className="w-full border-green-600 text-green-700 hover:bg-green-50"
            onClick={() => handleAction(autoCorrectDocument, "Correction", rules)}
          >🧹 Run Clean Up</Button>
          
          <Button 
            variant="ghost"
            className="w-full mt-2 text-xs"
            onClick={() => handleAction(summarizeSelection, "Summary")}
          >✨ Summarize Selection</Button>
        </CardContent>
      </Card>

      {status && (
        <div className="text-[11px] p-2 bg-slate-200 rounded text-center shadow-inner">
          {status}
        </div>
      )}
    </div>
  );
}