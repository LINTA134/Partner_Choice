from otree.api import Page
from .models import Constants, Player
import math
import random

# ----------------------------------------
# ページ 1: 同意取得
# ----------------------------------------
class P1_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']
    
    def before_next_page(self): 
        # timeout_happened が使われない場合でも定義は必要
        if not self.player.consent:
            self.participant.vars['consent_rejected'] = True

# ----------------------------------------
# ページ 2: マッチング待機 (演出)
# ----------------------------------------
class P2_MatchingWait(Page):
    # 5秒間、自動でこのページに留まらせる (演出のため)
    timeout_seconds = 3 
    show_countdown = False

    # 同意した人だけ表示 (同意しなかった人はこのAppの以降のページをすべてスキップ)
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 3: グループ形成 (演出)
# ----------------------------------------
class P3_GroupFormation(Page):

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 4: 実験の概要
# ----------------------------------------
class P4_ExperimentOverview(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 5: お返しゲームのルール説明
# ----------------------------------------
class P5_GameInstruction(Page):
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ 6: お返しゲームの練習
# ----------------------------------------
class P6_GamePractice(Page):

    # ----------------------------------------
    # 練習1 (贈る側): Botの返礼率をランダムに決める
    # ----------------------------------------
    def live_determine_bot_giver(self, payload):
        player = self.player
        min_r, max_r = Constants.PRACTICE_BOT_RETURN_RATE_RANGE
        
        # 1. ランダムな返礼率を決定 (例: 0.1 ～ 0.9 の間で、小数点1桁)
        rate = round(random.uniform(min_r, max_r), 1)
        
        # 2. Playerモデルに一時保存
        player.practice_bot_return_rate = rate
        
        # 3. JSに結果を返す
        return {
            player.id_in_group: {
                'type': 'bot_giver_determined',
                'rate_percent': int(rate * 100) # (例: 40)
            }
        }

    # ----------------------------------------
    # 練習1 (贈る側): シミュレーション計算
    # ----------------------------------------
    def live_calculate_giver(self, payload):
        player = self.player
        try:
            investment = int(payload['investment'])
            if not 0 <= investment <= Constants.INVESTMENT_MAX:
                raise ValueError("Investment out of range")

            # Playerに保存された返礼率を読み込む
            rate = player.practice_bot_return_rate 
            if rate == 0.0: # 安全装置
                raise ValueError("Bot behavior not determined")

            multiplier = Constants.MULTIPLIER
            max_invest = Constants.INVESTMENT_MAX

            your_keep = max_invest - investment
            received_by_bot = investment * multiplier
            bot_return_amount = math.floor(received_by_bot * rate)
            final_payoff = your_keep + bot_return_amount
            
            return {
                player.id_in_group: {
                    'type': 'giver_result',
                    'investment': investment,
                    'your_keep': your_keep,
                    'received_by_bot': received_by_bot,
                    'bot_return': bot_return_amount,
                    'final_payoff': final_payoff,
                }
            }
        except Exception as e:
            return { player.id_in_group: { 'type': 'error', 'message': str(e) } }

    # ----------------------------------------
    # 練習2 (返礼側): Botの贈与額をランダムに決める
    # ----------------------------------------
    def live_determine_bot_receiver(self, payload):
        player = self.player
        min_g, max_g = Constants.PRACTICE_GIFT_FROM_BOT_RANGE
        multiplier = Constants.MULTIPLIER

        # 1. ランダムな贈与額を決定
        gift = random.randint(min_g, max_g)
        
        # 2. Playerモデルに一時保存
        player.practice_bot_gift_amount = gift
        
        # 3. JSに結果を返す
        received_amount = gift * multiplier
        return {
            player.id_in_group: {
                'type': 'bot_receiver_determined',
                'gift_amount': gift,
                'received_amount': received_amount
            }
        }

    # ----------------------------------------
    # 練習2 (返礼側): シミュレーション計算
    # ----------------------------------------
    def live_calculate_receiver(self, payload):
        player = self.player
        try:
            return_amount = int(payload['return_amount'])
            
            # Playerに保存された贈与額を読み込む
            gift = player.practice_bot_gift_amount
            multiplier = Constants.MULTIPLIER
            received_by_you = gift * multiplier

            if not 0 <= return_amount <= received_by_you:
                raise ValueError("Return amount out of range")

            final_payoff = received_by_you - return_amount
            
            return {
                player.id_in_group: {
                    'type': 'receiver_result',
                    'received_by_you': received_by_you,
                    'return_amount': return_amount,
                    'final_payoff': final_payoff,
                }
            }
        except Exception as e:
            return { player.id_in_group: { 'type': 'error', 'message': str(e) } }

# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P1_Consent,
    P2_MatchingWait,
    P3_GroupFormation,
    P4_ExperimentOverview,
    P5_GameInstruction,
    P6_GamePractice
]