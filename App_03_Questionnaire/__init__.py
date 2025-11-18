from otree.api import *
from .models import Constants, Subsession, Group, Player 
from .pages import (
    P20_Wait_Game2,
    P21_ManipulationCheck,
    P22_Questionnaire_DVs,
    P23_Questionnaire_Covs,
)

doc = """
Your app description
"""


# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P20_Wait_Game2,
    P21_ManipulationCheck,
    P22_Questionnaire_DVs,
    P23_Questionnaire_Covs,
]
