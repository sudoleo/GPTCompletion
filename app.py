from flask import Flask, render_template, request, jsonify
import openai
import re

app = Flask(__name__)

def set_api_key(api_key):
    openai.api_key = api_key

@app.route('/set-api-key', methods=['POST'])
def set_api_key_route():
    api_key = request.form['api_key']
    try:
        set_api_key(api_key)
        return {"status": "success"}
    except openai.error.AuthenticationError:
        return {"status": "error"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complete', methods=['POST'])
def complete():
    input_text = request.form['input_text']
    context_text = request.form.get('context_text', '')
    completions = complete_text(input_text, context_text)
    return {'completions': completions}

def complete_text(prompt, context_text='', n=1):
    if context_text:
        prompt = f"{context_text}\n{prompt}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=80,  # Set a higher max_tokens value to ensure you get a full sentence
        n=n,
        stop=None,
        temperature=0.7,
    )
    
    completions = []
    for choice in response.choices:
        completion = choice.text.strip()
        sentences = re.split(r'(?<=[.!?])\s+', completion)
        first_sentence = sentences[0] if sentences else ''
        completions.append(first_sentence.strip())

    return completions

if __name__ == '__main__':
    app.run(debug=True)
