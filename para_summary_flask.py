from flask import Flask, request, jsonify, render_template
import os
import json
from openai import OpenAI

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = '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'

# Initialize OpenAI client
client = OpenAI()

def generate_summary(user_prompt, sys_prompt):
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages
    )

    summary_text = response['choices'][0]['message']['content']
    return summary_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    user_prompt = request.form['user_prompt']
    sys_prompt = """
    You are an AI model that can summarize text inputs given by the user.
    
    Give the output in the following JSON format:
    
    {"summary_text": [write summary text here]}
    """
    if user_prompt:
        summary_text = generate_summary(user_prompt, sys_prompt)
        return jsonify({
            "original_text": user_prompt,
            "summary_text": summary_text
        })
    return jsonify({
        "error": "Please provide text to summarize."
    })

if __name__ == "__main__":
    app.run(debug=True)
