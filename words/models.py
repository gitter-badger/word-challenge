from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import get_language

@python_2_unicode_compatible
class Word(models.Model):
    def translation(self, language):
        try:
            return self.translations.get(language=language)
        except WordTranslation.DoesNotExist:
            return None

    def __str__(self):
        try:
            return self.translations.get(language=get_language()).translation
        except WordTranslation.DoesNotExist:
            pass

        try:
            return self.translations \
                       .get(language=settings.LANGUAGE_CODE).translation
        except WordTranslation.DoesNotExist:
            pass

        return ""

@python_2_unicode_compatible
class WordTranslation(models.Model):
    word = models.ForeignKey(Word, related_name='translations')
    language = models.CharField(max_length=5, db_index=True)
    translation = models.CharField(max_length=100, null=True, blank=False)
    added_by = models.ForeignKey(User)
    added_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.translation is None or self.translation == '':
            raise ValidationError('translation must not be empty',
                                  code='translation-empty')

    def __str__(self):
        return self.translation

    class Meta:
        unique_together = (
            ('word', 'language'),
            ('language', 'translation'),
        )

class Draw(models.Model):
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word, related_name='draws')
    accepted = models.NullBooleanField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('timestamp',)

class Work(models.Model):
    draw = models.OneToOneField(Draw, related_name='work', primary_key=True)
    language = models.CharField(max_length=5, db_index=True)
