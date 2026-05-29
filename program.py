from openai import OpenAI
from dotenv import load_dotenv

import json
import os
import re
from datetime import datetime

# Load API key from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    print("Copy .env.example to .env and add your key")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

print("✅ Setup complete!")


# ============================================================
# TOOL FUNCTIONS
# ============================================================

def calculate(expression):
    """Calculate financial values accurately"""
    try:
        safe_expr = re.sub(r'[^0-9+\-*/.() ]', '', expression)
        result = eval(safe_expr, {"__builtins__": {}}, {})
        return json.dumps({"result": round(result, 4)})
    except Exception as e:
        return json.dumps({"error": str(e)})


def web_search(query):
    """Mock web search for business info"""
    mock_results = {
        "market trends":  "Tech sector showing 18% growth in Q1 2026. AI adoption up 40% YoY across enterprises.",
        "industry news":  "AI integration is the #1 priority for 73% of businesses in 2026. Cloud spending at all-time high.",
        "best practices": "Email best practices: personalization increases open rates by 26%, clear CTAs drive 3x more clicks.",
        "competitor":     "Main competitors expanding to new markets. Consolidation trend visible in mid-market segment.",
        "sales":          "Sales benchmarks 2026: avg SME growth 15%, top performers seeing 40%+ QoQ growth.",
        "revenue":        "Recurring revenue models outperforming one-time sales by 3x in long-term valuation metrics.",
        "email":          "Professional email tips: Keep subject under 50 chars, personalize greeting, one clear CTA.",
        "marketing":      "Digital marketing ROI up 22% in 2026. Content marketing and SEO lead in cost-effectiveness.",
    }
    for keyword in mock_results:
        if keyword in query.lower():
            return json.dumps({"results": mock_results[keyword]})
    return json.dumps({"results": f"Business data for '{query}': Positive momentum with 12-18% sector growth in 2026."})


def analyze_data(data_string, operation):
    """Analyze business data - sum, average, max, min"""
    try:
        parsed = json.loads(data_string)

        if isinstance(parsed, dict):
            values = [float(v) for v in parsed.values()]
        elif isinstance(parsed, list):
            values = [float(x) for x in parsed]
        else:
            return json.dumps({"error": "Invalid data format. Use a JSON list or dict."})

        if operation == "sum":
            result = sum(values)
        elif operation == "average":
            result = sum(values) / len(values)
        elif operation == "max":
            result = max(values)
        elif operation == "min":
            result = min(values)
        else:
            return json.dumps({"error": f"Unknown operation: {operation}"})

        return json.dumps({"result": round(result, 2), "count": len(values)})

    except Exception as e:
        return json.dumps({"error": str(e)})


def format_report(report_type, period, metrics="{}"):
    """Format data into professional report structure"""
    templates = {
        "sales": {
            "sections": ["Executive Summary", "Key Metrics", "Monthly Analysis", "Recommendations"],
            "header": f"{period} Sales Performance Report"
        },
        "quarterly": {
            "sections": ["Overview", "Financial Highlights", "Operational Updates", "Next Steps"],
            "header": f"{period} Quarterly Business Report"
        },
        "revenue": {
            "sections": ["Executive Summary", "Revenue Breakdown", "Growth Analysis", "Forecast"],
            "header": f"{period} Revenue Report"
        },
        "performance": {
            "sections": ["Summary", "KPI Dashboard", "Team Performance", "Action Plan"],
            "header": f"{period} Performance Review"
        },
    }
    template = templates.get(report_type.lower(), templates["sales"])
    return json.dumps({
        "header":    template["header"],
        "sections":  template["sections"],
        "timestamp": datetime.now().strftime("%B %d, %Y"),
    })


# ============================================================
# TOOL SCHEMAS (OpenAI format)
# ============================================================

calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Calculate financial metrics, percentages, and growth rates accurately",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression like '50000 * 0.15' or '(75000-50000)/50000*100'"
                }
            },
            "required": ["expression"]
        }
    }
}

print("✅ Calculator tool defined!")

web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search for market trends, industry news, competitor info, and business best practices",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query e.g. 'market trends 2026' or 'email best practices'"
                }
            },
            "required": ["query"]
        }
    }
}

print("✅ Web search tool defined!")

data_analyzer_tool = {
    "type": "function",
    "function": {
        "name": "analyze_data",
        "description": "Analyze business data: sum, average, max, or min on lists or dicts of numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "data_string": {
                    "type": "string",
                    "description": "JSON list like '[50000,60000]' or dict like '{\"Jan\":50000,\"Feb\":60000}'"
                },
                "operation": {
                    "type": "string",
                    "enum": ["sum", "average", "max", "min"],
                    "description": "Operation to perform on the data"
                }
            },
            "required": ["data_string", "operation"]
        }
    }
}

