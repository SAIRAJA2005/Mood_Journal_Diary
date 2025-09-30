import os
import json
from google import genai
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any

# --- Pydantic Schema ---


# Define a restricted set of mood labels
Mood = Literal["Joyful", "Happy", "Calm", "Neutral", "Anxious", "Stressed", "Sad", "Angry", "Frustrated"]

class Recommendation(BaseModel):
    """A sub-model for a single book or movie recommendation."""
    title: str = Field(description="The title of the movie or book.")
    reason: str = Field(description="A brief, one-sentence reason for the recommendation.")

class UserAnalysis(BaseModel):
    """The main structured model for all analysis and recommendations."""
    overall_mood: Mood = Field(description="The primary emotional state derived from the user's text.")
    mood_summary: str = Field(description="A brief explanation of why the text suggests this mood.")
    health_tip_1: str = Field(description="A practical, first tip for staying healthy based on the mood.")
    health_tip_2: str = Field(description="A second, complementary tip for mental or physical wellness.")
    movie_recommendations: List[Recommendation] = Field(
        default=[], 
        description="A list of movie recommendations, or an empty list if none were requested."
    )
    book_recommendations: List[Recommendation] = Field(
        default=[], 
        description="A list of book recommendations, or an empty list if none were requested."
    )

# --- Core Logic Function ---

def analyze_user_input(
    user_text: str, 
    num_movies: int = 0, 
    num_books: int = 0,
    api_key: str = None
) -> Dict[str, Any]:
    """
    Analyzes user text using the Gemini API and returns a structured dictionary.
    """
    
    # 1. Initialize Client
    try:
        # Pass the key directly to the client constructor
        client = genai.Client(api_key=api_key)  # <--- USE THE api_key HERE
    except Exception as e:
        return {"error": f"API Client Error. Ensure GEMINI_API_KEY is set. Details: {e}"}

    # 2. Dynamically Build Instructions
    recommendation_instructions = ""
    
    if num_movies > 0:
        recommendation_instructions += f"and suggest exactly {num_movies} relevant movies,"
    
    if num_books > 0:
        recommendation_instructions += f"and suggest exactly {num_books} relevant books,"
        
    recommendation_instructions = recommendation_instructions.rstrip(', ')
    
    # 3. Define System Instruction and Prompt
    system_instruction = (
        "You are an empathetic wellness assistant. Your task is to analyze the user's "
        "text, determine their mood, provide two helpful health and wellness tips tailored "
        "to that mood"
        f" {recommendation_instructions}. "
        "You must return the entire response in a single JSON object that strictly adheres "
        "to the provided schema. If a recommendation type was not requested (count is 0), "
        "return an empty list for that field."
    )
    
    prompt = f"Analyze my current situation and provide advice based on this: '{user_text}'"

    # 4. Generate Content
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "system_instruction": system_instruction,
                "response_mime_type": "application/json",
                "response_schema": UserAnalysis,
            },
        )
        
        # The SDK automatically parses the JSON into the Pydantic object
        # We convert it to a dict for easy use in Streamlit's session_state
        return {"success": True, "data": response.parsed.model_dump()}

    except Exception as e:
        return {"error": f"Gemini API Call Failed. Details: {e}"}

# --- Optional History Management (Stub) ---
# NOTE: In a full project, this would use SQLite or similar. 
# For Streamlit prototyping, session_state is used in app.py
def get_mood_history():
    """Placeholder for fetching a user's past entries."""
    # In a real app, this would query a database

    return []
