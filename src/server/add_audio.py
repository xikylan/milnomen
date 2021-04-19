from gtts import gTTS as gtts
from app import Language, Word
from sys import argv
import time

code = argv[1]
lang = Language.query.filter_by(code=code).first()
words = Word.query.filter_by(language=lang).all()


def generate_audio(text):
    tts = gtts(text=text, lang=code, slow=False)
    assets_path = '../client/src/assets/audio/'
    file_name = text + ".mp3"
    folder_path = assets_path + code + "/" + file_name

    tts.save(folder_path)


for word in words:
    text = word.text
    start = time.time()
    generate_audio(text)
    end = time.time()
    print("Generation audio took", end-start, "seconds")
