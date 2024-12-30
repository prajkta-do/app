import sqlite3
from datetime import datetime
import openai

# Set your OpenAI API key
openai.api_key = "use your api key here"

def initialize_database():
    """Initializes the SQLite database."""
    conn = sqlite3.connect("faq_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faq_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_to_database(question, response):
    """Logs the question, response, and timestamp to the database."""
    conn = sqlite3.connect("faq_system.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO faq_logs (question, response, timestamp)
        VALUES (?, ?, ?)
    """, (question, response, timestamp))
    conn.commit()
    conn.close()

def generate_prompt(question):
    """Generates the prompt for the ChatGPT API."""
    return f"You are a support assistant. Answer the following question in one paragraph: {question}"

def get_chatgpt_response(question):
    """Sends the question to the ChatGPT API and retrieves the response."""
    prompt = generate_prompt(question)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred while fetching the response: {e}"

def main():
    """Main function to handle user interaction and system logic."""
    initialize_database()
    print("Welcome to the Automated FAQ System. Type 'exit' to quit.")

    while True:
        user_question = input("Enter your question: ")
        if user_question.lower() == 'exit':
            print("Goodbye!")
            break

        response = get_chatgpt_response(user_question)
        print("\nResponse:")
        print(response)

        log_to_database(user_question, response)
        print("\nYour query and the response have been logged.\n")

if __name__ == "__main__":
    main()
