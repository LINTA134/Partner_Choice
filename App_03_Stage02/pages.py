from otree.api import Page
from .models import Constants, Player

# ----------------------------------------
# ページ 20: 待機・移動演出
# ----------------------------------------
class P20_Intro(Page):
    timeout_seconds = 3
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

class P21_ChooserLottery(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None
    
class P22_GossipInstruction(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None
    
class P23_MessegeWriting(Page):
    timeout_seconds = 45
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# [新規] ゴシップの提示
# ----------------------------------------
class P24_GossipPresentation(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

    def vars_for_template(self):
        condition = self.participant.vars.get('condition', 'cooperative') # デフォルトはcooperative

        if condition == 'cooperative':
            gossiper_id = 'A'
        else:
            gossiper_id = 'B'
        
        gossiper = Constants.BOTS_INFO[gossiper_id]

        return {
            'gossiper_name': gossiper['name'],
            'gossiper_icon': gossiper['icon_class'],
            'gossip_text': Constants.GOSSIP_TEXT
        }

# ----------------------------------------
# [新規] パートナー選択（ランキング）
# ----------------------------------------
class P25_PartnerSelection(Page):
    form_model = 'player'
    # 投資額フィールドを追加
    form_fields = [
        'rank_1_partner', 'rank_2_partner', 'rank_3_partner', 'rank_4_partner',
        'invest_A', 'invest_B', 'invest_C', 'invest_X'
    ]

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

    def vars_for_template(self):
        condition = self.participant.vars.get('condition', 'cooperative')
        gossiper_id = 'A' if condition == 'cooperative' else 'B'
        gossiper = Constants.BOTS_INFO[gossiper_id]

        return {
            'bots': Constants.BOTS_INFO,
            # 評判スコア (App_01の定数から取得)
            'rep_A': Constants.BOTS_INFO['A'].get('reputation_val', 52),
            'rep_B': Constants.BOTS_INFO['B'].get('reputation_val', 10),
            # ゴシップ情報
            'gossip_sender_name': gossiper['name'],
            'gossip_sender_icon_class': gossiper['icon_class'],
            'gossip_content_text': "贈り物ゲームで相手に何も分けなかったよ", # 文言は調整してください
        }

# ----------------------------------------
# ページ 21: 事後アンケート①（操作チェック）
# ----------------------------------------
class P21_ManipulationCheck(Page):
    form_model = 'player'
    form_fields = ['mc_A_recall', 'mc_B_recall']
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 22: 事後アンケート②（従属変数）
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

# ----------------------------------------
# ページ 23: 事後アンケート③（共変量）
# ----------------------------------------
class P23_Questionnaire_Covs(Page):
    form_model = 'player'
    form_fields = ['gts1', 'gts2', 'gts3', 'age', 'gender']
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ページ遷移順序
page_sequence = [
    P20_Intro,
    P21_ChooserLottery,
    P22_GossipInstruction,
    P23_MessegeWriting,
    P24_GossipPresentation,
    P25_PartnerSelection,
]