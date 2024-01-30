import pandas as pd
from code.classes.board import Board

class ReprTester:
    def comparer(input, csv):
        a = Board(input, csv, False)
        # print(a.get_moves())
        b = Board(input, csv, False)

        print('a == b', a.__repr__(), a.__repr__() == b.__repr__(), b.__repr__())

        c = Board(input, csv, True)
        print('a == c', a.__repr__(), a.__repr__() == c.__repr__(), c.__repr__())

        c.move(c.cars[0], -1)

        print('a != c (after a move)', a.__repr__(), a.__repr__() != c.__repr__(), c.__repr__())
        c.move(c.cars[0], 1)
        print('a == c (after backmove)', a.__repr__(), a.__repr__() == c.__repr__(), c.__repr__())

    def get_moves():
        input = 'data/Rushhour6x6_1.csv'
        csv = pd.read_csv(input) 

        a = Board(input, csv, False)

        original_repr = a.__repr__()

        moves = a.get_states()

        print('original_repr not in moves', original_repr not in moves)
        print('moves all different', len(set(moves)) == len(moves))
