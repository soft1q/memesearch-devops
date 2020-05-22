from django.test import TestCase
from memes.models import Memes
from memes.ocr_pipeline.recognition import getTextFromImage

class MemeTestCase(TestCase):
    def test_meme_save(self):
        meme = Memes(textDescription='', imageDescription='')
        meme.image = 'tests/test.jpg'
        meme.save()

class MarkupTestCase(TestCase):
    def test_markup(self):
        result = getTextFromImage('tests/test.jpg')
        print('Successful markup!')
        print('Test image text is', result)

