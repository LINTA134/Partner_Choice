from otree.api import Pages
from .models import Constants, Player, Currency as c

# ----------------------------------------
# ページ 25: 結果確認と報酬の計算
# ----------------------------------------
class P25_Results(Page):
    
    # このページでは参加者からの入力はなし
    
    def get_payoff(self, investment, return_rate):
        # MULTIPLIER : 投資額が何倍になって相手に届くのか
        multiplier = Constants.MULTIPLIER
        
        # ボットからの返礼額
        return_amount = investment * multiplier * return_rate
        
        payoff_per_game = (Constants.INVESTMENT_MAX - investment) + return_amount
        return payoff_per_game

    def before_next_page(self):
        
        # App_04で保存した意思決定データを取得
        investments = {
            'A': self.player.investment_A,
            'B': self.player.investment_B,
            'C': self.player.investment_C,
            'X': self.player.investment_X,
        }
        
        ranks = {
            'A': self.player.rank_A,
            'B': self.player.rank_B,
            'C': self.player.rank_C,
            'X': self.player.rank_X,
        }

        bot_rates = {
            'A': Constants.BOTS_INFO['A']['return_rate'],
            'B': Constants.BOTS_INFO['B']['return_rate'],
            'C': Constants.BOTS_INFO['C']['return_rate'],
            'X': Constants.BOTS_INFO['X']['return_rate'],
        }

        # --- 成功報酬の計算 ---
        total_points = 0
        
        # 各Botの優先順位に基づいた重みづけ
        rank_weights_map = {}
        for bot_id, rank in ranks.items():
            rank_weights_map[bot_id] = Constants.RANK_WEIGHTS[rank]

        # 各Botの1回あたり利得を計算
        payoff_per_bot = {}
        for bot_id in ['A', 'B', 'C', 'X']:
            investment = investments[bot_id]
            rate = bot_rates[bot_id]
            
            # (原資100 - 投資額) + (投資額 * 倍率 * 返礼率)
            payoff = (Constants.INVESTMENT_MAX - investment) + (investment * Constants.MULTIPLIER * rate)
            payoff_per_bot[bot_id] = payoff

        # 合計12回の加重平均を計算し、最終的な得点を算出
        weighted_sum = 0
        for bot_id in ['A', 'B', 'C', 'X']:
            weighted_sum += payoff_per_bot[bot_id] * rank_weights_map[bot_id]
            
        
        # --- 最終報酬の計算 ---
        success_payoff_jpy = weighted_sum * Constants.POINT_TO_YEN_RATE
        total_payoff_jpy = Constants.FIXED_REWARD + success_payoff_jpy
        
        # --- データをPlayerモデルに保存 ---
        self.player.total_payoff_points = weighted_sum
        self.player.final_payoff_jpy = total_payoff_jpy
        
        # 参加者の最終的な報酬（oTreeの標準機能）
        self.player.payoff = total_payoff_jpy

    #計算結果をHTMLテンプレートに渡す
    def vars_for_template(self):
        success_payoff_jpy = self.player.total_payoff_points * Constants.POINT_TO_YEN_RATE
        
        return {
            'fixed_reward': Constants.FIXED_REWARD,
            'total_payoff_points': round(self.player.total_payoff_points, 2), # 小数点以下2桁に丸める
            'success_payoff_jpy': round(success_payoff_jpy, 2),
            'total_payoff_jpy': self.player.final_payoff_jpy,
        }

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P25_Results,
]