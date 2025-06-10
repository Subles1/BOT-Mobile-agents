from dataclasses import dataclass
import os

@dataclass
class BotConfig:
    token: str
    commission_text: str
    log_text: str
    leaderboard_text: str
    faq_text: str
    rates_text: str

    @classmethod
    def from_env(cls) -> 'BotConfig':
        return cls(
            token=os.environ['TELEGRAM_BOT_TOKEN'],
            commission_text=os.getenv('COMMISSION_TEXT', 'No commission info.'),
            log_text=os.getenv('LOG_TEXT', 'No log info.'),
            leaderboard_text=os.getenv('LEADERBOARD_TEXT', 'No leaderboard info.'),
            faq_text=os.getenv('FAQ_TEXT', 'No FAQ info.'),
            rates_text=os.getenv('RATES_TEXT', 'No rates info.'),
        )
