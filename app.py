from flask import Flask, render_template, request
import openai
import re
from spellchecker.spellchecker import SpellChecker

# Ersetzen Sie YOUR_API_KEY durch Ihren tatsächlichen API-Schlüssel
openai.api_key = "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"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/complete', methods=['POST'])
def complete():
    input_text = request.form['input_text']
    completions = complete_text(input_text)
    misspellings = find_misspellings(input_text)
    return {'completions': completions, 'misspellings': misspellings}

def complete_text(prompt, n=1):
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
