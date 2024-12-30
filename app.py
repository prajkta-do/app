import sqlite3
import openai
from datetime import datetime

# Initialize OpenAI API key
openai.api_key = 'your-openai-api-key-here'

# Connect to SQLite database
conn = sqlite3.connect('ai_intern.db')
cursor = conn.cursor()

# Create FAQ table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS faq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Function to call OpenAI API
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful support assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response at this time."


# Function to handle FAQ task
def ask_faq(question):
    # Check if the question already exists in the database
    cursor.execute('SELECT answer FROM faq WHERE question = ?', (question,))
    result = cursor.fetchone()

    if result:
        print("Answer retrieved from the database.")
        return result[0]  # Return the answer from the database

    # Generate answer using OpenAI API
    print("Generating a new answer...")
    prompt = f"Answer the following question in one paragraph: {question}"
    answer = generate_response(prompt)

    # Save the question and answer to the database
    if "Error" not in answer:
        cursor.execute('INSERT INTO faq (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()

    return answer

if __name__ == "__main__":
    print("Welcome to the FAQ System!")
    while True:
        print("\nEnter your question (or type 'exit' to quit):")
        user_question = input("Question: ").strip()

        if user_question.lower() == 'exit':
            print("Exiting the FAQ System. Goodbye!")
            break

        # Get the answer for the user's question
        answer = ask_faq(user_question)
        print(f"\nAnswer: {answer}")
