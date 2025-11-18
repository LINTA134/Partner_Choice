import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    # --- 基本設定 ---
    name_in_url = '協力に関する実験（本番②）' 
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
    INVESTMENT_MAX = 100
    MULTIPLIER = 2

    # --- 報酬設定 ---
    # c(xxx)：int オブジェクトを Currency オブジェクトに変換
    FIXED_REWARD = c(300)
    POINT_TO_YEN_RATE = 0.1

    # 優先順位に応じたゲーム回数
    RANK_WEIGHTS = {1: 6, 2: 3, 3: 2, 4: 1}
    TOTAL_GAMES = sum(RANK_WEIGHTS.values())

class Player(BasePlayer):
    
    # --- 2. 意思決定 ---
    investment_A = models.IntegerField(label="レッドさんへの贈り物", verbose_name="Aへの投資額", min=Constants.INVESTMENT_MIN, max=Constants.INVESTMENT_MAX)
    investment_B = models.IntegerField(label="シアンさんへの贈り物", verbose_name="Bへの投資額", min=Constants.INVESTMENT_MIN, max=Constants.INVESTMENT_MAX)
    investment_C = models.IntegerField(label="グリーンさんへの贈り物", verbose_name="Cへの投資額", min=Constants.INVESTMENT_MIN, max=Constants.INVESTMENT_MAX)
    investment_X = models.IntegerField(label="オレンジさんへの贈り物", verbose_name="Xへの投資額", min=Constants.INVESTMENT_MIN, max=Constants.INVESTMENT_MAX)
    
    # パートナー優先順位 (1〜4位)
    # ※「重複なし」のバリデーションは pages.py の error_message で行います
    rank_A = models.IntegerField(label="レッドさんの順位", verbose_name="Aの順位", min=1, max=4)
    rank_B = models.IntegerField(label="シアンさんの順位", verbose_name="Bの順位", min=1, max=4)
    rank_C = models.IntegerField(label="グリーンさんの順位", verbose_name="Cの順位", min=1, max=4)
    rank_X = models.IntegerField(label="オレンジさんの順位", verbose_name="Xの順位", min=1, max=4)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass # 1人実験のためGroupは使用しない