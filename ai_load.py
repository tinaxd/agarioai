from ai import StandardAI, NaturalAI
from chase_ai import ChaserAI


def get_ai(ai_name):
    return {
        'StandardAI': StandardAI,
        'ChaserAI': ChaserAI,
        'NaturalAI': NaturalAI
    }[ai_name]