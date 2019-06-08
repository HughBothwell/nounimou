# Monty Hall simulator
from abc import ABC, abstractmethod
from random import choice

TRIES = 1000

#
# Game Strategies
#

class MontyHallStrategy(ABC):
    @abstractmethod
    def guess1(self, doors):
        """
        First guess - given a list of doors, pick one of them and return it
        """
        return doors[0]
        
    @abstractmethod
    def guess2(self, remaining_doors):
        """
        Second guess - given a list of remaining doors,
        return your initial guess OR one of the remaining doors
        """
        return remaining_doors[0]
        
class Change(MontyHallStrategy):
    def guess1(self, doors):
        return choice(doors)
        
    def guess2(self, remaining_doors):
        return choice(remaining_doors)
        
class DontChange(MontyHallStrategy):
    def guess1(self, doors):
        self.first_guess = choice(doors)
        return self.first_guess
        
    def guess2(self, remaining_doors):
        return self.first_guess

#
# Game
#

class MontyHallGame:
    def __init__(self, strategy, num_doors = 3):
        assert num_doors >= 3, "Can't have fewer than 3 doors"
        self.strategy = strategy
        self.doors = list(range(num_doors))
        
    def do_round(self):
        # place the prize behind a random door
        prize = choice(self.doors)
        # contestant makes first guess
        guess = self.strategy.guess1(self.doors)
        # produce list of remaining doors
        remaining_doors = self.doors[:]
        remaining_doors.remove(guess)
        # host removes an empty door
        while True:
            pick = choice(remaining_doors)
            if pick != prize:
                remaining_doors.remove(pick)
                break
        # contestant makes second guess
        guess = self.strategy.guess2(remaining_doors)
        return guess == prize
        
    def play(self, rounds):
        return sum(self.do_round() for i in range(rounds))

def main():
    print("Monty Hall sim")

    print("\nStrategy: Change")
    wins = MontyHallGame(Change(), 3).play(TRIES)
    pct = 100. * wins / TRIES
    print(f"{wins:d} wins out of {TRIES:d} = {pct:0.1f}")
    
    print("\nStrategy: Don't Change")
    wins = MontyHallGame(DontChange(), 3).play(TRIES)
    pct = 100. * wins / TRIES
    print(f"{wins:d} wins out of {TRIES:d} = {pct:0.1f}")

if __name__ == "__main__":
    main()