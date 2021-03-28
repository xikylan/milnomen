from app import TranslatedWord, Language, Word, db
import translators as ts

spanish = Language.query.filter_by(name='spanish').first()

with open('top_es.txt', 'r') as file:
    for w in file:
        translations = ts.google(w, from_language='es', is_detail_result=True, sleep_seconds=0.05)[
            1][0][0][-1][0][1]
        for tr in translations:
            original = Word.query.filter_by(language=spanish, text=w).first()
            new_trans = TranslatedWord(
                word=original, language=spanish, text=tr)
            db.session.add(new_trans)
            db.session.commit()
