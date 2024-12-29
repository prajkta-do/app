import sqlite3
import openai
from datetime import datetime

# Initialize OpenAI API key
openai.api_key = 'your-openai-api-key-here'

# Connect to SQLite database
conn = sqlite3.connect('ai_intern.db')
cursor = conn.cursor()

# Create necessary tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS faq (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS content_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT,
    summary TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS journal_reflection (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    journal_entry TEXT,
    reflection TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS idea_generator (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    ideas TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS email_reply (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_email TEXT,
    reply TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS code_snippets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_description TEXT,
    code_snippet TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keywords TEXT,
    blog_content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    questions TEXT,
    answers TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sentiment_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    sentiment TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS product_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reviews TEXT,
    summary TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS course_chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_description TEXT,
    subject TEXT,
    level TEXT,
    chapters TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

# Function to call ChatGPT API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Change to the model you use
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

# Task 1: Automated FAQ System
def ask_faq(question):
    prompt = f"You are a support assistant. Answer the following question in one paragraph: {question}"
    answer = generate_response(prompt)
    cursor.execute('''
    INSERT INTO faq (question, answer) VALUES (?, ?)
    ''', (question, answer))
    conn.commit()
    return answer

# Task 2: Content Summarizer
def summarize_content(text):
    prompt = f"Summarize the following text in under 150 words: {text}"
    summary = generate_response(prompt)
    cursor.execute('''
    INSERT INTO content_summary (original_text, summary) VALUES (?, ?)
    ''', (text, summary))
    conn.commit()
    return summary

# Task 3: Daily Journal with AI Reflection
def journal_reflection(entry):
    prompt = f"Generate a positive reflection or insight based on this journal entry: {entry}"
    reflection = generate_response(prompt)
    cursor.execute('''
    INSERT INTO journal_reflection (journal_entry, reflection) VALUES (?, ?)
    ''', (entry, reflection))
    conn.commit()
    return reflection

# Task 4: Idea Generator
def generate_ideas(topic):
    prompt = f"Generate three unique ideas related to the following topic: {topic}"
    ideas = generate_response(prompt)
    cursor.execute('''
    INSERT INTO idea_generator (topic, ideas) VALUES (?, ?)
    ''', (topic, ideas))
    conn.commit()
    return ideas

# Task 5: AI Email Reply Generator
def generate_email_reply(email_content):
    prompt = f"Write a professional reply to the following email: {email_content}"
    reply = generate_response(prompt)
    cursor.execute('''
    INSERT INTO email_reply (original_email, reply) VALUES (?, ?)
    ''', (email_content, reply))
    conn.commit()
    return reply

# Task 6: Code Snippet Generator
def generate_code_snippet(task_description):
    prompt = f"Write a Python function that solves the following task: {task_description}"
    code_snippet = generate_response(prompt)
    cursor.execute('''
    INSERT INTO code_snippets (task_description, code_snippet) VALUES (?, ?)
    ''', (task_description, code_snippet))
    conn.commit()
    return code_snippet

# Task 7: Keyword-Based Blog Generator
def generate_blog_post(keywords):
    prompt = f"Write a short blog post about: {keywords}"
    blog_content = generate_response(prompt)
    cursor.execute('''
    INSERT INTO blog_posts (keywords, blog_content) VALUES (?, ?)
    ''', (keywords, blog_content))
    conn.commit()
    return blog_content

# Task 8: AI-Based Quiz Generator
def generate_quiz(topic):
    prompt = f"Generate 5 quiz questions with answers about: {topic}"
    quiz = generate_response(prompt)
    cursor.execute('''
    INSERT INTO quizzes (topic, questions, answers) VALUES (?, ?, ?)
    ''', (topic, quiz, "Answers Placeholder"))
    conn.commit()
    return quiz

# Task 9: Sentiment Analysis Tool
def analyze_sentiment(text):
    prompt = f"Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral: {text}"
    sentiment = generate_response(prompt)
    cursor.execute('''
    INSERT INTO sentiment_analysis (text, sentiment) VALUES (?, ?)
    ''', (text, sentiment))
    conn.commit()
    return sentiment

# Task 10: Product Review Summarizer
def summarize_product_reviews(reviews):
    prompt = f"Summarize the following product reviews into key takeaways: {reviews}"
    summary = generate_response(prompt)
    cursor.execute('''
    INSERT INTO product_reviews (reviews, summary) VALUES (?, ?)
    ''', (reviews, summary))
    conn.commit()
    return summary

# Task 11: Chapter Generator for Course Creation
def generate_course_chapters(course_description, subject, level):
    prompt = f"Create a table of contents for a course with the following details: Description: {course_description}, Subject: {subject}, Level: {level}."
    chapters = generate_response(prompt)
    cursor.execute('''
    INSERT INTO course_chapters (course_description, subject, level, chapters) VALUES (?, ?, ?, ?)
    ''', (course_description, subject, level, chapters))
    conn.commit()
    return chapters

# Example use of one of the tasks
if __name__ == "__main__":
    question = "What is Artificial Intelligence?"
    print("FAQ Answer: ", ask_faq(question))
    
    text = "AI is a branch of computer science that aims to create machines that can simulate human intelligence."
    print("Summary: ", summarize_content(text))

    journal = "Today was a great day, I learned a lot about Python programming."
    print("Reflection: ", journal_reflection(journal))

    topic = "Sustainability"
    print("Ideas: ", generate_ideas(topic))

    email = "Can you provide more details about the upcoming project?"
    print("Email Reply: ", generate_email_reply(email))

    task = "Write a Python function that calculates the factorial of a number."
    print("Code Snippet: ", generate_code_snippet(task))

    keywords = "climate change, solutions, environment"
    print("Blog Post: ", generate_blog_post(keywords))

    quiz_topic = "Python programming"
    print("Quiz: ", generate_quiz(quiz_topic))

    sentiment_text = "I am really happy with the progress of my project!"
    print("Sentiment: ", analyze_sentiment(sentiment_text))

    reviews = "Great product, works as expected! Highly recommend."
    print("Product Review Summary: ", summarize_product_reviews(reviews))

    course_description = "A beginner's guide to Python."
    subject = "Programming"
    level = "Beginner"
    print("Course Chapters: ", generate_course_chapters(course_description, subject, level))
