from ai import StandardAI
from chase_ai import ChaserAI


def get_ai(ai_name):
    return {
        'StandardAI': StandardAI,
        'ChaserAI': ChaserAI
    }[ai_name]