from otree.api import Page, WaitPage
from .models import Constants, Player

# ----------------------------------------
# ページ 1: 同意取得
# ----------------------------------------
class P1_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

def before_next_page(self, timeout_happened): 
        # timeout_happened が使われない場合でも定義は必要
        if not self.player.consent:
            self.participant.vars['consent_rejected'] = True

# ----------------------------------------
# ページ 2: マッチング待機 (演出)
# ----------------------------------------
class P2_MatchingWait(Page):
    # 5秒間、自動でこのページに留まらせる (演出のため)
    timeout_seconds = 3 
    show_countdown = False

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
# ページ 4: 役割の説明
# ----------------------------------------
class P4_RoleInstruction(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 5: 報酬の説明
# ----------------------------------------
class P5_RewardInstruction(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 6: 役割割り当て待機 (演出)
# ----------------------------------------
class P6_RoleAssignmentWait(Page):
    timeout_seconds = 3 # 5秒間 演出

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None