from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def get_question_generator_chain(api_key):
    # Using 'gemini-3-flash' is perfect for high-speed literary audits
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        google_api_key=api_key,
        temperature=1.0,
        thinking_level="medium"
    )
    template = """
    ROLE: You are an expert Literary Analyst and Developmental Editor.
    TASK: 
    1. Review the provided context from the manuscript.
    2. Address the USER'S SPECIFIC REQUEST directly.
    3. If the user asks a factual question (like "who are the characters"), answer it clearly using the context.
    4. If the user asks for an audit or analysis, provide your professional editorial feedback.
    
    GUIDELINES:
    1. IF THE QUERY IS FACTUAL (e.g., "who are the characters", "what happened in chapter 2"):
        -Provide a direct, comprehensive answer based on the context.
        -Mention the page numbers where you found the information.

    2. IF THE QUERY IS ANALYTICAL (e.g., "audit the pacing", "check for inconsistencies"):
        -Act as a critic. Formulate 2-3 deep questions for the author.
        -For each question, provide an 'Expected Answer' and the 'Why this matters' structural impact.
        -Reference specific page numbers (e.g., [📍 Page X]).
    
    3. ALWAYS be grounded in the text. Do not hallucinate external books unless the context explicitly mentions them.
    CONTEXT:
    {context}

    USER QUERY: {query}
    
    YOUR PROFESSIONAL RESPONSE:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["context"])
    
    # Industry standard: Using the Pipe (LCEL) syntax instead of LLMChain
    return prompt | llm