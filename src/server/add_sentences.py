from .app import Language, Word, Sentence, TranslatedSentence, db
import time
import math
import multiprocessing as mp
from sys import argv


def main():
    new_lang = Language.query.filter_by(name=argv[1]).first()
    english = Language.query.filter_by(code='en').first()

    sentences_file = "./texts/" + argv[1] + '.tsv'

    parse_sentences_tsv(
        sentences_file=sentences_file,
        src_lang=new_lang,
        dest_lang=english,
        max=20
    )


def parse_sentences_tsv(sentences_file, src_lang, dest_lang, max):
    top_words = Word.query.filter_by(
        language=src_lang).order_by(Word.frequency.desc()).all()

    # read tsv into list
    with open(sentences_file, 'r', encoding='utf-8-sig') as file:
        sentences = file.readlines()

    start = time.time()
    split_tasks(top_words, sentences, dest_lang, max)
    end = time.time()

    print("Parsing sentences took",
          (end - start) / 60, "minutes")


def split_tasks(top_words, sentences, dest_lang, max):
    num_workers = mp.cpu_count() - 1
    chunk_size = math.ceil(len(top_words) / num_workers)

    word_chunks = chunkify(top_words, chunk_size)
    jobs = []

    for chunk in word_chunks:
        process = mp.Process(target=convert_sentences,
                             args=(chunk, sentences, dest_lang, max))
        process.start()
        jobs.append(process)
        time.sleep(1)

    for job in jobs:
        job.join()


def chunkify(word_list, num):
    return (word_list[i:i+num] for i in range(0, len(word_list), num))


def convert_sentences(words_list, sentences, dest_lang, max):
    max_length = 7
    for word in words_list:
        num_sentences = 0

        for line in sentences:
            # exit if max sentences reached
            if num_sentences >= max:
                break

            # parse sentence + translations
            did_parse = parse_sentence(line, word, dest_lang, max_length)
            if did_parse:
                num_sentences += 1


def parse_sentence(line, word, dest_lang, max_length):
    # split sentence line
    orig_id, orig_text, trans_id, trans_text = line.split('\t')

    # clean sentence
    sentence = clean_sentence(orig_text.split(' '))

    # check if sentence is valid
    is_valid = len(sentence) <= max_length and word.text in sentence

    # if sentence of len 10 contains this top word
    if is_valid:
        # add sentence + translation
        did_add_new = add_sentence(
            id=orig_id,
            text=orig_text,
            word=word
        )

        if did_add_new:
            # add translation if add
            add_sentence_translation(
                id=orig_id,
                trans_id=trans_id,
                trans_sentence=trans_text,
                dest_lang=dest_lang
            )

            return True

    return False


def clean_sentence(sentence):
    for i in range(0, len(sentence)):
        sentence[i] = "".join(ch.lower() for ch in sentence[i] if ch.isalpha())

    return sentence


def add_sentence(id, text, word):
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


def add_sentence_translation(id, trans_id, trans_sentence, dest_lang):
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


if __name__ == '__main__':
    main()
