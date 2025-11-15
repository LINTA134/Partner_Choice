# __init__.py

from otree.api import *
# 💡 修正 1: models.py からモデルと定数をインポートする
from .models import Constants, Subsession, Group, Player 
# 💡 修正 2: pages.py から必要なページクラスをインポートする
from .pages import (
    P1_Consent,
    P2_MatchingWait,
    P3_GroupFormation,
    P4_RoleInstruction,
    P5_RewardInstruction,
    P6_RoleAssignmentWait
)

doc = """
Your app description
"""

# 💡 修正 3: 冗長なクラス定義はすべて削除し、インポートしたクラスを使用する

# page_sequence はこのファイルで定義する
page_sequence = [
    P1_Consent,
    P2_MatchingWait,
    P3_GroupFormation,
    P4_RoleInstruction,
    P5_RewardInstruction,
    P6_RoleAssignmentWait,
]
