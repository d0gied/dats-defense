from typing import List, Tuple, Set, Dict
from random import randint, choice
from uuid import uuid4

from models_gen.cell import Cell, Coordinate
from models_gen.zombie import Zombie, ZPot
from models_gen.block import Base
from models_gen.player import Player

MIN_DIST_BETWEEN_PLAYERS = 50 ** 2
MIN_DIST_FROM_PLAYER_TO_ZPOT = 3 ** 2
GENERATE_ZPOT_LINES = True
# все шансы в процентах
CHANCE_FOR_ZPOT = 10
CHANCE_FOR_ZPOT_IN_LINE = 80
CHANCE_FOR_WALL = 1
CHANCE_FOR_ZOMBIES = 20


def generate_map(
        map_size: int = 300,
        num_players: int = 3,
        team_names: List[str] | None = None):
    teams = dict()
    if team_names is None:
        team_names = []
        for i in range(num_players):
            name = f"BDSM_BOT{i}"
            team_names.append(name)
            teams[name] = Player(enemyBlockKills=0, gameEndedAt="---", gold=10, name=name, points=0, zombieKills=0)
    map_matrix = [[[Cell(x=i, y=j)] for j in range(map_size)] for i in range(map_size)]
    map_matrix, players_cells = _generate_players(map_matrix, map_size, team_names)
    map_matrix, zpots = _generate_ZPot(map_matrix, map_size, players_cells)
    map_matrix = _generate_walls(map_matrix, map_size)
    map_matrix, zombies = _generate_zombies(map_matrix, map_size)
    players_bases = dict()
    players_heads = dict()
    for base in players_cells:
        players_bases[base[0].id] = (base[0].x, base[0].y)
        if base[0].is_head:
            players_heads[base[0].team] = (base[0].x, base[0].y)
    return map_matrix, players_bases, players_heads, zombies, zpots, teams


def _generate_players(
        map_matrix: List[List[Cell]],
        map_size: int,
        team_names: List[str]
) -> Tuple[List[List[Cell]], List[Cell]]:
    players_cells = []
    for team_name in team_names:
        x, y = randint(1, map_size - 1), randint(1, map_size - 1)
        while _get_min_distance(map_matrix[x][y], players_cells) < MIN_DIST_BETWEEN_PLAYERS:
            x, y = randint(1, map_size - 1), randint(1, map_size - 1)
        flag = True
        for i in range(x - 1, x + 1):
            for j in range(y - 1, y + 1):
                if flag:
                    map_matrix[i][j] = [Base(x=i, y=j, attack=40, health=300, isHead=True, id=str(uuid4()), range=8,
                                            team=team_name, lastAttack=Coordinate(x=1, y=1), moved=False)]
                    flag = False
                else:
                    map_matrix[i][j] = [Base(x=i, y=j, attack=10, health=100, isHead=False, id=str(uuid4()), range=5,
                                            team=team_name, lastAttack=Coordinate(x=1, y=1), moved=False)]
                players_cells.append(map_matrix[i][j])
    return map_matrix, players_cells


def _generate_ZPot(map_matrix: List[List[Cell]],
                   map_size: int,
                   players_cells: List[Cell]) -> Tuple[List[List[Cell]], Set[Tuple[int, int]]]:
    zpots_pos = set()
    zpots_pos_dop = set()
    for i in range(map_size):
        for j in range(map_size):
            if randint(0, 100) <= CHANCE_FOR_ZPOT and _get_min_distance(map_matrix[i][j],
                                                                        players_cells) > MIN_DIST_FROM_PLAYER_TO_ZPOT:
                map_matrix[i][j] = [ZPot(x=i, y=j, type="default")]
                zpots_pos.add((i, j))

    if GENERATE_ZPOT_LINES:
        for x, y in zpots_pos:
            if randint(0, 1):
                x_move, y_move = 0, 1
            else:
                x_move, y_move = 1, 0

            x_right_down, y_right_down, x_left_up, y_left_up = x + x_move, y + y_move, x - x_move, y - y_move
            right_down, left_up = True, True

            while right_down or left_up:
                if x_right_down < map_size and y_right_down < map_size and (
                        right_down and randint(0, 100) <= CHANCE_FOR_ZPOT_IN_LINE
                        and _get_min_distance(map_matrix[x_right_down][y_right_down], players_cells) > MIN_DIST_FROM_PLAYER_TO_ZPOT):
                    map_matrix[x_right_down][y_right_down] = [ZPot(x=x_right_down, y=y_right_down, type="default")]
                    zpots_pos_dop.add((x_right_down, y_right_down))
                    x_right_down, y_right_down = x_right_down + x_move, y_right_down + y_move
                else:
                    right_down = False

                if x_left_up > -1 and y_left_up > -1 and (
                        left_up and randint(0, 100) <= CHANCE_FOR_ZPOT_IN_LINE and
                        _get_min_distance(map_matrix[x_left_up][y_left_up], players_cells) > MIN_DIST_FROM_PLAYER_TO_ZPOT):
                    map_matrix[x_left_up][y_left_up] = [ZPot(x=x_left_up, y=y_left_up, type="default")]
                    zpots_pos_dop.add((x_left_up, y_left_up))
                    x_left_up, y_left_up = x_left_up - x_move, y_left_up - y_move
                else:
                    left_up = False
    return map_matrix, zpots_pos_dop | zpots_pos


def _generate_walls(map_matrix: List[List[Cell]],
                    map_size: int) -> List[List[Cell]]:
    return map_matrix


def _generate_zombies(map_matrix: List[List[Cell]],
                      map_size: int) -> Tuple[List[List[Cell]], Dict[str, Tuple[int, int]]]:
    types_of_zombies = {"normal": 1, "fast": 2, "bomber": 1, "liner": 1, "juggernaut": 1, "chaos_knight": 1}
    directions = ["up", "down", "left", "right"]
    zombies = dict()
    for i in range(map_size):
        for j in range(map_size):
            if randint(0, 100) <= CHANCE_FOR_ZOMBIES and not isinstance(map_matrix[i][j][0], (Base, ZPot)):
                z_type = choice(list(types_of_zombies.keys()))
                map_matrix[i][j] = [Zombie(x=i, y=j,
                                          direction=choice(directions),
                                          id=str(uuid4()),
                                          speed=types_of_zombies[z_type],
                                          type=z_type,
                                          waitTurns=randint(0, 5),
                                          health=5,
                                          attack=5)]
                zombies[map_matrix[i][j][0].id] = (i, j)
    return map_matrix, zombies


def _get_min_distance(obj_from: Cell, objects_to: List[Cell]):
    min_dist = 1e18
    for obj_to in objects_to:
        min_dist = min(min_dist, (obj_from[0].x - obj_to[0].x) ** 2 + (obj_from[0].y - obj_to[0].y) ** 2)
    return min_dist


if __name__ == "__main__":
    map, _, _, _, _ = generate_map(map_size=20, num_players=1)

    for row in map:
        for cell in row:
            to_print = ""
            if isinstance(cell[0], Base):
                to_print = "Б"
            elif isinstance(cell[0], Zombie):
                to_print = "З"
            elif isinstance(cell[0], ZPot):
                to_print = "С"
            else:
                to_print = "0"
            print(to_print, end="")
        print()