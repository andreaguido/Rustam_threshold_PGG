from otree.api import Currency as c, currency_range, SubmissionMustFail, Submission, expect
from . import pages
from ._builtin import Bot
from .models import Constants

import random

class PlayerBot(Bot):


    def play_round(self):

        if self.round_number==1:
            yield (pages.Introduction)
        else:
            yield (pages.Contribute, {'contribution': random.randint(0,10)})
            yield (pages.Results)