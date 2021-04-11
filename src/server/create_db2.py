
from app import Language, Word, Sentence, TranslatedWord, TranslatedSentence, db
import time
import translators as ts
import csv


def main(sentences_file):
    spanish = Language.query.filter_by(code='es').first()
    english = Language.query.filter_by(code='en').first()

    # clear database
    print("Deleting", Sentence.query.delete(), "sentences")
    print("Deleting", TranslatedSentence.query.delete(), "translations")
    db.session.commit()

    parse_sentences_tsv(
        sentences_file=sentences_file,
        src_lang=spanish,
        dest_lang=english,
        max=100
    )


def parse_sentences_tsv(sentences_file, src_lang, dest_lang, max):
    top_words = Word.query.filter_by(
        language=src_lang).order_by(Word.frequency.desc()).all()

    sentence_freq = {}
    for word in top_words:
        sentence_freq[word.text] = 0

    start = time.time()

    with open(sentences_file, 'r') as file:
        tsv_file = csv.reader(file, delimiter='\t')

        for line in tsv_file:
            sentences_text = line[1]
            text_split = sentences_text.split(' ')

            if len(text_split) < 10:

                # clean up sentence for comparison
                for i in range(0, len(text_split)):
                    text_split[i] = "".join(ch.lower()
                                            for ch in text_split[i] if ch.isalpha())

                for word in top_words:
                    if sentence_freq[word.text] >= max:
                        continue

                    if word in text_split:
                        try:
                            new_sentence = add_sentence(
                                sentence_pair=line,
                                word=word
                            )

                            if new_sentence:
                                add_sentence_translation(
                                    sentence_pair=line,
                                    dest_lang=dest_lang
                                )

                                sentence_freq[word.text] += 1

                        except Exception as e:
                            print("EXCEPTION")
                            print(e)
                            continue

    end = time.time()
    print("Parsing sentences took", (end - start) / 60, "minutes")


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


def clear_sentences():
    print("Deleting", Sentence.query.delete(), "sentences")
    print("Deleting", TranslatedSentence.query.delete(), "translated sentences")
    db.session.commit()


main('es.tsv')
