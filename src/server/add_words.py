from app import Language, Word, TranslatedWord, db
import translators as ts
import time
import multiprocessing as mp
import math


def main(words_file):
    spanish = Language.query.filter_by(code='es').first()
    english = Language.query.filter_by(code='en').first()

    clear_words()
    parse_words_txt(
        words_file=words_file,
        src_lang=spanish,
        dest_lang=english,
        max=1100
    )


def clear_words():
    print("Deleting", Word.query.delete(), "words")
    print("Deleting", TranslatedWord.query.delete(), "translated words")
    db.session.commit()


def parse_words_txt(words_file, src_lang, dest_lang, max):
    # read <= max words into an array
    with open(words_file, 'r') as file:
        words_list = file.readlines()[:max]

    # start processes
    start = time.time()
    split_tasks(words_list, src_lang, dest_lang)
    end = time.time()

    print("Parsing vocab took", (end-start) / 60, "minutes")
    print("Num words", len(words_list))


def split_tasks(top_words, src_lang, dest_lang):
    num_workers = mp.cpu_count() - 1
    chunk_size = math.ceil(len(top_words) / num_workers)

    word_chunks = chunkify(top_words, chunk_size)
    jobs = []

    for chunk in word_chunks:
        process = mp.Process(target=convert_vocab,
                             args=(chunk, src_lang, dest_lang))
        process.start()
        jobs.append(process)
        time.sleep(1)

    for job in jobs:
        job.join()



def chunkify(word_list, increment):
    return (word_list[i:i+increment] for i in range(0, len(word_list), increment))


def convert_vocab(word_chunk, src_lang, dest_lang):
    for pair in word_chunk:
        word, frequency = pair.rstrip().split(' ')

        if word.isalpha():
            # add word and translations
            new_word = add_word(text=word, language=src_lang, freq=frequency)

            add_word_translations(
                word=new_word, src_lang=src_lang, dest_lang=dest_lang)


def add_word(text, language, freq):
    new_word = Word(text=text, language=language, frequency=freq)
    db.session.add(new_word)
    db.session.commit()

    return Word.query.filter_by(language=language, text=text).first()


def add_word_translations(word, src_lang, dest_lang):
    # get translations list
    translations = get_translations(word, src_lang)

    # remove word if no translations available
    if not translations:
        remove_word(word)
        return

    parse_translations(translations, word, dest_lang)


def parse_translations(translations, word, dest_lang):
    did_translate = False

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

            did_translate = True

    # if no good translations, then delete bad word from db
    if not did_translate:
        remove_word(word)


def get_translations(word, src_lang):
    try:
        # call translate api
        translations = ts.google(
            word.text,
            from_language=src_lang.code,
            is_detail_result=True,
            sleep_seconds=0.75
        )[1][0][0]

    except Exception as e:
        print('Word', word, 'encountered error while translating\n', e)
        quit()

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


if __name__ == '__main__':
    main('es.txt')
