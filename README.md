# 🧘 Mood Diary Compass: An AI-Powered Wellness Journal

A sophisticated web application built with Streamlit and the Google Gemini API that transforms unstructured text journal entries into structured, actionable wellness reports, complete with personalized recommendations for books and movies.

## 🚀 Live Demo

Experience the app directly on Streamlit Community Cloud:
👉 **[Launch Mood Diary Compass Here](https://mood-journal-dairy.streamlit.app/)** 👈

## ✨ Key Features

- **Structured Mood Analysis**: Uses Gemini's advanced reasoning capabilities to extract key metrics (e.g., Energy Level, Stress Factor, Primary Emotion) from free-form text
- **Pydantic Schema Enforcement**: Guarantees reliable, structured JSON output from the LLM using Pydantic for seamless data integration into the Streamlit UI
- **Personalized Recommendations**: Based on the analyzed mood and recommended actions, the app suggests relevant books and movies to help balance the user's emotional state
- **Real-Time Visualization**: Tracks and displays the user's mood trends over time using Streamlit's built-in charting for quick insights
- **Modular Architecture**: Separates the UI (app.py) from the core AI logic (gemini_logic.py) for clean, maintainable code

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| Frontend/App Framework | Streamlit | Rapidly create the interactive, data-driven web interface |
| Large Language Model | Google Gemini API | Provides the core intelligence for text analysis and generation |
| Data Structuring | Pydantic | Defines and enforces data schemas for reliable, predictable JSON output from the Gemini model |
| Data Handling | Pandas | Used for managing and manipulating the mood history data |
| Deployment | Streamlit Community Cloud | Hosts the application live and securely handles API secrets |

## 💻 Local Setup and Installation

Follow these steps to run the application on your local machine for development or testing.

### 1. Clone the Repository

git clone https://github.com/SAIRAJA2005/Mood_Journal_Diary
cd Mood_Journal_Diary


### 2. Set up the Environment

Create a virtual environment and install the required packages:

Create and activate environment
python -m venv venv
source venv/bin/activate # On Windows, use: .\venv\Scripts\activate

Install dependencies
pip install -r requirements.txt


### 3. Configure API Key

- The app requires a Gemini API Key
- Get your key from [Google AI Studio](https://aistudio.google.com/apikey)
- Create a file named `.env` in the root directory
- Add your API key to the `.env` file:

.env file content
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"



### 4. Run the Application

Execute the main Streamlit application file:

streamlit run app.py



The app will automatically open in your browser at `http://localhost:8501`.

## 📁 File Structure

```plaintext
.
├── .streamlit/
│   └── secrets.toml       # For cloud deployment secrets (not committed)
├── app.py                 # Streamlit UI — handles user input and displays output
├── gemini_logic.py        # Core logic — calls Gemini API and applies Pydantic schemas
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
└── README.md              # Project documentation

```


## 🛣️ Future Enhancements

- **Database Integration**: Implement SQLite or another small database to persist mood history and trends beyond the current session
- **RAG Implementation**: Incorporate a small vector store to allow Gemini to provide recommendations based on an existing library of curated content
- **User Authentication**: Add basic sign-in functionality to isolate user data

## 📧 Contact

**[Sai Raja Saride]** – [sairajasaride113@gmail.com] – [https://www.linkedin.com/in/sairaja-saride-b4292725b/]

**Project Link**: [https://github.com/SAIRAJA2005/Mood_Journal_Diary](https://github.com/SAIRAJA2005/Mood_Journal_Diary)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
LICENSE

MIT License

Copyright (c) 2025 [Sai Raja Saride]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

