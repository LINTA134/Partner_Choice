from otree.api import Page
from .models import Constants, Player

# ----------------------------------------
# ページ 26: 実験の種明かしと最終同意
# ----------------------------------------
class P26_Debriefing_ReConsent(Page):
    
    # 最終同意のフォーム
    form_model = 'player'
    form_fields = ['re_consent']

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P26_Debriefing_ReConsent,
]