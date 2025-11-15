from otree.api import *
from .pages import (
    P7_Game1_Instruction,
    P9_RoomTransition1,
    P10_Game2_Instruction,
    P11_Game2_Rule,
    P13_PriorityRule,
)
from .models import Constants, Subsession, Group, Player

doc = """
Your app description
"""

page_sequence = [
    P7_Game1_Instruction,
    P9_RoomTransition1,
    P10_Game2_Instruction,
    P11_Game2_Rule,
    P13_PriorityRule,
]