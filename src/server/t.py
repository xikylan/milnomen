
def contains_word(arr, word):
    word = "".join(ch for ch in word if ch.isalpha()).lower()
    for token in arr:
        clean_token = token

        if not token.isalpha():
            clean_token = "".join(ch for ch in token if ch.isalpha())

        if clean_token.lower() == word:
            return True

    return False


print(contains_word('Su hermano es aun más alto.'.split(), 'aun'))
