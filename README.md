# 🏢 Business Email & Report Manager

A complete AI-powered business assistant that writes professional emails,
generates reports from data, summarizes meetings, analyzes business metrics,
and drafts client communications — all from a simple chat interface.

---

## 🚀 Installation

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Copy the env template:
   cp .env.example .env
4. Add your OpenAI API key to .env:
   OPENAI_API_KEY=your-key-here
5. Run the assistant:
   python program.py

---

## 💡 Features

### ✉️ Smart Email Writer
Writes professional business emails on any topic.
Researches market trends before writing if a topic is provided.
Supports formal, professional, and friendly tones.
Works for clients, teams, stakeholders, and suppliers.
Example: type 1 → enter purpose → choose tone

### 📊 Report Generator
Creates structured business reports from your sales or revenue data.
Automatically calculates totals, averages, growth rates, and more.
Outputs a formatted report with executive summary and recommendations.
Supports sales, quarterly, revenue, and performance report types.
Example: type 2 → enter data as JSON → get full report

### 📋 Meeting Summarizer
Converts raw meeting notes into a clean structured summary.
Extracts key discussion points, decisions made, and action items.
Identifies owners and deadlines from the notes automatically.
Example: type 3 → paste notes → get formatted summary

### 🔢 Data Analyzer
Analyzes business metrics using natural language queries.
Calculates averages, totals, growth rates, highs, and lows.
Provides interpretation and actionable recommendations.
Example: type 4 → ask your question → enter your data

### 🤝 Client Communication Drafter
Drafts professional communications for any client situation.
Supports project proposals, status updates, inquiry responses, and follow-ups.
Adapts tone and structure to the communication type automatically.
Example: type 5 → choose type → enter client details

---

## 🛠️ Tools

| Tool            | What it does                              | Used by                      |
|-----------------|-------------------------------------------|------------------------------|
| Calculator      | Financial calculations and percentages    | Report Generator, Data Analyzer |
| Web Search      | Market trends and industry research       | Email Writer                 |
| Data Analyzer   | Sum, average, max, min on business data   | Report Generator, Data Analyzer |
| Report Formatter| Generates professional report structures  | Report Generator             |

---

## 💬 Commands

| Command | Action                          |
|---------|---------------------------------|
| 1       | Open Email Writer               |
| 2       | Open Report Generator           |
| 3       | Open Meeting Summarizer         |
| 4       | Open Data Analyzer              |
| 5       | Open Client Communication Drafter |
| help    | Show the help menu              |
| exit    | Quit the assistant              |

You can also just type naturally:
  "write an email to our investors about Q2 results"
  "draft a proposal for ABC Technologies"
  "analyze this data: [50000, 60000, 70000, 80000]"

---

## 📁 File Structure

business-assistant/
├── business_assistant.py   # Main program (all features + tools)
├── README.md               # This file
├── requirements.txt        # Dependencies
├── .env                    # Your API key (not on GitHub)
├── .env.example            # API key template
└── examples/
    ├── email_examples.txt      # Sample email outputs
    ├── report_examples.txt     # Sample report outputs
    └── meeting_examples.txt    # Sample meeting summaries

---

## 📦 Requirements

openai
python-dotenv

---

## 🔑 .env.example

OPENAI_API_KEY=your-openai-api-key-here
