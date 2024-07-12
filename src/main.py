from libs.alerts import AlertManager
from argparse import ArgumentParser
from libs.game.game import Game, CommandPayload
from libs.models.core import AttackCommand, Coordinate, BuildCommand

parser = ArgumentParser(description="Big Data Small Memory")

parser.add_argument(
    "--command-test", action="store_true", help="Send a test command to the game server"
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.command_test:
        game = Game(api_base_url="http://127.0.0.1:8000/")
        game._command(
            CommandPayload(
                attack=[
                    AttackCommand(
                        block_id="f47ac10b-58cc-0372-8562-0e02b2c3d479",
                        target=Coordinate(x=1, y=1),
                    )
                ],
                build=[],
                move_base=Coordinate(x=1, y=1),
            )
        )
