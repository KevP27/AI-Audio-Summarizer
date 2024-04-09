from flask import Flask, render_template, request, redirect, url_for
from flask import send_file, jsonify
from summarizer import audio_summarizer
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
from answerQuestion import answerQ
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aiaudiosummarizersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio_files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class uploadFile(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = uploadFile()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        audio_file = AudioFile(filename=filename)
        db.session.add(audio_file)
        db.session.commit()
        file_data = BytesIO()
        file_data.write(file.read())
        audio_file.data = file_data.getvalue()
        db.session.commit()
        return jsonify({'filename': filename})
    return render_template('index.html', form=form)

@app.route('/summarize', methods=['POST'])
def summarize():
    filename = request.form.get('filename')
    audio_file = AudioFile.query.filter_by(filename=filename).first()
    if audio_file:
        summary = audio_summarizer(BytesIO(audio_file.data))
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