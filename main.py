from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import send_file, jsonify
from summarizer import audio_summarizer
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
from answerQuestion import answerQ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aiaudiosummarizersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class uploadFile(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
            if file:
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)

                return jsonify({'filename': filename})

    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    filename = request.form.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        summary = audio_summarizer(file_path) 
        return jsonify({'summary': summary})
    else:
        return jsonify({'error': 'File not found'}), 404
    
@app.route('/answer_question', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get('question')
    if question:
        answer = answerQ(question)
        return answer
    else:
        return jsonify({'error': 'No question provided'}), 400

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)