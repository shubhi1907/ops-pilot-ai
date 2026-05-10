from ai.openai_service import (
    agent_decision,
    generate_response
)


# =====================================
# CLASSIFICATION AGENT
# =====================================

def classification_agent(email: str):
    """
    Determines:
    - category
    - priority
    """

    return agent_decision(email)


# =====================================
# DECISION AGENT
# =====================================

def decision_agent(email: str, classification: dict):
    """
    Determines:
    - escalation
    - department
    - risk
    """

    return classification


# =====================================
# RESPONSE AGENT
# =====================================

def response_agent(email: str, category: str, context: list):
    """
    Generates customer response
    """

    return generate_response(
        email,
        category,
        context
    )