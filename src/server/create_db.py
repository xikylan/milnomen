from app import Language, Word, Sentence, TranslatedWord, TranslatedSentence, db
import translators as ts
import csv

filename = 'top_es.txt'
code = 'es'
src = 'spanish'
dest = 'english'


def main(words_file):
    english = add_new_lang(code='en', name='english')
    spanish = add_new_lang(code='es', name='spanish')
    parse_words_txt(
        words_file=words_file,
        src_lang=spanish,
        dest_lang=english,
        amount=1000
    )


def add_new_lang(code, name):
    new_lang = Language(code=code, name=name)
    db.session.add(new_lang)
    db.session.commit()

    # return language query object
    return Language.query.filter_by(code=code).first()


def parse_words_txt(words_file, src_lang, dest_lang, amount):
    count = 0
    with open(words_file, 'r') as file:
        for line in file:
            if count >= amount:
                return True

            split = line.split(' ')
            word = split[0]
            frequency = split[1]

            # add word and translations
            add_word(word=word, language=src_lang, freq=frequency)
            add_word_translations(
                word=word,
                src_lang=src_lang,
                dest_lang=dest_lang
            )

            count += 1


def add_word(word, language, freq):
    new_word = Word(text=word, language=language, frequency=freq)
    db.session.add(new_word)
    db.session.commit()


def add_word_translations(word, src_lang, dest_lang):
    # get translations list
    try:
        # call translate api
        translations = ts.google(
            word,
            from_language=src_lang.code,
            is_detail_result=True,
            sleep_seconds=0.075
        )[1][0][0][-1][0][-1]

        # add new TranslatedWord for each translation
        for trans in translations:
            # get original word
            original = Word.query.filter_by(
                text=word,
                language=src_lang
            ).first()
            # create TranslatedWord
            new_trans = TranslatedWord(
                word=original,
                language=dest_lang,
                text=trans.lower()
            )

            db.session.add(new_trans)
            db.session.commit()
    except Exception as e:
        print('Word', word, 'encountered error while translating')
        print("Error:", e)


main('es.txt')
