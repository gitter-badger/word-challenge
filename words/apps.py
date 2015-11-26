from django.apps import AppConfig
from django.contrib.auth.models import User


def _current_word(self):
    from .models import Draw

    # If the user has an undecided draw, return that one
    try:
        word = Draw.objects.get(user=self, accepted=None).word

        return word
    except Draw.DoesNotExist:
        pass

    # If the user has an accepted draw that is unfinished (ie. no work
    # is uploaded), return that one
    try:
        word = Draw.objects.get(user=self, accepted=True, work=None).word

        return word
    except Draw.DoesNotExist:
        pass

    return None

def _last_draw(self):
    from .models import Draw

    return Draw.objects.filter(user=self).order_by('-timestamp').first()

def _draw_word(self):
    if self.current_word() is not None:
        return self.current_word()

    from .models import Word, Draw

    # Find all words
    # Exclude all words that has an accepted draw for this user
    # Choose a random one
    # If there are no more words, return None
    word = Word.objects \
               .exclude(draws__accepted=True, draws__user=self) \
               .order_by('?') \
               .first()

    if word is None:
        return None

    Draw.objects.create(user=self, word=word, accepted=None)

    return word

class WordsConfig(AppConfig):
    name = 'words'

    def ready(self):
        User.current_word = _current_word
        User.draw_word = _draw_word
        User.last_draw = _last_draw
