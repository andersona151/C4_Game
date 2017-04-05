from game_objects import *


def main():

    print("Welcome to Connect 4 Game.")
    game_inst = C4_Game()
    game_inst.print_grid()

    while not game_inst.is_over:
        game_inst.place_token()
        game_inst.check_for_win()
        game_inst.print_grid()

