from typing import Dict, List, Tuple
from uuid import uuid4

from models_gen.block import Base
from models_gen.zombie import Zombie
from models_gen.cell import Cell, Coordinate
from models_gen.player import Player
from models_gen.zombie import ZPot
"""!!!!!! везде нужно ещё дфс"""
def players_moves(moves: Dict[Dict]):
    pass


def _attacks(attacks_coms: List[Tuple[str, List]],
             bases: Dict[str, Tuple[int, int]],
             zombies: Dict[str, Tuple[int, int]], map_matrix: List[List[List[Cell]]],
             players: Dict[str, Player]):
    for player, attacks_player in attacks_coms:
        for attack in attacks_player:
            base_x, base_y = bases[attack.block_id]
            base_obj = map_matrix[base_x][base_y]
            target = attack.target
            if not (base_obj.moved) and get_dist(base_x, base_y, target.x, target.y) <= base_obj.range ** 2:
                for obj in map_matrix[target.x, target.y]:
                    if isinstance(obj, Base) and obj.team != player:
                        obj.health -= base_obj.attack
                        if obj.health <= 0:
                            bases.pop(obj.id)
                            players[player].enemy_block_kills += 1
                    if isinstance(obj, Zombie):
                        obj.health -= base_obj.attack
                        if obj.health <= 0:
                            zombies.pop(obj.id)
                            players[player].zombie_kills += 1
                            players[player].gold += 1



def _buy_bases(buy_bases_coms: List[Tuple[str, List]], players: Dict[str, Player], map_matrix: List[List[List[Cell]]]):
    for player, buy_base in buy_bases_coms:
        for base in buy_base:
            x = base.x
            y = base.y
            check_difs = [(1, 0), (0, 1), (1, 1), (1, -1)]
            neighbors: List[List[Cell]] = []
            for x_dif, y_dif in check_difs:
                neighbors.append(map_matrix[x + x_dif][y + y_dif])
                neighbors.append(map_matrix[x - x_dif][y - y_dif])
            can_build = False

            for i in range(4):
                for neighbor in neighbors[i]:
                    if isinstance(neighbor, Base) and neighbor.team == player:
                        can_build = True

            for i in range(4):
                for neighbor in neighbors[i]:
                    if isinstance(neighbor, ZPot):
                        can_build = False

            for i in range(8):
                for neighbor in neighbors[i]:
                    if isinstance(neighbor, Base) and neighbor.team != player:
                        can_build = False

            for obj in map_matrix[x][y]:
                if isinstance(obj, (Zombie, ZPot, Base)):
                    can_build = False

            if players[player].gold < 1:
                can_build = False

            if can_build:
                players[player].gold -= 1
                map_matrix[x][y] = [Base(x=x, y=y, attack=10, health=100, isHead=False, id=str(uuid4()), range=5,
                                            team=player, lastAttack=Coordinate(x=1, y=1), moved=False)]




def _move_heads(move_heads_coms: Tuple[str, List[List]]):
    pass


def get_dist(x1: int, y1:int, x2: int, y2: int):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2