print("✅ Data analyzer tool defined!")

report_formatter_tool = {
    "type": "function",
    "function": {
        "name": "format_report",
        "description": "Get a professional report template structure with sections and header",
        "parameters": {
            "type": "object",
            "properties": {
                "report_type": {
                    "type": "string",
                    "enum": ["sales", "quarterly", "revenue", "performance"],
                    "description": "Type of report to generate"
                },
                "period": {
                    "type": "string",
                    "description": "Time period e.g. 'Q1 2026' or 'January 2026'"
                },
                "metrics": {
                    "type": "string",
                    "description": "Optional JSON string of pre-calculated metrics"
                }
            },
            "required": ["report_type", "period"]
        }
    }
}

print("✅ Report formatter tool defined!")


# ============================================================
# FEATURE CLASSES
# ============================================================

class EmailWriter:
    """
    Feature 1: Smart Email Writer
    Writes professional emails with optional market research via web_search tool.
    """

    def __init__(self):
        self.tools = [web_search_tool, calculator_tool]
        self.functions = {
            "web_search": web_search,
            "calculate":  calculate,
        }

    def write(self, purpose, recipient="stakeholder", tone="formal", research_topic=None):
        print(f"\n📧 Writing email | Purpose: {purpose}")
        print(f"   Recipient: {recipient} | Tone: {tone}")
        if research_topic:
            print(f"   🔍 Will research: {research_topic}\n")

        system_prompt = f"""You are a professional business email writer.
Write in a {tone} tone addressed to a {recipient}.
{'Use the web_search tool to research the topic before writing.' if research_topic else ''}
Always include:
  - Subject: [subject line]
  - A proper greeting
  - 3-5 well-structured body paragraphs
  - A professional closing with signature placeholder [Your Name]"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write a business email.\nPurpose: {purpose}\nRecipient: {recipient}\nTone: {tone}\n{'Research topic: ' + research_topic if research_topic else ''}"}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.tools
            )
        except Exception as e:
            print(f"Error occurred while writing email: {e}")
            return

        response_message = response.choices[0].message

        # Check if AI wants to use tools
        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"   🔧 Using tool: {function_name}({function_args})")

                result = self.functions[function_name](**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            try:
                final_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                return final_response.choices[0].message.content
            except Exception as e:
                print(f"Error occurred while getting final email: {e}")
                return

        return response_message.content


class ReportGenerator:
    """
    Feature 2: Report Generator
    Creates professional business reports using data analysis + calculation tools.
    """

    def __init__(self):
        self.tools = [calculator_tool, data_analyzer_tool, report_formatter_tool]
        self.functions = {
            "calculate":     calculate,
            "analyze_data":  analyze_data,
            "format_report": format_report,
        }

    def generate(self, report_type, data, period, company="Your Company"):
        print(f"\n📊 Generating {report_type} report | Period: {period}")
        print(f"   Data: {str(data)[:80]}{'...' if len(str(data)) > 80 else ''}\n")

        system_prompt = """You are a professional business analyst and report writer.
Use the tools in this order:
  1. format_report → get the report structure
  2. analyze_data  → calculate sum, average, max, min on the data
  3. calculate     → compute growth rate and percentages

Then write a complete polished report using ============ dividers for major sections.
Include specific numbers. End with 3-5 concrete recommendations."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate a {report_type} report for {company}.\nPeriod: {period}\nData (JSON): {json.dumps(data) if isinstance(data, dict) else str(data)}\nUse all tools to compute metrics, then write the full report."}
        ]

        # Agentic loop — keep going until no more tool calls
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    tools=self.tools
                )
            except Exception as e:
                return f"❌ API Error: {e}"

            response_message = response.choices[0].message

            if not response_message.tool_calls:
                return response_message.content

            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"   🔧 Using tool: {function_name}({function_args})")

                result = self.functions[function_name](**function_args)
                print(f"   ✅ Result: {result[:100]}{'...' if len(result) > 100 else ''}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })


class MeetingSummarizer:
    """
    Feature 3: Meeting Summarizer
    Converts raw meeting notes into structured summaries with action items.
    """

    def summarize(self, notes, date, attendees=None):
        print(f"\n📋 Summarizing meeting | Date: {date}")
        if attendees:
            print(f"   Attendees: {attendees}\n")

        system_prompt = """You are a professional meeting facilitator and note-taker.
Convert raw meeting notes into a clean structured summary using EXACTLY this format:

===========================================
MEETING SUMMARY
===========================================
Date: [date]
Attendees: [list or Not specified]

SUMMARY
[2-3 sentence high-level overview]

KEY DISCUSSION POINTS
• [point 1]
• [point 2]

DECISIONS MADE
1. [decision]
2. [decision]

ACTION ITEMS
• [Owner]: [task] — [deadline if mentioned]

NEXT MEETING: [date if mentioned, else TBD]
==========================================="""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize these meeting notes:\n\nDate: {date}\nAttendees: {attendees or 'Not specified'}\n\nRaw notes:\n{notes}"}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error occurred while summarizing meeting: {e}")
            return


