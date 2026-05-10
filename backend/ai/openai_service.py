from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ✅ AGENT DECISION FUNCTION
def agent_decision(email_text: str):
    prompt = f"""
    You are an enterprise AI operations agent.

    Analyze the customer email and determine:

    1. category
    2. priority (Low, Medium, High)
    3. should_escalate (yes/no)
    4. department (Support, Engineering, Billing)
    5. confidence_score (0 to 1)
    6. reasoning
    7. risk_score (0 to 1)

    Risk score represents BUSINESS IMPACT.

    Risk scoring rules:
    - 0.0 - 0.3 → low impact
    - 0.4 - 0.6 → moderate impact
    - 0.7 - 0.8 → high operational impact
    - 0.9 - 1.0 → critical enterprise/business impact

    Examples:
    - Production outage affecting enterprise customers = 0.95
    - Security breach = 0.98
    - Billing complaint = 0.5
    - Login issue affecting few users = 0.4
    - Feature request = 0.2

    IMPORTANT:
    If the email mentions:
    - production outage
    - system down
    - all users affected
    - enterprise customers impacted
    - revenue impact
    - critical issue

    Then risk_score MUST be above 0.9.

    Email:
    {email_text}

    Return ONLY valid JSON.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content

        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())
        else:
            raise ValueError("No JSON found")

    except Exception as e:
        print("AGENT ERROR:", e)

        return {
            "category": "Other",
            "priority": "Medium",
            "department": "Support",
            "should_escalate": "no",
            "confidence_score": 0.5,
            "reasoning": "fallback",
            "risk_score": 0.3
        }


# ✅ RESPONSE GENERATION FUNCTION (THIS WAS MISSING)
def generate_response(email_text: str, category: str, context: list = None):
    context_text = "\n".join(context) if context else "No similar past issues found."

    prompt = f"""
    You are a professional customer support agent.

    Category: {category}

    Use past similar issues if helpful to inform your response.

    Past similar issues:
    {context_text}

    Current customer email:
    {email_text}

    Write a helpful, professional, and empathetic response that addresses the customer's issue.
    Keep the response concise (2-3 paragraphs max).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print(f"RESPONSE GENERATION ERROR: {e}")
        return f"Thank you for contacting us. We have received your {category} request and will get back to you shortly."