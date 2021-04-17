from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/api/languages')
def get_languages_json():
    languages = Language.query.all()

    response = {
        'data': {
            'count': len(languages),
            'languages': [language.name for language in languages]
        }
    }

    return jsonify(response)


@app.route('/api/<src_lang>/words')
def get_words_json(src_lang):
    # query words from db
    language = Language.query.filter_by(name=src_lang).first()
    words = Word.query.filter_by(language=language).order_by(
        Word.frequency.desc()).all()[:1000]

    # format words json
    words_data = format_words_data(words)

    # create response json
    response = {
        'data': {
            'count': len(words_data),
            'words': [wd for wd in words_data]
        }
    }

    return jsonify(response)


def format_words_data(words):
    words_data = []
    rank = 1
    # format each word in dictionary
    for word in words:
        word_info = {
            'rank': rank,
            'text': word.text,
            'translations': [wt.text for wt in word.translations]
        }
        words_data.append(word_info)
        rank += 1

    return words_data


@app.route('/api/<src_lang>/sentences/<start>')
def get_sentences_json(src_lang, start):
    # Query amount
    query_amount = 20

    limit = get_query_limit(int(start), query_amount)

    # query from db
    language = Language.query.filter_by(name=src_lang).first()
    words = Word.query.filter_by(language=language).order_by(
        Word.frequency.desc()).all()[int(start):limit]

    sentence_data = format_sentences_data(words)

    # generate sentences json
    response = {
        'data': {
            'words': [w.text for w in words],
            'sentences': [sd for sd in sentence_data]
        }
    }

    return jsonify(response)


def get_query_limit(start, query_amount):
    num_words = Word.query.count()

    # next n queries, or whatever is left
    next_query = start + query_amount
    leftover = num_words - start

    limit = min(next_query, leftover)

    return limit


def format_sentences_data(words):
    sentences_data = []

    for word in words:
        sentences = word.sentences
        translations = get_sentence_translations(sentences)

        # format sentence json
        sentence_info = {
            'text': [s.text for s in sentences],
            'translations': [tr.text for tr in translations]
        }
        sentences_data.append(sentence_info)

    return sentences_data


def get_sentence_translations(sentences):
    translations = []

    for sentence in sentences:
        trans = TranslatedSentence.query.filter_by(
            sentence=sentence).first()
        translations.append(trans)

    return translations


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
    translations = db.relationship(
        "TranslatedWord", back_populates="word", passive_deletes=True)

    def __repr__(self):
        return '<Word %r>' % self.text


class TranslatedWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey(
        'word.id', ondelete="CASCADE"), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey(
        'language.id'), nullable=False)

    language = db.relationship('Language', lazy=True)
    word = db.relationship("Word", back_populates="translations")

    def __repr__(self):
        return '<TranslatedWord %r>' % self.text


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10_000), nullable=False)
    tatoeba_id = db.Column(db.Integer, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)

    word = db.relationship('Word', backref='sentences', lazy=True)

    def __repr__(self):
        return '<Sentence %r...>' % self.text[:15]


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
