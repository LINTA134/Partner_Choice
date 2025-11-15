from otree.api import Page
from .models import Constants, Player

# ----------------------------------------
# ページ 20: 全体ルーム移動 (アンケート導入演出)
# ----------------------------------------
class P20_Wait_Game2(Page):
    timeout_seconds = 5 # 5秒間 演出

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 21: 事後アンケート①（操作チェック）
# ----------------------------------------
class P21_ManipulationCheck(Page):
    form_model = 'player'
    form_fields = ['mc_A_recall', 'mc_B_recall']
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 22: 事後アンケート②（従属変数アンケート）
# ----------------------------------------
class P22_Questionnaire_DVs(Page):
    form_model = 'player'
    form_fields = [
        'dv1_x_estimation',
        'dv4_gossiper_intent',
        'dv5_importance_content',
        'dv6_importance_reputation',
        'dv7_importance_distortion'
    ]

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

'''
    def error_message(self, values):
        for field in self.form_fields:
            if values[field] is None:
                return '未回答の質問項目があります。すべての質問にご回答ください。'
'''

# ----------------------------------------
# ページ 23: 事後アンケート③（共変量＆デモグラ）
# ----------------------------------------
class P23_Questionnaire_Covs(Page):
    form_model = 'player'
    form_fields = [
        'gts1', 'gts2', 'gts3', 'age', 'gender'
    ]

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

'''
    def error_message(self, values):
        # common.js のバリデーションでチェック済みだが、念のため
        for field in self.form_fields:
            if values[field] is None:
                return '未回答の質問項目があります。すべての質問にご回答ください。'
            # age のみ追加チェック
            if field == 'age' and (values['age'] < 18 or values['age'] > 99):
                 return '年齢は18歳から99歳の間で入力してください。'
'''