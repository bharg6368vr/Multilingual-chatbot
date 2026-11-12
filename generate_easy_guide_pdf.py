import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(r"c:\multilingual_chatbot")
HTML_PATH = PROJECT_ROOT / "EASY_PROJECT_EXPLANATION_GUIDE.html"
PDF_PATH = PROJECT_ROOT / "EASY_PROJECT_EXPLANATION_GUIDE.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Smart Multilingual AI Chatbot - Quick Presentation & Viva Guide</title>
<style>
  @page {
    size: A4 portrait;
    margin: 15mm 15mm 15mm 15mm;
  }
  
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #1f2937;
    margin: 0;
    padding: 0;
  }

  .page-break {
    page-break-after: always;
    break-after: page;
  }

  .header-card {
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    color: white;
    padding: 20px 25px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
  }
  .header-card h1 {
    margin: 0;
    font-size: 18pt;
    font-weight: 800;
    letter-spacing: 0.5px;
  }
  .header-card h2 {
    margin: 6px 0 0 0;
    font-size: 12pt;
    font-weight: 400;
    opacity: 0.9;
  }
  .header-card .badge-row {
    margin-top: 12px;
    display: flex;
    gap: 10px;
    font-size: 9pt;
  }
  .header-card .badge {
    background: rgba(255,255,255,0.2);
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 600;
  }

  .section-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-left: 5px solid #2563eb;
    border-radius: 6px;
    padding: 15px 20px;
    margin-bottom: 16px;
  }
  .section-title {
    font-size: 13pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 0;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .speech-bubble {
    background-color: #eff6ff;
    border: 1.5px solid #bfdbfe;
    border-radius: 8px;
    padding: 12px 16px;
    font-style: italic;
    color: #1e40af;
    margin: 10px 0;
    line-height: 1.6;
    font-size: 10.5pt;
  }

  .flowchart-box {
    background-color: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 8px;
    padding: 15px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    line-height: 1.35;
    color: #0f172a;
    white-space: pre;
    overflow-x: auto;
    margin: 12px 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 10pt;
  }
  th, td {
    border: 1px solid #e2e8f0;
    padding: 8px 10px;
    text-align: left;
  }
  th {
    background-color: #f1f5f9;
    font-weight: 700;
    color: #1e293b;
  }

  .component-grid {
    display: flex;
    gap: 12px;
    margin: 10px 0;
  }
  .component-col {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
  }
  .component-col h4 {
    margin: 0 0 6px 0;
    color: #1e3a8a;
    font-size: 11pt;
  }
  .component-col p {
    margin: 0;
    font-size: 9.5pt;
    color: #475569;
    line-height: 1.4;
  }

  .qa-box {
    background: #faf5ff;
    border: 1px solid #e9d5ff;
    border-left: 4px solid #9333ea;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 10px;
  }
  .qa-q {
    font-weight: 700;
    color: #6b21a8;
    margin-bottom: 4px;
    font-size: 10.5pt;
  }
  .qa-a {
    color: #3b0764;
    font-size: 10pt;
    line-height: 1.45;
  }

  .step-pill {
    display: inline-block;
    background: #dbeafe;
    color: #1d4ed8;
    font-weight: 700;
    font-size: 9pt;
    padding: 2px 8px;
    border-radius: 12px;
    margin-right: 6px;
  }

  .footer-bar {
    text-align: center;
    font-size: 8.5pt;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    padding-top: 6px;
    margin-top: 20px;
  }
</style>
</head>
<body>

<!-- PAGE 1: INTRO, FLOWCHART & 3 COMPONENTS -->
<div class="page-break">
  <div class="header-card">
    <h1>🌐 SMART MULTILINGUAL AI CHATBOT</h1>
    <h2>Presentation & Viva Cheat Sheet: The Easiest Explanation</h2>
    <div class="badge-row">
      <span class="badge">MVJ College of Engineering</span>
      <span class="badge">Dept. of CSE</span>
      <span class="badge">NLP (MVJ22CS72)</span>
      <span class="badge">Academic Year 2026 - 2027</span>
    </div>
  </div>

  <div class="section-card">
    <div class="section-title">🎤 1. The 1-Minute Spoken Pitch (Say This First!)</div>
    <div class="speech-bubble">
      "Good morning/afternoon. My project is a <strong>Smart Multilingual AI Chatbot</strong>.<br>
      Most chatbots fail because of a big trade-off: traditional rule-based bots only work in English, while pure ChatGPT or Gemini bots <strong>hallucinate fake facts</strong> and skip required fields in business forms.<br>
      To solve this, our project combines two engines:<br>
      1. <strong>Rasa Open Source:</strong> Acts as the strict manager for deterministic tasks like <strong>appointment booking</strong> with zero hallucinations.<br>
      2. <strong>LangChain + Google Gemini:</strong> Acts as the multilingual brain, detecting languages and answering company questions using our verified <strong>Knowledge Base (RAG)</strong>.<br>
      Together, it delivers <strong>100% reliable forms</strong> and <strong>fluent support across 16+ languages</strong>."
    </div>
  </div>

  <div class="section-card">
    <div class="section-title">📊 2. The Simple Flowchart (Draw or Explain This)</div>
    <div class="flowchart-box">
                  ┌───────────────────────────────────────────────┐
                  │         👤 User Input in ANY Language         │
                  │        (English, Spanish, Hindi, etc.)        │
                  └───────────────────────┬───────────────────────┘
                                          │
                                          ▼
                  ┌───────────────────────────────────────────────┐
                  │          🖥️ Streamlit Web Interface           │
                  │   Detects Language & Displays Badge (🇪🇸/🇮🇳)   │
                  └───────────────────────┬───────────────────────┘
                                          │ (REST API on Port 5005)
                                          ▼
                  ┌───────────────────────────────────────────────┐
                  │              🤖 Rasa Core & NLU               │
                  │         Classifies Intent & Entities          │
                  └───────────────────────┬───────────────────────┘
                                          │
                     Is it a Booking?     │ Is it an FAQ / Multilingual?
                     ┌────────────────────┴────────────────────┐
                     ▼                                         ▼
        ┌─────────────────────────┐               ┌─────────────────────────┐
        │     Rasa Form Loop      │               │   Rasa Action Server    │
        │  Captures Service &     │               │  (Port 5055 / LangChain)│
        │  User Name via from_text│               └────────────┬────────────┘
        └────────────┬────────────┘                            │
                     │                           1. Retrieves "company_info.txt"
                     │                           2. Prompts Gemini Flash Lite
                     │                                         │
                     ▼                                         ▼
        ┌───────────────────────────────────────────────────────────────────┐
        │            💬 Final Localized Response displayed on UI            │
        └───────────────────────────────────────────────────────────────────┘
    </div>
  </div>

  <div class="section-card">
    <div class="section-title">🧩 3. The 3 Main Parts & Code (Explained in Plain English)</div>
    <div class="component-grid">
      <div class="component-col">
        <h4>1. The Face (Website)</h4>
        <p><strong>File:</strong> <code>frontend/app.py</code><br>
        Built with Streamlit. Shows chat history, diagnostic health lights, and instant language detection badges (e.g. 🇪🇸 Spanish • 99%).</p>
      </div>
      <div class="component-col">
        <h4>2. The Manager (Rasa)</h4>
        <p><strong>Folder:</strong> <code>rasa_bot/</code><br>
        Tracks dialog state. Uses <code>appointment_form</code> in <code>domain.yml</code> with <code>from_text</code> mapping to accept any custom name.</p>
      </div>
      <div class="component-col">
        <h4>3. The Brain (LangChain)</h4>
        <p><strong>Folder:</strong> <code>action_server/</code><br>
        Port 5055. Uses <code>detector.py</code> to identify scripts, reads <code>company_info.txt</code>, and prompts Gemini for native answers.</p>
      </div>
    </div>
  </div>

  <div class="footer-bar">
    Smart Multilingual AI Chatbot | MVJCE Dept. of CSE | Page 1 of 2
  </div>
</div>

<!-- PAGE 2: STEP-BY-STEP EXAMPLES, VIVA Q&A, AND DEMO CHEAT SHEET -->
<div>
  <div class="section-card" style="border-left-color: #059669;">
    <div class="section-title" style="color: #065f46;">🔄 4. Step-by-Step Live Demo Scenarios</div>
    
    <div style="margin-bottom: 12px;">
      <span class="step-pill">Demo 1</span> <strong>Multilingual Knowledge RAG (Spanish Pricing Query)</strong>
      <p style="margin: 4px 0 0 0; font-size: 10pt;">
        • <strong>You type:</strong> <code>¿Cuáles son los precios de sus servicios?</code><br>
        • <strong>What happens:</strong> Streamlit displays <code>🇪🇸 Spanish (ES) • 99%</code>. Rasa routes to LangChain. LangChain reads Section 3 of <code>company_info.txt</code> (in English). Gemini synthesizes the pricing tiers ($1,500 Starter, $5,000 Professional) into fluent Spanish!<br>
        • <strong>Evaluator Takeaway:</strong> <em>"We don't need to manually translate our documents into 10 languages—RAG handles localization dynamically."</em>
      </p>
    </div>

    <div>
      <span class="step-pill">Demo 2</span> <strong>Deterministic Booking with ANY Custom Name</strong>
      <p style="margin: 4px 0 0 0; font-size: 10pt;">
        • <strong>Turn 1:</strong> <code>I want to book an appointment</code> ──> Bot asks for service (Cloud, AI Consulting, Web Dev).<br>
        • <strong>Turn 2:</strong> <code>AI Consulting</code> ──> Bot asks: <em>"May I have your name, please?"</em><br>
        • <strong>Turn 3:</strong> <code>Bhargavi</code> (or your name) ──> Bot confirms: <em>"Thank you Bhargavi! Your appointment for AI Consulting has been registered."</em><br>
        • <strong>Evaluator Takeaway:</strong> <em>"Rasa Forms with <code>from_text</code> slot mapping guarantee that any regional or international name is captured with zero hallucination."</em>
      </p>
    </div>
  </div>

  <div class="section-card" style="border-left-color: #9333ea;">
    <div class="section-title" style="color: #6b21a8;">🎯 5. Top 4 Viva Questions & Winning Answers</div>
    
    <div class="qa-box">
      <div class="qa-q">Q1: "Why not use only ChatGPT or Gemini for the entire chatbot?"</div>
      <div class="qa-a">"Pure LLMs frequently hallucinate incorrect pricing, cannot strictly guarantee that required form fields (like service or user name) are collected, and calling an external API for simple greetings like 'Hello' wastes money and adds unnecessary network lag."</div>
    </div>

    <div class="qa-box">
      <div class="qa-q">Q2: "How does the bot understand Spanish/French if the knowledge base is in English?"</div>
      <div class="qa-a">"Through Retrieval-Augmented Generation (RAG). LangChain retrieves the factual English paragraphs from <code>company_info.txt</code> and instructs Gemini: <em>'Answer the user's question in their native language using only these verified facts.'</em>"</div>
    </div>

    <div class="qa-box">
      <div class="qa-q">Q3: "How does the language detection work without lagging?"</div>
      <div class="qa-a">"We use a fast 4-tier hybrid detector in <code>detector.py</code>: Unicode character block analysis immediately identifies Hindi (Devanagari), Arabic, and CJK with 100% accuracy, punctuation markers (<code>¿</code>) catch Spanish, and lexicon overlap catches short words."</div>
    </div>

    <div class="qa-box">
      <div class="qa-q">Q4: "How did you solve the problem of custom names not being recognized in Rasa?"</div>
      <div class="qa-a">"Instead of relying on entity extraction which only recognizes pre-trained names, we defined an <code>appointment_form</code> in <code>domain.yml</code> with a <code>from_text</code> slot mapping. Once the bot asks for the name, any text the user enters is automatically saved."</div>
    </div>
  </div>

  <div class="section-card" style="border-left-color: #d97706; margin-bottom: 0;">
    <div class="section-title" style="color: #b45309;">⚡ 6. Presentation Day Quick Reference Commands</div>
    <table>
      <tr>
        <th style="width: 25%;">Task</th>
        <th style="width: 45%;">What to Type in Chat</th>
        <th style="width: 30%;">Key Talking Point</th>
      </tr>
      <tr>
        <td><strong>Spanish Pricing</strong></td>
        <td><code>¿Cuáles son los precios de sus servicios?</code></td>
        <td>Multilingual RAG + English facts</td>
      </tr>
      <tr>
        <td><strong>French Support</strong></td>
        <td><code>Quels sont vos horaires de support client ?</code></td>
        <td>24/7/365 global hub details</td>
      </tr>
      <tr>
        <td><strong>Hindi / Hinglish</strong></td>
        <td><code>Namaste, kya aap meri madad kar sakte hain?</code></td>
        <td>Devanagari script + Indic detection</td>
      </tr>
      <tr>
        <td><strong>Booking Flow</strong></td>
        <td><code>I want to book an appointment</code></td>
        <td>Rasa Form + Custom Name slot filling</td>
      </tr>
    </table>
  </div>

  <div class="footer-bar">
    Smart Multilingual AI Chatbot | MVJCE Dept. of CSE | Page 2 of 2
  </div>
</div>

</body>
</html>
"""

def generate_pdf():
    print(f"1. Writing HTML to {HTML_PATH}...")
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)
    print("HTML created successfully.")

    print(f"2. Compiling PDF using Edge headless...")
    cmd = [
        EDGE_EXE,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_PATH}",
        str(HTML_PATH)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and PDF_PATH.exists():
        size_kb = PDF_PATH.stat().st_size / 1024
        print(f"SUCCESS! Quick Guide PDF generated at: {PDF_PATH} ({size_kb:.1f} KB)")
    else:
        print(f"Error: {result.returncode}")
        print(result.stderr)

if __name__ == "__main__":
    generate_pdf()
