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

    # --- お返しゲーム設定 ---
    # MULTIPLIER：投資額が何倍になって相手に届くのか
    INVESTMENT_MIN = 0
    INVESTMENT_MAX = 1000
    MULTIPLIER = 3

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