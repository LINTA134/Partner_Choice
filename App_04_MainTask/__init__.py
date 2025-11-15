from otree.api import *
from .models import Constants, Subsession, Group, Player 
from .pages import (
    P15_Wait_Game1,
    P16_MessageInstruction,
    P17_Wait_Message,
    P18_Reputation_Gossip,
    P19_Decision,
)

doc = """
Your app description
"""

page_sequence = [
    P15_Wait_Game1,
    P16_MessageInstruction,
    P17_Wait_Message,
    P18_Reputation_Gossip,
    P19_Decision,
]
