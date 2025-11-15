import random
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    # --- 基本設定 ---
    name_in_url = '協力に関する実験（事後アンケート）' 
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

    # --- 3. 事後アンケート---
    
    # DV1: Xの行動の推測
    dv1_x_estimation = models.IntegerField(
        label="あなたは実際、オレンジさんが贈り物ゲームでどれだけの額を相手に贈ったと思いますか？",
        verbose_name="Xの推測額",
        min=0, max=100
    )
    
    # DV4: ゴシップ発信者の意図推測 (7段階リッカート)
    dv4_gossiper_intent = models.IntegerField(
        label="メッセージを送った人は、メッセージによって相手を貶める意図をどの程度持っていたと思いますか？",
        verbose_name="ゴシップの意図",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, '全く持っていない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, '非常に強く持っている']]
        )
    
    # DV5-7: 意思決定プロセスの確認 (7段階リッカート)
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

    # --- 4. 操作チェック ---
    mc_A_recall = models.IntegerField(
        label="（操作チェック）レッドさん が贈り物ゲームで相手に配分した額として、いくらが提示されていましたか？",
        min=0
    )
    mc_B_recall = models.IntegerField(
        label="（操作チェック）シアンさん が贈り物ゲームで相手に配分した額として、いくらが提示されていましたか？",
        min=0
    )

    # --- 5. 共変量（一般的信頼尺度） ---
    gts1 = models.IntegerField(
        label="（一般的信頼尺度 項目1）",
        verbose_name="一般的信頼尺度 項目１",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, 'まったくそう思わない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, 'とてもそう思う']]
    )
    gts2 = models.IntegerField(
        label="（一般的信頼尺度 項目2）",
        verbose_name="一般的信頼尺度 項目２",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, 'まったくそう思わない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, 'とてもそう思う']]
    )
    gts3 = models.IntegerField(
        label="（一般的信頼尺度 項目3）",
        verbose_name="一般的信頼尺度 項目３",
        widget=widgets.RadioSelectHorizontal,
        choices=[[1, 'まったくそう思わない'], [2, ''], [3, ''], [4, 'どちらともいえない'], [5, ''], [6, ''], [7, 'とてもそう思う']]
    )

    # --- 6. デモグラフィック変数 ---
    age = models.IntegerField(
        label="あなたの年齢を半角数字で入力してください。",
        verbose_name="年齢",
        min=18
    )
    gender = models.StringField(
        label="あなたの性別を選択してください。",
        verbose_name="性別",
        choices=['男性', '女性', 'その他', '回答しない'],
        widget=widgets.RadioSelect
    )

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass # 1人実験のためGroupは使用しない