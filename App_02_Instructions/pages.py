from otree.api import Page
from .models import Constants, Player

# ----------------------------------------
# ページ 7: 贈り物ゲーム説明
# ----------------------------------------
class P7_Game1_Instruction(Page):
    def is_displayed(self):
        # App_01で同意した人のみ表示
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 9: 作業ルーム2へ移動 (演出)
# ----------------------------------------
class P9_RoomTransition1(Page):
    timeout_seconds = 30 # 30秒間 演出
    show_countdown = False

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 10: タスク2（お返しゲーム）概要
# ----------------------------------------
class P10_Game2_Instruction(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 11: お返しゲーム詳細ルール
# ----------------------------------------
class P11_Game2_Rule(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 13: 優先順位ルール説明
# ----------------------------------------
class P13_PriorityRule(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None
