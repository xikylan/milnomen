from app import Language, Word, Sentence, TranslatedSentence, db
import time
import multiprocessing as mp


def main(sentences_file):
    spanish = Language.query.filter_by(code='es').first()
    english = Language.query.filter_by(code='en').first()

    clear_sentences()
    parse_sentences_tsv(
        sentences_file=sentences_file,
        src_lang=spanish,
        dest_lang=english,
        max=20
    )


def clear_sentences():
    print("Deleting", Sentence.query.delete(), "sentences")
    print("Deleting", TranslatedSentence.query.delete(), "translated sentences")
    db.session.commit()


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
    num_cores = mp.cpu_count()
    list_chunks = chunkify(top_words, num_cores)

    # Split processing to utilize all cores
    pool = mp.Pool(num_cores)
    for chunk in list_chunks:
        pool.apply_async(convert_sentences, args=(
            chunk,
            sentences,
            dest_lang,
            max
        ))

    pool.close()
    pool.join()


def chunkify(word_list, num):
    return (word_list[i:i+num] for i in range(0, len(word_list), num))


def convert_sentences(words_list, sentences, dest_lang, max):
    for word in words_list:
        num_sentences = 0

        for line in sentences:
            # exit if max sentences reached
            if num_sentences >= max:
                break

            orig_id, orig_text, trans_id, trans_text = line.split('\t')

            # clean sentence
            sentence = clean_sentence(orig_text.split(' '))

            # if sentence of len 10 contains this top word
            if len(sentence) <= 10 and word.text in sentence:
                try:
                    # add sentence + translation
                    new_sentence = add_sentence(
                        id=orig_id,
                        text=orig_text,
                        word=word
                    )

                    if new_sentence:
                        add_sentence_translation(
                            id=orig_id,
                            trans_id=trans_id,
                            trans_sentence=trans_text,
                            dest_lang=dest_lang
                        )
                        # increment number of sentences only if new one is added
                        num_sentences += 1

                except Exception as e:
                    print(str(e))


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
    main('es.tsv')
