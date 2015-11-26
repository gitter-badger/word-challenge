# -*- coding: utf-8
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.dateparse import parse_duration
from django.utils.translation import activate
from django.test import TestCase

from .models import Word, WordTranslation, Draw, Work

class WordTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='test')
        self.word1 = Word.objects.create()
        self.translation1 = WordTranslation.objects.create(
            word=self.word1,
            language='en-us',
            translation='color',
            added_by=user)
        self.translation2 = WordTranslation.objects.create(
            word=self.word1,
            language='en-gb',
            translation='colour',
            added_by=user)
        self.translation3 = WordTranslation.objects.create(
            word=self.word1,
            language='hu-hu',
            translation='szín',
            added_by=user)

    def test_word_str(self):
        with self.settings(LANGUAGE_CODE='en-us'):
            self.assertEquals("color", self.word1.__str__())

        with self.settings(LANGUAGE_CODE='en-gb'):
            self.assertEquals('colour', self.word1.__str__())

        activate('hu-hu')
        self.assertEquals('szín', self.word1.__str__())

        with self.settings(LANGUAGE_CODE='es-es'):
            activate('is-is')
            self.assertEquals('', self.word1.__str__())

    def test_word_translation(self):
        self.assertEquals('color', self.word1.translation('en-us').translation)
        self.assertEquals('colour', self.word1.translation('en-gb').translation)
        self.assertIsNone(self.word1.translation('is-is'))

    def test_translation_validation(self):
        word = WordTranslation()

        with self.assertRaises(ValidationError) as ctx:
            word.clean()

        self.assertEquals('translation-empty', ctx.exception.code)

    def test_translation_str(self):
        self.assertEquals('color', self.translation1.__str__())

class DrawTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.word = Word.objects.create()

    def test_current_word(self):
        self.assertIsNone(self.user.current_word())

        draw = Draw.objects.create(user=self.user,
                                   word=self.word,
                                   accepted=None)
        self.assertEquals(self.word, self.user.current_word())

        draw.accepted = True
        draw.save()
        self.assertEquals(self.word, self.user.current_word())

    def test_draw_word(self):
        draw = Draw.objects.create(user=self.user,
                            word=self.word,
                            accepted=None)
        self.assertEquals(self.word, self.user.draw_word())
        draw.accepted = True
        duration = parse_duration(settings.DRAW_TIME)
        draw.timestamp -= 2 * duration
        draw.save()
        Work.objects.create(draw=draw)

        word2 = Word.objects.create()
        self.assertEquals(word2, self.user.draw_word())

        draw = Draw.objects.get(user=self.user, word=word2)
        self.assertIsNotNone(draw)
        self.assertIsNone(draw.accepted)

        draw.accepted = True
        draw.timestamp -= 2 * duration
        draw.save()
        Work.objects.create(draw=draw)

        self.assertIsNone(self.user.draw_word())

    def test_last_draw(self):
        draw = Draw.objects.create(
            user=self.user,
            word=self.word,
            accepted=True,
            timestamp=timezone.now() - timedelta(days=1))
        Work.objects.create(draw=draw)
        word = Word.objects.create()
        draw = Draw.objects.create(user=self.user,
                            word=word,
                            accepted=True)
        Work.objects.create(draw=draw)

        self.assertEquals(word, self.user.last_draw().word)

    def test_draw_per_day(self):
        draw = Draw.objects.create(user=self.user,
                                   word=self.word,
                                   accepted=True)
        Work.objects.create(draw=draw)
        Word.objects.create()

        self.assertEquals(self.word, self.user.draw_word())
