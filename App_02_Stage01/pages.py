from otree.api import Page
from .models import Constants

# -------------------------------------------------------
# Page 6: 説明 (今回はスキップ/使い回しとのことなので枠のみ)
# -------------------------------------------------------
class P7_MatchingInstruction(Page):

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None


class P8_MatchingWait(Page):
    # 5秒間、自動でこのページに留まらせる (演出のため)
    timeout_seconds = 3
    timer_text = "相手が決定するまでお待ちください"

    # 同意した人だけ表示 (同意しなかった人はこのAppの以降のページをすべてスキップ)
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 7: 1人目(Aさん) - Receiver役 (Botからの贈り物)
# -------------------------------------------------------
class P9_Game1_Receiver_Wait(Page):
    timeout_seconds = 30
    timer_text = "相手が決定するまでお待ちください"

    def vars_for_template(self):
        return {
            'bot': Constants.BOT_A,
            'multiplier': Constants.MULTIPLIER,
            'initial_endowment': Constants.INVESTMENT_MAX,
        }

    def before_next_page(self):
        # 記録用: Botの贈与額を保存
        bot_gift = Constants.BOT_A['gift_amount']
        multiplier = Constants.MULTIPLIER
        received = bot_gift * multiplier
        self.player.g1_bot_gift = bot_gift
        self.player.g1_recieved = received


    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 8: 1人目(Aさん) - Sender役 (あなたが贈り物)
# -------------------------------------------------------
class P10_Game1_Receiver_Decision(Page):
    form_model = 'player'
    form_fields = ['g1_return']

    def vars_for_template(self):
        # 受け取る額を計算して渡す
        received = self.player.g1_recieved
        
        return {
            'bot': Constants.BOT_A,
            'multiplier': Constants.MULTIPLIER,
            'received_amount': received,
            'initial_endowment': Constants.INVESTMENT_MAX,
        }
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

class P11_Game1_Sender_Decision(Page):
    form_model = 'player'
    form_fields = ['g1_gift']

    def vars_for_template(self):
        return {
            'bot': Constants.BOT_A,
            'multiplier': Constants.MULTIPLIER,
            'initial_endowment': Constants.INVESTMENT_MAX,
        }
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 8b: 1人目(Aさん) - 相手の意思決定 (待機)
# -------------------------------------------------------
class P12_Game1_Sender_Wait(Page):
    # ★ 20秒経過で自動的に次のページへ
    timeout_seconds = 30
    timer_text = "相手が決定するまでお待ちください"

    def vars_for_template(self):
        return {
            'bot': Constants.BOT_A,
        }

    def before_next_page(self):
        # Botの返礼額を計算して保存
        invest = self.player.g1_gift
        received = invest * Constants.MULTIPLIER
        bot_return = int(received * Constants.BOT_A['return_rate'])
        self.player.g1_bot_return = bot_return
        self.player.g1_bot_recieved = received

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 8c: 1人目(Aさん) - 結果表示
# -------------------------------------------------------
class P13_Game1_Sender_Result(Page):
    def vars_for_template(self):
        invest = self.player.g1_gift
        bot_return = self.player.g1_bot_return
        received = self.player.g1_bot_recieved
        initial = Constants.INVESTMENT_MAX
        
        your_keep = initial - invest
        final_gain = your_keep + bot_return
        
        return {
            'bot': Constants.BOT_A,
            'initial_endowment': initial,
            'invest': invest,
            'bot_recieved': received,
            'bot_return': bot_return,
            'final_gain': final_gain,
        }
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

class P14_MatchingWait(Page):
    # 5秒間、自動でこのページに留まらせる (演出のため)
    timeout_seconds = 3
    timer_text = "相手が決定するまでお待ちください"

    # 同意した人だけ表示 (同意しなかった人はこのAppの以降のページをすべてスキップ)
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 7: 2人目(Bさん) - Receiver役 (Botからの贈り物)
# -------------------------------------------------------
class P15_Game2_Receiver_Wait(Page):
    timeout_seconds = 30
    timer_text = "相手が決定するまでお待ちください"

    def vars_for_template(self):
        return {
            'bot': Constants.BOT_B,
            'multiplier': Constants.MULTIPLIER,
            'initial_endowment': Constants.INVESTMENT_MAX,
        }

    def before_next_page(self):
        # 記録用: Botの贈与額を保存
        bot_gift = Constants.BOT_B['gift_amount']
        multiplier = Constants.MULTIPLIER
        received = bot_gift * multiplier
        self.player.g2_bot_gift = bot_gift
        self.player.g2_recieved = received


    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 8: 2人目(Bさん) - Sender役 (あなたが贈り物)
# -------------------------------------------------------
class P16_Game2_Receiver_Decision(Page):
    form_model = 'player'
    form_fields = ['g2_return']

    def vars_for_template(self):
        # 受け取る額を計算して渡す
        received = self.player.g2_recieved
        
        return {
            'bot': Constants.BOT_B,
            'multiplier': Constants.MULTIPLIER,
            'received_amount': received,
            'initial_endowment': Constants.INVESTMENT_MAX,
        }
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

class P17_Game2_Sender_Decision(Page):
    form_model = 'player'
    form_fields = ['g2_gift']

    def vars_for_template(self):
        return {
            'bot': Constants.BOT_B,
            'multiplier': Constants.MULTIPLIER,
            'initial_endowment': Constants.INVESTMENT_MAX,
        }
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 8b: 2人目(Bさん) - 相手の意思決定 (待機)
# -------------------------------------------------------
class P18_Game2_Sender_Wait(Page):
    # ★ 20秒経過で自動的に次のページへ
    timeout_seconds = 30
    timer_text = "相手が決定するまでお待ちください"

    def vars_for_template(self):
        return {
            'bot': Constants.BOT_B,
        }

    def before_next_page(self):
        # Botの返礼額を計算して保存
        invest = self.player.g2_gift
        received = invest * Constants.MULTIPLIER
        bot_return = int(received * Constants.BOT_B['return_rate'])
        self.player.g2_bot_return = bot_return
        self.player.g2_bot_recieved = received

    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

# -------------------------------------------------------
# Page 8c: 2人目(Bさん) - 結果表示
# -------------------------------------------------------
class P19_Game2_Sender_Result(Page):
    def vars_for_template(self):
        invest = self.player.g2_gift
        bot_return = self.player.g2_bot_return
        received = self.player.g2_bot_recieved
        initial = Constants.INVESTMENT_MAX
        
        your_keep = initial - invest
        final_gain = your_keep + bot_return
        
        return {
            'bot': Constants.BOT_B,
            'initial_endowment': initial,
            'invest': invest,
            'bot_recieved': received,
            'bot_return': bot_return,
            'final_gain': final_gain,
        }
    
    def is_displayed(self):
        return self.participant.vars.get('consent_rejected') is None

page_sequence = [
    P7_MatchingInstruction,
    P8_MatchingWait,
    P9_Game1_Receiver_Wait,
    P10_Game1_Receiver_Decision,
    P11_Game1_Sender_Decision,
    P12_Game1_Sender_Wait,
    P13_Game1_Sender_Result,
    P14_MatchingWait,
    P15_Game2_Receiver_Wait,
    P16_Game2_Receiver_Decision,
    P17_Game2_Sender_Decision,
    P18_Game2_Sender_Wait,
    P19_Game2_Sender_Result,
]