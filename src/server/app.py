from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
import random

app = Flask(__name__)
# CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/api/<src_lang>/words')
def get_words(src_lang):
    # query from db
    language = Language.query.filter_by(name=src_lang).first()
    words = Word.query.filter_by(language=language).order_by(
        Word.frequency.desc()).all()[:1000]

    # format dict

    words_data = []
    rank = 1

    for word in words:
        word_info = {
            'rank': rank,
            'text': word.text,
            'translations': [wt.text for wt in word.translations]
        }
        words_data.append(word_info)
        rank += 1

    response = {
        'data': {
            'count': len(words_data),
            'words': [wd for wd in words_data]
        }
    }

    return jsonify(response)


@app.route('/api/<src_lang>/sentences/<index>')
def get_sentences(src_lang, index):
    next_amount = 5
    start = int(index)
    language = Language.query.filter_by(name=src_lang).first()

    num_words = Word.query.count()
    limit = min(start + next_amount, num_words - start)

    words = Word.query.filter_by(language=language).order_by(
        Word.frequency.desc()).all()[start:limit]

    sentence_data = []

    for word in words:
        sentences = word.sentences
        translations = []

        for sentence in sentences:
            trans = TranslatedSentence.query.filter_by(
                sentence=sentence).first()
            translations.append(trans)

        sentence_info = {
            'text': [s.text for s in sentences],
            'translations': [tr.text for tr in translations]
        }
        sentence_data.append(sentence_info)

    response = {
        'data': {
            'words': [w.text for w in words],
            'sentences': [sd for sd in sentence_data]
        }
    }

    return jsonify(response)


@app.route('/api/test')
def hello():
    word = random.choice(Word.query.all())
    # word = Word.query.filter_by(text='de').first()
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
                'tatoeba_id': translation.tatoeba_id,
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
                'translations': [tr.text for tr in word.translations]
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
