from flask import Flask, render_template, request
import openai
import re
from spellchecker.spellchecker import SpellChecker

app = Flask(__name__)

def set_api_key(api_key):
    openai.api_key = api_key

@app.route('/set-api-key', methods=['POST'])
def set_api_key_route():
    api_key = request.form['api_key']
    set_api_key(api_key)
    return {"status": "success"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complete', methods=['POST'])
def complete():
    input_text = request.form['input_text']
    context_text = request.form.get('context_text', '')
    completions = complete_text(input_text, context_text)
    misspellings = find_misspellings(input_text)
    return {'completions': completions, 'misspellings': misspellings}

def complete_text(prompt, context_text='', n=1):
    if context_text:
        prompt = f"{context_text}\n{prompt}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=n,
        stop=None,
        temperature=0.7,
    )
    
    completions = []
    for choice in response.choices:
        completion = choice.text.strip()
        completion = re.split(r'[.!?]', completion)[0]
        completions.append(completion + '.')

    return completions


def find_misspellings(text):
    spell = SpellChecker(language='de')
    words = text.split()
    misspelled = spell.unknown(words)
    return ', '.join(misspelled)

if __name__ == '__main__':
    app.run(debug=True)
