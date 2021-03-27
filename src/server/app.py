from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello World!'


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Language %r>' % self.name


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey(
        'language.id'), nullable=False)

    language = db.relationship('Language', backref='words', lazy=True)

    def __repr__(self):
        return '<Word %r>' % self.text


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10_000), nullable=False)
    tatoeba_id = db.Column(db.Integer, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)

    word = db.relationship('Word', backref='sentences', lazy=True)

    def __repr__(self):
        return '<Sentence %r>' % self.text[:15]


class TranslatedWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey(
        'word.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey(
        'language.id'), nullable=False)

    language = db.relationship('Language', lazy=True)
    word = db.relationship('Word', backref='translations', lazy=True)

    def __repr__(self):
        return '<TranslatedWord %r>' % self.text


class TranslatedSentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10_000), nullable=False)
    tatoeba_id = db.Column(db.Integer, nullable=False)
    sentence_id = db.Column(db.Integer, db.ForeignKey(
        'sentence.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey(
        'language.id'), nullable=False)

    language = db.relationship('Language', lazy=True)
    sentence = db.relationship('Sentence', backref='translations', lazy=True)

    def __repr__(self):
        return '<TranslatedSentence %r>' % self.text[:15]


if __name__ == "__main__":
    app.run()
