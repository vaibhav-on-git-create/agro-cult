import os
from groq import Groq

def groq_chat_single_query(query: str, response_language: str = "HINDI AND ENGLISH") -> str:
    """
    Single function to handle a query and return the chatbot response with real-time data capability.
    response_language controls the default language of chatbot replies.
    """
    api_key = "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"
    if not api_key:
        raise ValueError("Please set the GROQ_API_KEY environment variable with your API key.")

    client = Groq(api_key=api_key)

    categorization_model = "openai/gpt-oss-20b"
    main_model = "openai/gpt-oss-20b"
    tool_model = "groq/compound-mini"

    system_message = {
        "role": "system",
        "content": f"""
        You are a very accurate chatbot assisting a farmer , and pefer to give one or two liner answer.
        Provide to-the-point, concise, and practical answers tailored to agricultural topics, farming practices, weather updates, crop management, and related real-time data.
        When asked for real-time or current information, first use the provided tools to gather data, then use that data to answer the user's query.
        Consider that the user values clear, actionable advice and information relevant to farming and agriculture.
        Always respond in {response_language}.
        """
    }

    categorization_prompt = {
        "role": "system",
        "content": """
        Categorize the user's query into one of two types:
        - REAL_TIME: If the query asks for current, recent, or up-to-date information that a general LLM would not know. Examples: "What is the latest news?", "Who won the game?", "Current stock price of Google?".
        - GENERAL: If the query can be answered with general knowledge. Examples: "What is the capital of France?", "Write a poem about nature.", "Explain photosynthesis.".
        
        Your response must be a single word: either 'REAL_TIME' or 'GENERAL'.
        """
    }

    # Step 1: Categorize the query
    category_completion = client.chat.completions.create(
        model=categorization_model,
        messages=[
            categorization_prompt,
            {"role": "user", "content": query}
        ]
    )
    category = category_completion.choices[0].message.content.strip()

    # Step 2: Respond based on category
    if category == "REAL_TIME":
        # Get real-time data using tool model
        tool_completion = client.chat.completions.create(
            model=tool_model,
            messages=[{"role": "user", "content": query}],
            tool_choice="auto"
        )
        real_time_content = tool_completion.choices[0].message.content

        combined_prompt = f"""
        REAL-TIME DATA (DO NOT EDIT):
        {real_time_content}

        USER'S ORIGINAL QUERY (USE DATA ABOVE TO ANSWER):
        {query}
        """

        main_completion = client.chat.completions.create(
            model=main_model,
            messages=[
                system_message,
                {"role": "user", "content": combined_prompt}
            ],
            stream=False
        )
    else:
        # General query handled directly by main model
        main_completion = client.chat.completions.create(
            model=main_model,
            messages=[
                system_message,
                {"role": "user", "content": query}
            ],
            stream=False
        )

    # Collect full response text
    response = main_completion.choices[0].message.content
    return response

# response = groq_chat_single_query("What is the weather today?", response_language="Hindi")
# print("Bot:", response)
"""
You are a very accurate and highly concise chatbot assisting a farmer. Your mission is to provide to-the-point,
 one-or-two-line answers that are practical and actionable for agricultural topics. When asked for any current information,
   first use your tools to get real-time data before providing a solution. This includes any requests for a profitable crop analysis,
     where you will act as a demand analyzer to summarize the best crop,
 its pricing, and key buyers based on a specific country and state.
"""