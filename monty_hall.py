from random import randint

def monty_hall_test(tries = 1000):
    """
    Monty Hall problem:
      There are three doors; behind one is a prize.
      Contestant picks one door.
      Host opens another door, showing no prize.
      Host asks if contestant wants to switch doors?
      
    Should the contestant switch? What are the odds?
    
    Return (probability of winning by not switching)
    """
    wins = sum(randint(1, 3) == 1 for _ in range(tries))
    return wins / tries

def main():
    for _ in range(10):
        print(monty_hall_test())

if __name__ == "__main__":
    main()