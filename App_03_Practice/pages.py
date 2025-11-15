from otree.api import Page
from .models import Constants, Player


class P14_MainPractice(Page):

    def is_displayed(self):
        # App_01で同意した人のみ表示
        return self.participant.vars.get('consent_rejected') is None

