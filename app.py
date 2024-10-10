# Import required libraries
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Groq API key and URL from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")

# Function to make a request to Groq API for book recommendations
def get_groq_recommendations(user_input):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Use the Llama 3 Groq 70B model for your recommendations
    data = {
        "model": "llama3-groq-70b-8192-tool-use-preview",  # Update to the recommended model ID
        "messages": [
            {"role": "system", "content": "You are a helpful book recommendation assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }

    # Send POST request to the Groq API
    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        # Print the error response for debugging
        print(f"Error: {response.status_code}, Response: {response.text}")
        print(f"Request Data: {data}")  # Log the request data for further debugging
        return "🚨 Error: Unable to fetch book recommendations. Please try again."

# Streamlit UI
def main():
    # Title with emoji
    st.title("📚 Book Recommendation Chatbot 🤖")
    st.write("Get personalized book recommendations in *English* or *Urdu* based on your favorite genre! 🌍📖")

    # Ask user for input on genre and language
    genre = st.text_input("🔍 Enter the genre you're interested in (e.g., thriller, romance):")
    language = st.selectbox("🌐 Choose the language:", ["English", "Urdu"])

    # Initialize session state for recommendations
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []

    if st.button("📚 Get Recommendations"):
        if genre and language:
            # Prepare user input for the Groq API
            user_input = f"Please provide me with the top 5 book recommendations for the {genre} genre in {language}."
            # Fetch recommendations from Groq API
            recommendations = get_groq_recommendations(user_input)
            st.session_state.recommendations = recommendations.split('\n')  # Assuming recommendations are line-separated
        else:
            st.warning("⚠️ Please enter both genre and language!")

    # Show recommendations if they exist
    if st.session_state.recommendations:
        st.write("*✨ Your Top 5 Book Recommendations:*")

        # Create a dropdown for users to select a specific book
        selected_book = st.selectbox("📖 Select a book to read:", st.session_state.recommendations)

        if selected_book:
            st.write(f"You selected: **{selected_book}**")
            
            # Add a rating option for the user
            rating = st.slider("⭐ Rate the selected book (1-5):", 1, 5)
            if st.button("💬 Submit Rating"):
                st.success(f"Thank you for your rating of {rating} for '{selected_book}'! Your feedback helps improve the recommendations. 🙏")

# Run the app
if __name__ == "__main__":
    main()





