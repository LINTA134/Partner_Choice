from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'App_03_Stage02' # URL名を修正
    players_per_group = None
    num_rounds = 1

    # App_01に合わせてボット情報を再定義（または参照）
    BOTS_INFO = {
        'A': {'name': 'シアンさん', 'icon_class': 'icon-b'},
        'B': {'name': 'オレンジさん', 'icon_class': 'icon-x'},
        'C': {'name': 'グリーンさん', 'icon_class': 'icon-c'},
        'X': {'name': 'レッドさん', 'icon_class': 'icon-a'},
    }
    
    # ゴシップ内容
    GOSSIP_TEXT = "レッドさんは、あなたの贈り物に対して 5% の返礼を行うと予想します。"

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # --- パートナー選択（ランキング）の結果 ---
    # 誰を1位～4位に選んだか（'A', 'B', 'C', 'X' のいずれかが入る）
    rank_1_partner = models.StringField()
    rank_2_partner = models.StringField()
    rank_3_partner = models.StringField()
    rank_4_partner = models.StringField()

    invest_A = models.IntegerField(min=0, max=100, initial=50)
    invest_B = models.IntegerField(min=0, max=100, initial=50)
    invest_C = models.IntegerField(min=0, max=100, initial=50)
    invest_X = models.IntegerField(min=0, max=100, initial=50)

    # --- 以下、既存のアンケート項目 ---
    # DV1: Xの行動の推測
    dv1_x_estimation = models.IntegerField(
        label="あなたは実際、オレンジさんが贈り物ゲームでどれだけの額を相手に贈ったと思いますか？",
        verbose_name="Xの推測額",
        min=0, max=100
    )
    
    # DV4: ゴシップ発信者の意図推測
    dv4_gossiper_intent = models.IntegerField(
        label="メッセージを送った人は、メッセージによって相手を貶める意図をどの程度持っていたと思いますか？",
        verbose_name="ゴシップの意図",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, '全く持っていない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, '非常に強く持っている']]
    )
    
    # DV5-7: 意思決定プロセスの確認
    dv5_importance_content = models.IntegerField(
        label="あなたは意思決定の際に「メッセージの内容」をどの程度重視しましたか？",
        verbose_name="ゴシップの重要視",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, '全く重視しなかった'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, '非常に重視した']]
    )
    dv6_importance_reputation = models.IntegerField(
        label="あなたは意思決定の際に「メッセージを送った人がどれだけ相手にポイントを送ったのか」をどの程度重視しましたか？",
        verbose_name="ゴシップ発信者の評判の重要視",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, '全く重視しなかった'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, '非常に重視した']]
    )
    dv7_importance_distortion = models.IntegerField(
        label="あなたは意思決定の際に「ゴシップの内容が発信者によって歪められている可能性」をどの程度重視しましたか？",
        verbose_name="ゴシップ発信者の意図の重要視",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, '全く重視しなかった'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, '非常に重視した']]
    )

    # --- 操作チェック ---
    mc_A_recall = models.IntegerField(
        label="（操作チェック）レッドさん が贈り物ゲームで相手に配分した額として、いくらが提示されていましたか？",
        min=0
    )
    mc_B_recall = models.IntegerField(
        label="（操作チェック）シアンさん が贈り物ゲームで相手に配分した額として、いくらが提示されていましたか？",
        min=0
    )

    # --- 共変量・デモグラ ---
    gts1 = models.IntegerField(
        label="ほとんどの人は基本的に正直である",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, 'まったくそう思わない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, 'とてもそう思う']]
    )
    gts2 = models.IntegerField(
        label="人を信用しすぎると、利用されることが多い",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, 'まったくそう思わない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, 'とてもそう思う']]
    )
    gts3 = models.IntegerField(
        label="ほとんどの人は基本的に善意に満ちている",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, 'まったくそう思わない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, 'とてもそう思う']]
    )

    age = models.IntegerField(label="あなたの年齢", min=18)
    gender = models.StringField(
        label="あなたの性別",
        choices=['男性', '女性', 'その他', '回答しない'],
        widget=widgets.RadioSelect
    )