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

class WordsConfig(AppConfig):
    name = 'words'

    def ready(self):
        User.current_word = _current_word
