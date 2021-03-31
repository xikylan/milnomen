from app import Language, Word, Sentence, TranslatedWord, TranslatedSentence, db
import time
import translators as ts
import csv


def main(words_file, sentences_file):
    # english = add_new_lang(code='en', name='english')
    # spanish = add_new_lang(code='es', name='spanish')
    # parse_words_txt(
    #     words_file=words_file,
    #     src_lang=spanish,
    #     dest_lang=english,
    #     max=1000
    # )
    spanish = Language.query.filter_by(code='es').first()
    english = Language.query.filter_by(code='en').first()
    parse_sentences_tsv(
        sentences_file=sentences_file,
        src_lang=spanish,
        dest_lang=english,
        max=100
    )


def add_new_lang(code, name):
    new_lang = Language(code=code, name=name)
    db.session.add(new_lang)
    db.session.commit()

    # return language query object
    return Language.query.filter_by(code=code).first()


def parse_words_txt(words_file, src_lang, dest_lang, max):
    count = 0
    start = time.time()
    with open(words_file, 'r') as file:
        for line in file:
            if count >= max:
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
    end = time.time()
    print("Parsing words took", end - start, "seconds")
    return True


def add_word(word, language, freq):
    new_word = Word(text=word, language=language, frequency=freq)
    db.session.add(new_word)
    db.session.commit()
    return True


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

    return True


def parse_sentences_tsv(sentences_file, src_lang, dest_lang, max):
    top_words = Word.query.filter_by(
        language=src_lang).order_by(Word.frequency.desc()).all()

    start = time.time()

    with open(sentences_file, 'r') as file:
        tsv = csv.reader(file, delimiter='\t')

        for word in top_words:
            # goto top of file
            file.seek(0)
            num_sentences = 0

            for sentence_pair in tsv:
                # exit if max sentences reached
                if num_sentences >= max:
                    break

                # grab sentence text
                sentence_text = sentence_pair[1]
                text_split = sentence_text.split(' ')

                # if sentence of len 10 contains this top word
                if len(text_split) <= 10 and contains_word(text_split, word.text):
                    try:

                        # add sentence + translation
                        add_sentence(
                            sentence_pair=sentence_pair,
                            word=word
                        )

                        add_sentence_translation(
                            sentence_pair=sentence_pair,
                            dest_lang=dest_lang
                        )

                        # increment number of sentences
                        num_sentences += 1

                    except Exception as e:
                        print("id", sentence_pair[0], "trans_id", sentence_pair[2],
                              "encountered an error")
                        print(e)
                        continue

        end = time.time()
        print("Parsing sentences took",
              (end - start) / 60, "minutes")


def add_sentence(sentence_pair, word):
    id = sentence_pair[0]
    text = sentence_pair[1]

    # check if sentence already exists in db
    exists = Sentence.query.filter_by(tatoeba_id=id).first()

    if not exists:
        # add new sentence
        new_sentence = Sentence(
            text=text,
            tatoeba_id=id,
            word=word
        )
        db.session.add(new_sentence)
        db.session.commit()

    else:
        print("Sentence '", exists.text[:15], "...' already exists")


def add_sentence_translation(sentence_pair, dest_lang):
    id = sentence_pair[0]
    trans_id = sentence_pair[2]
    trans_sentence = sentence_pair[3]

    # add translated sentence
    original_sentence = Sentence.query.filter_by(
        tatoeba_id=id).first()

    new_translated_sentence = TranslatedSentence(
        text=trans_sentence,
        tatoeba_id=trans_id,
        language=dest_lang,
        sentence=original_sentence
    )
    db.session.add(new_translated_sentence)
    db.session.commit()


def contains_word(arr, word):
    for token in arr:
        if token == word:
            return True
    return False


main('es.txt', 'es.tsv')
