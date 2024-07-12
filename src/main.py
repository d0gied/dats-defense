from libs.alerts import AlertManager
from argparse import ArgumentParser

parser = ArgumentParser(description="Big Data Small Memory")

parser.add_argument(
    "--test-alert",
    action="store_true",
    help="Send a test alert to the configured Telegram chat"
)
parser.add_argument(
    "--bot-username",
    action="store_true",
    help="Get the username of the configured Telegram bot"
)

if __name__ == "__main__":
    args = parser.parse_args()
