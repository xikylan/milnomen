from app import Language, Word, Sentence, TranslatedWord, TranslatedSentence, db
from multiprocessing import Process
import csv
import translators as ts
import time


def main(words_file, sentences_file):
    # english = add_new_lang(code='en', name='english')
    # spanish = add_new_lang(code='es', name='spanish')
    spanish = Language.query.filter_by(code='es').first()
    english = Language.query.filter_by(code='en').first()

    clear_words()
    parse_words_txt(
        words_file=words_file,
        src_lang=spanish,
        dest_lang=english,
        max=1100
    )

    # spanish = Language.query.filter_by(code='es').first()
    # english = Language.query.filter_by(code='en').first()
    # clear_sentences()
    # parse_sentences_tsv(
    #     sentences_file=sentences_file,
    #     src_lang=spanish,
    #     dest_lang=english,
    #     max=120
    # )


def clear_words():
    print("Deleting", Word.query.delete(), "words")
    print("Deleting", TranslatedWord.query.delete(), "translated words")
    db.session.commit()


def clear_sentences():
    print("Deleting", Sentence.query.delete(), "sentences")
    print("Deleting", TranslatedSentence.query.delete(), "translated sentences")
    db.session.commit()


def add_new_lang(code, name):
    new_lang = Language(code=code, name=name)
    db.session.add(new_lang)
    db.session.commit()

    # return language query object
    return Language.query.filter_by(code=code).first()


def parse_words_txt(words_file, src_lang, dest_lang, max):
    start = time.time()

    # read <= max words into an array
    with open(words_file, 'r') as file:
        words_list = file.readlines()[:max]

    # start processes

    p1 = Process(target=convert_vocab, args=(
        words_list[:max//4],
        src_lang,
        dest_lang
    ))

    p2 = Process(target=convert_vocab, args=(
        words_list[max//4:max//2],
        src_lang,
        dest_lang
    ))

    p3 = Process(target=convert_vocab, args=(
        words_list[max//2:(max//4)*3],
        src_lang,
        dest_lang
    ))

    p4 = Process(target=convert_vocab, args=(
        words_list[(max//4)*3:],
        src_lang,
        dest_lang
    ))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    end = time.time()

    print("Parsing vocab took", (end-start) / 60, "minutes")
    print("Num words", len(words_list))


def convert_vocab(words_list, src_lang, dest_lang):
    for pair in words_list:
        word, frequency = pair.rstrip().split(' ')

        if word.isalpha():
            # add word and translations
            new_word = add_word(
                text=word, language=src_lang, freq=frequency
            )

            add_word_translations(
                word=new_word,
                src_lang=src_lang,
                dest_lang=dest_lang
            )


def add_word(text, language, freq):
    new_word = Word(text=text, language=language, frequency=freq)
    db.session.add(new_word)
    db.session.commit()

    return Word.query.filter_by(language=language, text=text).first()


def add_word_translations(word, src_lang, dest_lang):
    # get translations list
    translations = get_translations(word, src_lang)
    if not translations:
        remove_word(word)
        return

    did_add_word = False

    for trans in translations:

        if is_clean_trans(trans, word.text):

            # add new translation
            new_trans = TranslatedWord(
                word=word,
                language=dest_lang,
                text=trans.lower()
            )

            db.session.add(new_trans)
            db.session.commit()

            if not did_add_word:
                did_add_word = True

    # if no good translations, then delete bad word from db
    if not did_add_word:
        remove_word(word)


def get_translations(word, src_lang):
    try:
        # call translate api
        translations = ts.google(
            word.text,
            from_language=src_lang.code,
            is_detail_result=True,
            sleep_seconds=0.55
        )[1][0][0]

    except Exception as e:
        print('Word', word, 'encountered error while translating\n', e)
        return

    # avoid google translate api bad format
    if translations[-1] == src_lang.code:
        return

    return translations[-1][0][1]


def remove_word(word):
    db.session.delete(
        Word.query.filter_by(id=word.id).first()
    )
    db.session.commit()
    return True


def is_clean_trans(trans, word_text):
    if trans[-1] == '.':
        return False
    if trans.lower() == word_text:
        return False
    if not trans.replace(' ', '').replace("'", '').isalpha():
        return False

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
                        new_sentence = add_sentence(
                            sentence_pair=sentence_pair,
                            word=word
                        )

                        if new_sentence:
                            add_sentence_translation(
                                sentence_pair=sentence_pair,
                                dest_lang=dest_lang
                            )
                            # increment number of sentences only if new one is added
                            num_sentences += 1

                    except Exception as e:
                        print("id", sentence_pair[0], "trans_id", sentence_pair[2],
                              "encountered an error")
                        print(str(e))
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

        return True

    return False


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
    word = "".join(ch for ch in word if ch.isalpha()).lower()
    for token in arr:
        clean_token = token

        if not token.isalpha():
            clean_token = "".join(ch for ch in token if ch.isalpha())

        if clean_token.lower() == word:
            return True

    return False


if __name__ == '__main__':

    main('es.txt', 'es.tsv')
