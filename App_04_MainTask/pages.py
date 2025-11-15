from otree.api import Page
from .models import Constants, Player
#from App_01_Intro.models import Constants as App01Constants

# ----------------------------------------
# ページ 15: 贈り物ゲーム待機 (演出)
# ----------------------------------------
class P15_Wait_Game1(Page):
    timeout_seconds = 3 # 3秒間 演出
    show_countdown = False

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 16: メッセージ作成ルール説明
# ----------------------------------------
class P16_MessageInstruction(Page):

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 17: メッセージ待機 (演出)
# ----------------------------------------
class P17_Wait_Message(Page):
    timeout_seconds = 3 # 3秒間 演出
    show_countdown = False
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 18: 評判とゴシップの開示 (★独立変数の操作★)
# ----------------------------------------
class P18_Reputation_Gossip(Page):
    
    def vars_for_template(self):
        # App_01で保存した'condition'変数を取得
        condition = self.participant.vars.get('condition')
        
        # Botの基本情報をHTMLに渡す
        bot_a_info = Constants.BOTS_INFO['A']
        bot_b_info = Constants.BOTS_INFO['B']
        bot_c_info = Constants.BOTS_INFO['C']
        
        # 条件分岐
        if condition == 'cooperative':
            gossiper_name = bot_a_info['name'] # レッドさん
            gossiper_reputation = bot_a_info['reputation_jp']
        else: # condition == 'selfish'
            gossiper_name = bot_b_info['name'] # シアンさん
            gossiper_reputation = bot_b_info['reputation_jp']
            
        return {
            'bot_A_name': bot_a_info['name'],
            'bot_A_reputation': bot_a_info['reputation_jp'],
            'bot_B_name': bot_b_info['name'],
            'bot_B_reputation': bot_b_info['reputation_jp'],
            'bot_C_name': bot_c_info['name'],
            'bot_C_reputation': bot_c_info['reputation_jp'],
            'gossiper_name': gossiper_name,
            'gossip_content': Constants.GOSSIP_CONTENT,
            'condition' : condition,
        }

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 19: 本番の意思決定 (★従属変数の取得★)
# ----------------------------------------
class P19_Decision(Page):
    form_model = 'player'
    # ★ models.py で定義した8つのフィールドすべてを保存対象にする
    form_fields = [
        'investment_A', 'investment_B', 'investment_C', 'investment_X',
        'rank_A', 'rank_B', 'rank_C', 'rank_X'
    ]

    def vars_for_template(self):
        # --- 1. 定数を辞書として取得 ---
        bots = Constants.BOTS_INFO 
        gossip_content_text = Constants.GOSSIP_CONTENT
        
        # --- 2. 条件分岐 (P18 と同じロジック) ---
        condition = self.participant.vars.get('condition') # デフォルト
        print(condition)
        
        if condition == 'cooperative':
            gossip_sender_name = bots['A']['name']
            gossip_sender_icon_class = 'icon-a'
        else: # 'selfish'
            gossip_sender_name = bots['B']['name']
            gossip_sender_icon_class = 'icon-b'
            
        # --- 3. HTMLテンプレートに変数を渡す ---
        return dict(
            rep_A = bots['A']['reputation_val'],
            rep_B = bots['B']['reputation_val'],
            gossip_sender_name = gossip_sender_name,
            gossip_sender_icon_class = gossip_sender_icon_class,
            gossip_content_text = gossip_content_text,
        )

    def error_message(self, values):
        # --- 4. サーバーサイドでの順位バリデーション ---
        # (models.pyのコメントにあった通り)
        ranks_input = [values['rank_A'], values['rank_B'], values['rank_C'], values['rank_X']]
        
        # 0 が含まれている (D&Dが未完了)
        if 0 in ranks_input:
            return 'すべてのパートナーを1位〜4位の枠に配置してください。'
            
        # 重複がある
        if len(set(ranks_input)) != 4:
            return 'パートナーの順位が重複しています。1位から4位までを重複なく割り当ててください。'
            
        # 1-4 の範囲外 (念のため)
        if not all(1 <= r <= 4 for r in ranks_input):
             return '順位は1位から4位の間で指定してください。'

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P15_Wait_Game1,
    P17_Wait_Message,
    P18_Reputation_Gossip,
    P19_Decision,
]