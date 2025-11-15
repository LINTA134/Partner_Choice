from otree.api import *
from .models import Constants, Subsession, Group, Player 
from .pages import (
    P14_MainPractice
)

doc = """
Your app description
"""

# ----------------------------------------
# ページ遷移の定義
# ----------------------------------------
page_sequence = [
    P14_MainPractice,
]
