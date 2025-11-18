import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    # --- 基本設定 ---
    name_in_url = '協力に関する実験(同意と説明)' 
    players_per_group = None   # 1人実験（Bot対戦）のためグループなし
    num_rounds = 1             # 1回限りの実験

    # --- Botの挙動 ---
    # return_rate：何割のポイントをお返しするのか
    BOTS_INFO = {
        'A': {
            'name': 'レッドさん',
            'reputation_jp': '贈り物ゲームで相手に平均して約 52p の配分をした',
            'reputation_val': 52,
            'return_rate': 0.50,
        },
        'B': {
            'name': 'シアンさん',
            'reputation_jp': '贈り物ゲームで相手に平均して約 10p の配分をした',
            'reputation_val': 10,
            'return_rate': 0.10,
        },
        'C': {
            'name': 'グリーンさん',
            'reputation_jp': '（情報なし）',
            'reputation_val': None,
            'return_rate': 0.30,
        },
        'X': {
            'name': 'オレンジさん',
            'reputation_jp': '（情報なし）',
            'reputation_val': None,
            'return_rate': 0.30,
        },
    }

    # --- ゴシップ情報 ---
    # 協力条件群(A)・利己条件群(B)ともに、Xに関するゴシップ内容は同一
    GOSSIP_CONTENT = "オレンジさん は贈り物ゲームで相手に何も分けなかった"
    GOSSIP_VALUE = 0 # ゴシップで伝えられるXの分配額

    # --- お返しゲーム設定 ---
    # MULTIPLIER：投資額が何倍になって相手に届くのか
    INVESTMENT_MIN = 0
    INVESTMENT_MAX = 1000
    MULTIPLIER = 3

    # --- 練習ボットの挙動のランダム範囲 ---
    # [贈る側] 練習で、ボットが何%返礼するか (10%～90%)
    PRACTICE_BOT_RETURN_RATE_RANGE = (0.1, 0.9)
    # [返礼側] 練習で、ボットがいくら贈ってくるか (0pt～1000pt)
    PRACTICE_GIFT_FROM_BOT_RANGE = (0, 1000)

    # --- 報酬設定 ---
    # c(xxx)：int オブジェクトを Currency オブジェクトに変換
    FIXED_REWARD = c(300)
    POINT_TO_YEN_RATE = 0.1

    # 優先順位に応じたゲーム回数
    RANK_WEIGHTS = {1: 6, 2: 3, 3: 2, 4: 1}
    TOTAL_GAMES = sum(RANK_WEIGHTS.values())

class Player(BasePlayer):
    # --- 1. 同意 ---
    consent = models.BooleanField(
        label="実験の注意事項を確認し、参加に同意しますか？",
        widget=widgets.CheckboxInput,
        blank=True
        )
    
    #ページ内で決定されたBotの挙動を一時的に保存する
    practice_bot_return_rate = models.FloatField(initial=0.0)
    practice_bot_gift_amount = models.IntegerField(initial=0)

class Subsession(BaseSubsession):
    def creating_session(self):
        # 実験参加者に２つの条件をランダムに割り当てる
        for player in self.get_players():
            condition = random.choice(['cooperative', 'selfish'])
            player.participant.vars['condition'] = condition
            #player.condition = condition
            print(condition)

class Group(BaseGroup):
    pass