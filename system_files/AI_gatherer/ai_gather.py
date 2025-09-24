import os
from groq import Groq

def groq_chat_single_query(query: str, response_language: str = "HINDI AND ENGLISH") -> str:
    """
    Single function to handle a query and return the chatbot response with real-time data capability.
    response_language controls the default language of chatbot replies.
    
    Note: The effectiveness of real-time data integration depends on the capabilities of the
    models used. The prompt has been updated to be more explicit in instructing the model
    to use the data provided by the tool_model and override its own knowledge.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        # Use the provided key if not in environment variables
        api_key = "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"
        if not api_key:
            raise ValueError("Please set the GROQ_API_KEY environment variable with your API key.")

    client = Groq(api_key=api_key)

    categorization_model = "openai/gpt-oss-20b"
    main_model = "openai/gpt-oss-20b"
    tool_model = "groq/compound-mini"

    # Updated system message with the combined prompt
    system_message = {
        "role": "system",
        "content": f"""
        You are a very accurate and highly concise chatbot assisting a farmer. Your mission is to provide to-the-point,you use not more than 10 lines,
        one-or-two-line answers that are practical and actionable for agricultural topics. When asked for any current information,
        first use your tools to get real-time data before providing a solution. This includes any requests for a profitable crop analysis,
        where you will act as a demand analyzer to summarize the best crop, its pricing, and key buyers based on a specific country and state.
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

        # New, more explicit prompt to force the use of real-time data
        combined_prompt = f"""
        You have been provided with the following REAL-TIME DATA from a search tool. You MUST use this data to answer the user's query and ignore any prior knowledge that contradicts this information.

        REAL-TIME DATA (DO NOT EDIT):
        {real_time_content}

        USER'S ORIGINAL QUERY:
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

# The example call remains the same
# response = groq_chat_single_query("stock prise of tata steel", response_language="english")
# print("Bot:", response)