class DataAnalyzer:
    """
    Feature 4: Data Analyzer
    Analyzes business data with natural language queries using calculator + data analyzer tools.
    """

    def __init__(self):
        self.tools = [calculator_tool, data_analyzer_tool]
        self.functions = {
            "calculate":    calculate,
            "analyze_data": analyze_data,
        }

    def analyze(self, query, data):
        print(f"\n🔢 Analyzing data | Query: {query}")
        print(f"   Data: {str(data)[:80]}{'...' if len(str(data)) > 80 else ''}\n")

        system_prompt = """You are a business data analyst.
Use analyze_data and calculate tools to compute metrics, then present results as:

ANALYSIS RESULTS
==================
[computed metrics with labels]

INTERPRETATION
[2-3 sentences explaining what the numbers mean for the business]

RECOMMENDATION
[1-2 actionable next steps]"""

        data_json = json.dumps(data) if isinstance(data, (dict, list)) else str(data)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {query}\n\nData: {data_json}\n\nUse the tools to calculate all relevant metrics, then answer the query."}
        ]

        # Agentic loop
        while True:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    tools=self.tools
                )
            except Exception as e:
                return f"❌ API Error: {e}"

            response_message = response.choices[0].message

            if not response_message.tool_calls:
                return response_message.content

            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"   🔧 Using tool: {function_name}({function_args})")

                result = self.functions[function_name](**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })


