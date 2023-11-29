from enum import Enum
from pygtrie import CharTrie
from typing import List
from unicodedata import name, lookup

class ViệtWord:
    class Tone(Enum):
        # NGANG = None
        # SẮC = '0301'
        # HUYỀN = '0300'
        # HỎI = '0309'
        # NGÃ = '0303'
        # NẶNG = '0323'
        SẮC = 'ACUTE'
        HUYỀN = 'GRAVE'
        HỎI = 'HOOK ABOVE'
        NGÃ = 'TILDE'
        NẶNG = 'DOT BELOW'
        NGANG = 'NONE'

    alphabet = {'a','â','ă','b','c','d','đ','e','ê','g','h','i','k','l','m','n','o','ô','ơ','p','q','r','s','t','u','ư','v','x','y'}
    diphthongs = {'gh','gi','kh','ng','nh','ph','qu','th','tr','ch','ai','ay','ây','ao','au','âu','eo','ia','iê','iu','oa','oă','oe','oi','ôi','ơi','ua','ưa','uô','ươ','ui','uâ','uê','uơ','uy','ưi','ưu'}
    triphthongs = {'ngh','iêu','oai','uôi','uyê','ươi'}

    vowelTrie = CharTrie.fromkeys(alphabet | diphthongs | triphthongs)

    def __init__(self, withTone: str) -> None:
        self.tone: ViệtWord.Tone = ViệtWord.Tone.NGANG
        self.withTone: str = withTone
        self.withoutTone: str = self.strip_tone(withTone)
        self.syllables: List[str] = self.splitSyllables(self.withoutTone)

    def __str__(self):
        return f"{self.withTone} = {self.syllables} + {self.tone}"

    def strip_tone(self, word: str) -> str:
        strippedWord = ''
        for letter in word:
            letterName = name(letter)
            for tone in ViệtWord.Tone:
                if tone.value in letterName:
                    self.tone = tone
                    letterName = letterName.removesuffix(tone.value).removesuffix('AND ').removesuffix('WITH ').strip()
                    break
            strippedWord += lookup(letterName)
        return strippedWord

    def splitSyllables(self, word: str) -> List[str]:
        """Splits a single vietnamese word into its component syllables."""
        syllables = []
        remaining = str(word)
        while remaining:
            syllables.append(ViệtWord.vowelTrie.longest_prefix(remaining).key)
            remaining = remaining.replace(syllables[-1],"",1)
        return syllables
