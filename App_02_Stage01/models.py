from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'App_02_MainTask'
    players_per_group = None
    num_rounds = 1

    # 投資額の上限
    INVESTMENT_MAX = 1000
    # 倍率 (App_01に合わせて3倍とします)
    MULTIPLIER = 3

    # Botの設定
    # Aさん (シアン): 協力的 (贈与多め、返礼率高め)
    BOT_A = {
        'name': 'シアンさん',
        'icon_class': 'icon-b', # シアン色
        'gift_amount': 600,     # Page7で送ってくる額
        'return_rate': 0.5,     # Page8での返礼率
    }
    # Bさん (オレンジ): 利己的 (贈与少なめ、返礼率低め)
    BOT_B = {
        'name': 'オレンジさん',
        'icon_class': 'icon-x', # オレンジ色
        'gift_amount': 100,     # Page9で送ってくる額
        'return_rate': 0.1,     # Page10での返礼率
    }

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # --- Game 1 (vs Aさん) ---
    # Page 7 (Receiver): Botからの贈与を受け取り、返礼する
    g1_bot_gift = models.IntegerField(initial=0) # Botの贈与額
    g1_recieved = models.IntegerField(initial=0)
    g1_return = models.IntegerField(label="あなたのお返し額", min=0)
    
    # Page 8 (Sender): あなたが贈与し、Botが返礼する
    g1_gift = models.IntegerField(label="あなたの贈り物の額", min=0, max=Constants.INVESTMENT_MAX)
    g1_bot_recieved = models.IntegerField(initial=0) #Botの受取額
    g1_bot_return = models.IntegerField(initial=0) # Botの返礼額

    # --- Game 2 (vs Bさん) ---
    # Page 9 (Receiver)
    g2_bot_gift = models.IntegerField(initial=0) # Botの贈与額
    g2_recieved = models.IntegerField(initial=0)
    g2_return = models.IntegerField(label="あなたのお返し額", min=0)
    
    # Page 8 (Sender): あなたが贈与し、Botが返礼する
    g2_gift = models.IntegerField(label="あなたの贈り物の額", min=0, max=Constants.INVESTMENT_MAX)
    g2_bot_recieved = models.IntegerField(initial=0) #Botの受取額
    g2_bot_return = models.IntegerField(initial=0) # Botの返礼額