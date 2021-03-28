from app import Language, Word, Sentence, TranslatedWord, TranslatedSentence, db
import translators as ts

filename = 'top_es.txt'
code = 'es'
src = 'spanish'
dest = 'english'

english = Language(code='en', name=dest)

new_language = Language(code=code, name=src)
db.session.add(new_language)
db.session.commit()

language = Language.query.filter_by(name=src).first()

with open(filename, 'r') as file:
    for word in file:
        word = word.rstrip()

        # add new word
        new_word = Word(text=word, language=language)
        db.session.add(new_word)
        db.session.commit()

        # get translations list
        try:
            translations = ts.google(
                word, from_language=code, is_detail_result=True, sleep_seconds=0.075)[1][0][0][-1][0][-1]

            # add new TranslatedWord for each translation
            for trans in translations:
                original = Word.query.filter_by(
                    language=language, text=word).first()
                lang = Language.query.filter_by(name=dest).first()
                new_trans = TranslatedWord(
                    word=original, language=lang, text=trans.lower())
                db.session.add(new_trans)
                db.session.commit()
        except Exception as e:
            print('Word', word, 'encountered error while translating')
            print("Error:", e)
            continue
