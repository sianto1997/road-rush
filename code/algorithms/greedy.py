from enum import Enum
import random

class Greedy(Algorithm):
    def __init__(self):
        
    def run(self, board):
        self.board = board
        max_steps = self.board.size - self.board.red_car.column - 1
        
        if max_steps > 0:
            for step in range(1, max_forward_steps + 1):
                
                # Check if there are no cars in the way
                if not self.board.is_blocking_in_direction(self.board.red_car, step):
                    
                    # Move the red car forward by one step
                    if self.board.move(self.board.red_car, 1):
                        self.board.draw()
                        self.record_move(self.board.red_car.id, 1)
                else:
                    
                    # Stop moving if there's a blocking car
                    break
        
        # Check for other blocking cars and move the first one found
        blocking_cars = [car for car in self.board.cars if car != self.board.red_car and self.is_blocking(car)]
        if blocking_cars:
            blocking_car = blocking_cars[0]
            # Determine the direction to move the blocking car
            move_direction = 1 if blocking_car.column > self.board.red_car.column else -1
            if self.board.move(blocking_car, move_direction):
                self.board.draw()
                self.record_move(blocking_car.id, move_direction)
                return

        # If no blocking cars, the game is stuck
        print("The game is stuck! No more moves.")

    def is_blocking(self, car):
        return car.orientation == 'H' and car.row == self.board.red_car.row and car.column > self.board.red_car.column

    def get_name(self):
        return 'Greedy' + 'variant'