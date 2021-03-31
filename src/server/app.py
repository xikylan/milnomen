from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello():
    word = random.choice(Word.query.all())
    sentences = word.sentences
    language = Language.query.filter_by(id=word.language_id).first()

    sentence_data = []

    for s in sentences:
        translation = TranslatedSentence.query.filter_by(
            sentence_id=s.id).first()

        trans_lang = Language.query.filter_by(
            id=translation.language_id).first()

        s_dict = {
            'original': {
                'language': language.code,
                'tatoeba_id': s.tatoeba_id,
                'text': s.text,
            },
            'translation': {
                'language': trans_lang.code,
                'tatoeba_id': s.tatoeba_id,
                'text': translation.text,
            }}

        sentence_data.append(s_dict)

    sen_dict = {
        'data': {
            'count': len(sentences),
            'word': {
                'id': word.id,
                'text': word.text,
                'frequency': word.frequency,
                'language': language.code,
            },
            'sentences': [sd for sd in sentence_data]
        }
    }

    return sen_dict
    # all_words = Word.query.all()
    # words_dict = {}

    # for word in all_words:
    #     words_dict[word.frequency] = {
    #         'id': word.id,
    #         'text': word.text
    #     }

    # return words_dict


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Language %r>' % self.name


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
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
        return '<Sentence %r...>' % self.text[:15]


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
        return '<TranslatedSentence %r...>' % self.text[:15]


if __name__ == "__main__":
    app.run()
