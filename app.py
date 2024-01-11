import re
from flask import Flask, render_template, request

app = Flask(__name__)

def clean_mobile_number(data):
    cleaned_numbers = []

    if isinstance(data, str):
        lines = data.split('\n')
    elif hasattr(data, 'read'):
        lines = data.read().decode('utf-8').strip().split('\n')
    else:
        return None

    for line in lines:
        cleaned_number = re.sub(r'\D', '', line)  # Remove non-digit characters
        cleaned_numbers.append(cleaned_number)
        print(f'Original Line: {line}, Cleaned Number: {cleaned_number}')

    return cleaned_numbers

@app.route('/', methods=['GET', 'POST'])
def index():
    cleaned_numbers = None

    if request.method == 'POST':
        if 'url' in request.form:
            # Fetch data from the URL
            url = request.form['url']
            if url.startswith(('http://', 'https://')):
                response = requests.get(url)
                original_number = response.text.strip()
            else:
                return "Invalid URL"

        elif 'file' in request.files:
            # Read data from the uploaded file
            file = request.files['file']
            original_number = file.read().decode('utf-8').strip()

        elif 'text' in request.form and request.form['text'].strip():
            # Use data from the text input
            original_number = request.form['text']
        else:
            return "Invalid input"

        cleaned_numbers = clean_mobile_number(original_number)

    return render_template('index.html', cleaned_numbers=cleaned_numbers)

if __name__ == '__main__':
    app.run(debug=True)
