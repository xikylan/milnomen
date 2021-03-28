import csv
from app import Sentence, TranslatedSentence, Language, Word, db

filename = 'es.tsv'


def parse_tsv(word, filename, lang):
    with open(filename, 'r', encoding='utf-8-sig') as file:
        tsv_file = csv.reader(file, delimiter='\t')
        for line in tsv_file:
            if word.text in line[1].split(' '):
                new_sentence = Sentence(
                    text=line[1], tatoeba_id=int(line[0]), word=word)
                db.session.add(new_sentence)
                db.session.commit()
                sentence = Sentence.query.filter_by(text=line[1]).first()

                new_trans_sentence = TranslatedSentence(
                    text=line[3], tatoeba_id=int(line[2]), sentence=sentence, language=lang)
                db.session.add(new_trans_sentence)
                db.session.commit()
