from django.test import TestCase
from .util import Token, parse


# Create your tests here.
class TestDeckParsing(TestCase):
    def singleLineWithoutSetOrX(self):
        string = "1 Fog"
        result = parse(string)
        self.assertListEqual(result, [Token(1, "Fog", None)])

    def singleLineWithXWithoutSet(self):
        string = "4x Juxtapose"
        result = parse(string)
        self.assertListEqual(result, [Token(4, "Juxtapose", None)])

    def singleLineWithSetWithoutX(self):
        string = "9 Boar Umbra (PC2)"
        result = parse(string)
        self.assertListEqual(result, [Token(9, "Boar Umbra", "PC2")])

    def singleLineComment(self):
        string = "Creatures"
        result = parse(string)
        self.assertListEqual(result, [])

    def singleLineWithCommentWithoutSet(self):
        string = "1 Scion of the Ur-Dragon # !Commander"
        result = parse(string)
        self.assertListEqual(result, [Token(1, "Scion of the Ur-Dragon", "")])

    def singleLineWithCommentAndSet(self):
        string = "10 Volrath's Stronghold (TPR) # Nope"
        result = parse(string)
        self.assertListEqual(result, [Token(10, "Volrath's Stronghold", "TPR")])
