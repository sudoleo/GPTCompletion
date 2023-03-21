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
    model = request.form.get('model', 'text-davinci-002')
    max_tokens = int(request.form.get('max_tokens', 80))
    temperature = float(request.form.get('temperature', 0.7))
    completions = complete_text(input_text, context_text, model=model, max_tokens=max_tokens, temperature=temperature)
    return {'completions': completions}


def complete_text(prompt, context_text='', n=1, model="text-davinci-002", max_tokens=80, temperature=0.7):
    if context_text:
        prompt = f"{context_text}\n{prompt}"
    
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=None,
        temperature=temperature,
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