class ClientCommsDrafter:
    """
    Feature 5: Client Communication Drafter
    Creates professional client communications: proposals, updates, responses, follow-ups.
    """

    def __init__(self):
        self.tools = [web_search_tool]
        self.functions = {"web_search": web_search}

    def draft(self, comm_type, client, context, tone="professional but friendly", sender="[Your Name]"):
        print(f"\n🤝 Drafting {comm_type} | Client: {client}")
        print(f"   Tone: {tone}\n")

        system_prompt = f"""You are an expert business communication writer.
Write a compelling {comm_type} that is client-focused and professional.
Sender: {sender}. Tone: {tone}.
Include:
  - Proper greeting with client name
  - 3-4 well-structured paragraphs (context → value → details → next step)
  - A clear call-to-action
  - Warm professional closing"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write a {comm_type} for:\nClient: {client}\nContext: {context}\nTone: {tone}\nSender: {sender}"}
        ]

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.tools
            )
        except Exception as e:
            print(f"Error occurred while drafting communication: {e}")
            return

        response_message = response.choices[0].message

        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"   🔧 Using tool: {function_name}({function_args})")

                result = self.functions[function_name](**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            try:
                final_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                return final_response.choices[0].message.content
            except Exception as e:
                print(f"Error occurred: {e}")
                return

        return response_message.content


# ============================================================
# MAIN BUSINESS ASSISTANT CLASS
# ============================================================

class BusinessAssistant:
    """
    COMPLETE Business Email & Report Manager.

    Features:
    - Smart Email Writer (with research)
    - Report Generator (with data analysis)
    - Meeting Summarizer (with action items)
    - Data Analyzer (with natural language queries)
    - Client Communication Drafter (proposals, updates, follow-ups)

    Tools: calculate, web_search, analyze_data, format_report
    """

    def __init__(self):
        # All tools
        self.tools = [calculator_tool, web_search_tool, data_analyzer_tool, report_formatter_tool]
        self.functions = {
            "calculate":     calculate,
            "web_search":    web_search,
            "analyze_data":  analyze_data,
            "format_report": format_report,
        }

        # Feature sub-components
        self.email_writer   = EmailWriter()
        self.report_gen     = ReportGenerator()
        self.meeting_sum    = MeetingSummarizer()
        self.data_analyzer  = DataAnalyzer()
        self.client_drafter = ClientCommsDrafter()

        print("✅ Business Assistant initialized!")
        print("   Features: Email | Report | Meeting | Data | Client Comms\n")

    def write_email(self, purpose, recipient="stakeholder", tone="formal", research_topic=None):
        """Feature 1: Write a professional business email"""
        return self.email_writer.write(purpose, recipient, tone, research_topic)

    def generate_report(self, report_type, data, period, company="Your Company"):
        """Feature 2: Generate a professional business report from data"""
        return self.report_gen.generate(report_type, data, period, company)

    def summarize_meeting(self, notes, date, attendees=None):
        """Feature 3: Convert raw meeting notes into a structured summary"""
        return self.meeting_sum.summarize(notes, date, attendees)

    def analyze_business_data(self, query, data):
        """Feature 4: Analyze business data with a natural language query"""
        return self.data_analyzer.analyze(query, data)

    def draft_client_communication(self, comm_type, client, context, tone="professional but friendly", sender="[Your Name]"):
        """Feature 5: Draft a professional client communication"""
        return self.client_drafter.draft(comm_type, client, context, tone, sender)

    def route_request(self, request):
        """Decide which feature to use based on keywords"""
        request_lower = request.lower()

        if any(word in request_lower for word in ['email', 'write to', 'compose', 'send message']):
            return 'email'
        elif any(word in request_lower for word in ['report', 'quarterly', 'sales report', 'revenue report']):
            return 'report'
        elif any(word in request_lower for word in ['meeting', 'notes', 'summarize meeting', 'action items']):
            return 'meeting'
        elif any(word in request_lower for word in ['analyze', 'data', 'average', 'sum', 'growth', 'revenue trend']):
            return 'data'
        elif any(word in request_lower for word in ['proposal', 'client', 'draft', 'follow-up', 'status update']):
            return 'client'
        else:
            return 'general'

    def process(self, request):
        """Main request handler - routes to the right feature"""
        capability = self.route_request(request)

        if capability == 'email':
            return self.write_email(purpose=request)
        elif capability == 'report':
            return None  # handled interactively in CLI
        elif capability == 'meeting':
            return None  # handled interactively in CLI
        elif capability == 'data':
            return self.analyze_business_data(query=request, data=[])
        elif capability == 'client':
            return self.draft_client_communication(comm_type="follow-up message", client="Client", context=request)
        else:
            # General assistant with all tools
            messages = [{"role": "user", "content": request}]
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    tools=self.tools
                )
                response_message = response.choices[0].message

                if not response_message.tool_calls:
                    return response_message.content

                messages.append(response_message)
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    result = self.functions[function_name](**function_args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })

                final_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                return final_response.choices[0].message.content

            except Exception as e:
                return f"❌ API Error: {e}"


# ============================================================
# CLI HELPERS
# ============================================================

def show_help():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║               🏢  BUSINESS ASSISTANT — HELP MENU                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  TYPE A NUMBER TO USE A FEATURE:                                    ║
║  1 → Email Writer      Write professional emails with research     ║
║  2 → Report Generator  Generate reports from sales/revenue data    ║
║  3 → Meeting Summarizer  Turn raw notes into action items          ║
║  4 → Data Analyzer     Analyze business metrics naturally          ║
║  5 → Client Comms      Draft proposals, updates, follow-ups        ║
║                                                                     ║
║  OR JUST TYPE NATURALLY:                                            ║
║  "write an email to our investors about Q2 results"                ║
║  "analyze this data: [50000, 60000, 70000]"                        ║
║  "draft a proposal for ABC Technologies"                           ║
║                                                                     ║
║  COMMANDS:                                                          ║
║  help → show this menu       exit → quit                           ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def get_input(prompt, default=""):
    val = input(prompt).strip()
    return val if val else default


def interactive_email(assistant):
    print("\n─── EMAIL WRITER ─────────────────────────────────")
    purpose = get_input("Email purpose: ")
    if not purpose:
        print("❌ Purpose required."); return
    recipient = get_input("Recipient type (client/team/stakeholder/supplier) [stakeholder]: ", "stakeholder")
    tone      = get_input("Tone (formal/professional/friendly) [formal]: ", "formal")
    research  = get_input("Research topic (optional, press Enter to skip): ")
    result    = assistant.write_email(purpose, recipient, tone, research or None)
    print_output(result)


def interactive_report(assistant):
    print("\n─── REPORT GENERATOR ─────────────────────────────")
    report_type = get_input("Report type (sales/quarterly/revenue/performance) [sales]: ", "sales")
    period      = get_input("Time period (e.g. Q1 2026) [Q1 2026]: ", "Q1 2026")
    company     = get_input("Company name [Your Company]: ", "Your Company")
    print('Enter data as JSON (e.g. {"Jan": 50000, "Feb": 65000, "Mar": 70000})')
    raw_data    = get_input("Data: ", '{"Jan": 50000, "Feb": 65000, "Mar": 70000}')
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        print('❌ Invalid JSON. Example: {"Jan": 50000, "Feb": 65000}'); return
    result = assistant.generate_report(report_type, data, period, company)
    print_output(result)


def interactive_meeting(assistant):
    print("\n─── MEETING SUMMARIZER ───────────────────────────")
    date      = get_input(f"Meeting date [{datetime.now().strftime('%B %d, %Y')}]: ", datetime.now().strftime("%B %d, %Y"))
    attendees = get_input("Attendees (comma-separated, optional): ")
    print("Paste meeting notes (type END on a new line when done):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    notes = "\n".join(lines)
    if not notes.strip():
        print("❌ Notes required."); return
    result = assistant.summarize_meeting(notes, date, attendees or None)
    print_output(result)


def interactive_data(assistant):
    print("\n─── DATA ANALYZER ────────────────────────────────")
    query = get_input("Your query (e.g. 'What is avg monthly revenue and growth rate?'): ")
    if not query:
        print("❌ Query required."); return
    print("Enter data as JSON list or dict (e.g. [50000, 60000, 70000])")
    raw_data = get_input("Data: ", "[50000, 60000, 70000]")
    try:
        data = json.loads(raw_data)
    except json.JSONDecodeError:
        print("❌ Invalid JSON. Example: [50000, 60000, 70000]"); return
    result = assistant.analyze_business_data(query, data)
    print_output(result)


def interactive_client(assistant):
    print("\n─── CLIENT COMMUNICATION DRAFTER ────────────────")
    print("Types: project proposal / status update / response to inquiry / follow-up message")
    comm_type = get_input("Communication type [project proposal]: ", "project proposal")
    client    = get_input("Client name / company: ")
    if not client:
        print("❌ Client name required."); return
    sender    = get_input("Your name / company [Your Name]: ", "Your Name")
    tone      = get_input("Tone [professional but friendly]: ", "professional but friendly")
    print("Context and details (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    context = "\n".join(lines).strip()
    if not context:
        print("❌ Context required."); return
    result = assistant.draft_client_communication(comm_type, client, context, tone, sender)
    print_output(result)


def print_output(text):
    if not text:
        return
    print("\n" + "=" * 70)
    print("OUTPUT")
    print("=" * 70)
    print(text)
    print("=" * 70 + "\n")


# ============================================================
# MAIN PROGRAM
# ============================================================

# Create the assistant
assistant = BusinessAssistant()

conversation_history = []

print("🤖 Assistant ready! Type 'help' for commands or 'exit' to quit.\n")
show_help()

user_input = input("You: ").strip()

while user_input.lower() != "exit":

    # Input validation - reject empty input
    if not user_input:
        print("Please enter something!\n")
        user_input = input("You: ").strip()
        continue

    # Help command
    if user_input.lower() == "help":
        show_help()
        user_input = input("You: ").strip()
        continue

    # Feature number shortcuts
    if user_input == "1":
        interactive_email(assistant)
        user_input = input("You: ").strip()
        continue
    elif user_input == "2":
        interactive_report(assistant)
        user_input = input("You: ").strip()
        continue
    elif user_input == "3":
        interactive_meeting(assistant)
        user_input = input("You: ").strip()
        continue
    elif user_input == "4":
        interactive_data(assistant)
        user_input = input("You: ").strip()
        continue
    elif user_input == "5":
        interactive_client(assistant)
        user_input = input("You: ").strip()
        continue

    # Build history as a single string (same pattern as example)
    history_text = ""
    for msg in conversation_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    if history_text:
        full_query = f"Previous conversation:\n{history_text}\nNow answer this: {user_input}"
    else:
        full_query = user_input

    # Route and process
    ai_response = assistant.process(full_query)

    if ai_response is None:
        print("💡 Tip: Type the feature number (1–5) for a guided experience.\n")
        user_input = input("You: ").strip()
        continue

    # Save to history
    conversation_history.append({"role": "user",      "content": user_input})
    conversation_history.append({"role": "assistant",  "content": ai_response or ""})

    print(f"\nAssistant: {ai_response}\n")
    user_input = input("You: ").strip()


print("👋 Goodbye!")
