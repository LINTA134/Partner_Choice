from otree.api import Page
from .models import Constants, Player
import math
import random

# ----------------------------------------
# ページ 1: 同意取得
# ----------------------------------------
class P1_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']
    
    def before_next_page(self): 
        # timeout_happened が使われない場合でも定義は必要
        if not self.player.consent:
            self.participant.vars['consent_rejected'] = True

# ----------------------------------------
# ページ 2: マッチング待機 (演出)
# ----------------------------------------
class P2_MatchingWait(Page):
    # 5秒間、自動でこのページに留まらせる (演出のため)
    timeout_seconds = 3
    timer_text = "相手が決定するまでお待ちください"

    # 同意した人だけ表示 (同意しなかった人はこのAppの以降のページをすべてスキップ)
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 3: グループ形成 (演出)
# ----------------------------------------
class P3_GroupFormation(Page):

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 4: 実験の概要
# ----------------------------------------
class P4_ExperimentOverview(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 5: お返しゲームのルール説明
# ----------------------------------------
class P5_GameInstruction(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 6: お返しゲームの練習
# ----------------------------------------
class P6_GamePractice(Page):  
    def vars_for_template(self):
        return {
            'multiplier_percent': int(Constants.MULTIPLIER * 100)
        }
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P1_Consent,
    P2_MatchingWait,
    P3_GroupFormation,
    P4_ExperimentOverview,
    P5_GameInstruction,
    P6_GamePractice
]