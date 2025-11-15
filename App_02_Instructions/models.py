import random
from otree.api import *
"""
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
"""

class Constants(BaseConstants):
    # --- 基本設定 ---
    name_in_url = '協力に関する実験（ルール説明）' 
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
    FIXED_REWARD = Currency(300)
    POINT_TO_YEN_RATE = 0.1

    # 優先順位に応じたゲーム回数
    RANK_WEIGHTS = {1: 6, 2: 3, 3: 2, 4: 1}
    TOTAL_GAMES = sum(RANK_WEIGHTS.values())

class Player(BasePlayer):
    pass

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass # 1人実験のためGroupは使用しない