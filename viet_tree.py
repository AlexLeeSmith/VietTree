from csv import DictReader
from pygtrie import StringTrie
from re import sub
from ViệtWord import ViệtWord
from random import choice

def cleanWord(word: str) -> str:
    ret = sub(r'\(.*\)', '', word)
    ret = sub(r'\.', '', ret)
    ret = sub('  ', ' ', ret)
    return ret.strip()

def buildWordTrie(fileName, syllableSeparator):
    wordTrie = StringTrie(separator=syllableSeparator)

    with open(fileName, newline='', encoding="utf-8") as csvFile:
        for row in DictReader(csvFile):
            vietStr = cleanWord(row['Vietnamese'])
            engStr = cleanWord(row['English'])
            for subVietWord in vietStr.split():
                vietWord = ViệtWord(subVietWord)
                key = syllableSeparator.join(vietWord.syllables + [vietWord.tone.name])
                if not wordTrie.has_key(key):
                    wordTrie[key] = {vietStr: [engStr]}
                elif vietStr not in wordTrie[key]:
                    wordTrie[key][vietStr] = [engStr]
                else:
                    wordTrie[key][vietStr].append(engStr)
    return wordTrie

def vietWordByPrefixAndTone(syllableSeparator, wordTrie):
    while i := input("Prefix: "):
        try:
            vietWord = ViệtWord(i)
            key = syllableSeparator.join(vietWord.syllables + [vietWord.tone.name])
            print(*wordTrie.items(key), '', sep='\n')
        except KeyError as e:
            print(f"No entries found for '{i}'.\n")

def vietWordByPrefix(syllableSeparator, wordTrie):
    while i := input("Prefix: "):
        try:
            vietWord = ViệtWord(i)
            key = syllableSeparator.join(vietWord.syllables)
            print(*wordTrie.items(key), '', sep='\n')
        except KeyError as e:
            print(f"No entries found for '{i}'.\n")

def randomWord(wordTrie):
    while True:
        key, v = choice(wordTrie.items())
        print(f'  {key}:', *zip(v.keys(), v.values()), sep='\n    - ')
        print()
        if i := input("Enter any key to exit: "):
            break

def main():
    fileName = 'wordlist.csv'
    syllableSeparator = '/'
    mainMenu = f"""
====================================================
    1. Random Vietnamese Words
    2. Search Vietnamese Words by Prefix
    3. Search Vietnamese Words by Prefix and Tone
=====================================================

    Select an Option: """
    wordTrie = buildWordTrie(fileName, syllableSeparator)

    while opt1 := input(mainMenu):
        print()

        match opt1:
            case '1':
                randomWord(wordTrie)
            case '2':
                vietWordByPrefix(syllableSeparator, wordTrie)
            case '3':
                vietWordByPrefixAndTone(syllableSeparator, wordTrie)
            case default:
                print(f"{default} is not an option.")

if __name__ == "__main__":
    main()