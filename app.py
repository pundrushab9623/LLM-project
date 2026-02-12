from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from nlp_engine import extract_entities, get_semantic_score
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///candidates.db'
db = SQLAlchemy(app)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Float)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        jd = request.form['jd']
        file = request.files['resume']
        
        # In a real app, use PyPDF2 to extract text from file
        resume_text = "Sample extracted text from PDF" 
        
        score = get_semantic_score(resume_text, jd)
        entities = extract_entities(resume_text)
        
        new_candidate = Candidate(name=entities['name'] or "Unknown", score=score)
        db.session.add(new_candidate)
        db.session.commit()
        
        return f"Candidate {new_candidate.name} scored {score:.2f}%"
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
