import streamlit as st
import pandas as pd
from gemini_logic import analyze_user_input
import os
import random

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="Mood Diary Compass",
    layout="centered",
    initial_sidebar_state="auto"
)

# Initialize Session State for history and results
if 'history' not in st.session_state:
    st.session_state.history = []

if 'report_data' not in st.session_state:
    st.session_state.report_data = None

# --- Main Logic Function (Called by the button) ---
def generate_report():
    """Handles the full process from user input to API call."""
    
    user_text = st.session_state.user_text
    
    if not user_text:
        st.error("Please describe your current feelings or situation before generating a report.")
        st.session_state.report_data = None
        return
    
        # --- CRITICAL CHANGE: Retrieve API Key from Streamlit Secrets ---
    try:
        gemini_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        st.error("❌ API Key Error: GEMINI_API_KEY not found in Streamlit Secrets. Please configure your secrets.")
        st.session_state.report_data = None
        return

    # Check for recommendation toggles and sliders
    num_movies = st.session_state.movie_toggle * st.session_state.num_movies_slider
    num_books = st.session_state.book_toggle * st.session_state.num_books_slider

    with st.spinner("🧠 Analyzing your mood and generating personalized advice..."):
        # Call the external logic function
        result = analyze_user_input(
            user_text=user_text, 
            num_movies=num_movies, 
            num_books=num_books,
            api_key=gemini_key  # <--- PASS THE KEY HERE
        )

    if result.get("error"):
        st.error(result["error"])
        st.session_state.report_data = None
    else:
        # Store the successful report data
        data = result["data"]
        st.session_state.report_data = data
        
        # Add to history for the future (simple in-memory storage)
        st.session_state.history.append({
            "timestamp": pd.Timestamp.now(),
            "mood": data["overall_mood"],
            "summary": data["mood_summary"],
            "movies": len(data["movie_recommendations"]),
            "books": len(data["book_recommendations"]),
        })

# --- UI Component: Display Report ---
def display_report(data):
    """Formats and displays the structured data from the Gemini API."""
    
    st.markdown("### ✨ Personalized Wellness Report", unsafe_allow_html=True)
    
    # 1. Mood Analysis (Use a container for a clean look)
    col_mood, col_summary = st.columns(2)
    
    col_mood.metric(
        label="Primary Mood Detected",
        value=data["overall_mood"],
        delta_color="off"
    )
    col_summary.info(f"**Summary:** {data['mood_summary']}")

    st.divider()

    # 2. Health & Wellness Tips
    st.markdown("### 🌿 Healthy Living Tips", unsafe_allow_html=True)
    st.success(f"1. {data['health_tip_1']}")
    st.success(f"2. {data['health_tip_2']}")
    
    # 3. Media Recommendations (Dynamic section)
    if data["movie_recommendations"] or data["book_recommendations"]:
        st.divider()
        st.markdown("### 🎬 Media Recommendations", unsafe_allow_html=True)

        col_movies, col_books = st.columns(2)
        
        # Movies
        if data["movie_recommendations"]:
            with col_movies.expander(f"Movies ({len(data['movie_recommendations'])})"):
                for rec in data["movie_recommendations"]:
                    st.write(f"**{rec['title']}**")
                    st.caption(rec['reason'])
        
        # Books
        if data["book_recommendations"]:
            with col_books.expander(f"Books ({len(data['book_recommendations'])})"):
                for rec in data["book_recommendations"]:
                    st.write(f"**{rec['title']}**")
                    st.caption(rec['reason'])
    
# --- UI Component: History and Trend (Resume Feature) ---
def display_history():
    """Displays a mood trend chart using mock scoring."""
    
    if not st.session_state.history:
        st.sidebar.info("Submit your first entry to see your mood history!")
        return
        
    # Map mood to a numeric score for visualization
    mood_score_map = {
        "Joyful": 5, "Happy": 4, "Calm": 3, "Neutral": 3, 
        "Anxious": 2, "Stressed": 2, "Sad": 1, "Angry": 1, "Frustrated": 1
    }

    # Create a DataFrame from history for charting
    df_history = pd.DataFrame(st.session_state.history)
    df_history['score'] = df_history['mood'].map(mood_score_map)
    df_history['day'] = df_history['timestamp'].dt.strftime('%m-%d %H:%M')

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Mood Trend")
    st.sidebar.line_chart(df_history, x='day', y='score', color='#88b495')
    st.sidebar.caption("Higher score = More positive mood.")


# --- Application Layout ---

st.title("Mood Diary Compass 🧭")
st.markdown("### Analyze your current mood and get personalized wellness advice from Mood Diary.")

# 1. User Input Area (Text Area)
st.text_area(
    "✍️ Describe your current feelings or situation:", 
    key="user_text",
    placeholder="Example: I just got a huge promotion at work and am planning a trip to the beach. I feel like everything is finally going my way!"
)

st.markdown("---")

# 2. Recommendation Settings (Interactive Widgets)
st.subheader("🎬 Media Settings")
col1, col2 = st.columns(2)

# Movie Selection
with col1:
    st.toggle("🎬 Want Movie Recommendations?", key="movie_toggle")
    if st.session_state.movie_toggle:
        st.slider("How many movies?", 1, 5, 2, key="num_movies_slider", help="Select 1 to 5 movies.")
    else:
        st.session_state.num_movies_slider = 0

# Book Selection
with col2:
    st.toggle("📚 Want Book Recommendations?", key="book_toggle")
    if st.session_state.book_toggle:
        st.slider("How many books?", 1, 5, 2, key="num_books_slider", help="Select 1 to 5 books.")
    else:
        st.session_state.num_books_slider = 0

# 3. Generate Button
st.markdown("---")
st.button(
    "✨ **Generate My Wellness Report**", 
    on_click=generate_report,
    use_container_width=True,
    type="primary"
)

# 4. Report Output Area
if st.session_state.report_data:
    st.markdown("---")
    display_report(st.session_state.report_data)

# 5. History Sidebar (Resume Feature)

display_history()
