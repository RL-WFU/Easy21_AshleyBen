import random

random.seed()


class Card:
    def __init__(self, first_turn=False):
        # Color 0 is red, Color 1 or 2 is black
        if first_turn:
            self.cardColor = 1
        else:
            self.cardColor = random.randint(0, 2)

        # CardValue 1-10
        self.cardValue = random.randint(1, 10)


class State:
    def __init__(self, dealer, player, terminal=False):
        self.dealer_first = dealer  # Dealer's first card
        self.player_total = player  # Player's current total
        self.is_terminal = terminal  # Game over: y/n


# Start the game
def begin_game():
    dealer_card = Card(True)
    player_card = Card(True)
    initial_state = State(dealer_card.cardValue, player_card.cardValue)

    return initial_state


# Hit
def hit():
    new_card = Card()
    playerColor = new_card.cardColor
    playerValue = new_card.cardValue

    if playerColor == 0:
        playerValue = -playerValue
    return playerValue


# Stick
def stick(s):
    dealer_total = s.dealer_first
    while dealer_total < 17:
        dealer_total += hit()
    s.is_terminal = True
    return dealer_total


# Checks if either the player or dealer has busted
def checkBust(total):
    return total > 21 or total < 1


# Checks winner and returns reward
def checkWinner(s, dealer_total):
    if checkBust(s.player_total) or (dealer_total > s.player_total):  # redundant?
        r = -1
    elif checkBust(dealer_total) or (s.player_total > dealer_total):
        r = 1
    elif dealer_total == s.player_total:
        r = 0
    else:
        print("ERROR IN CHECKWINNNER") # FIXME: Can be removed after debugging, make the r = 0 statement the else statement
    return r


# Step function
def step(s, a):
    next_s = s
    reward = 0

    # Chooses hit
    if a == 0:
        next_s.player_total += hit()
        if checkBust(next_s, next_s.player_total):
            next_s.is_terminal = True

    # Chooses stick
    elif a == 1:
        dealer_total = stick(next_s)
    else:
        print("ERROR IN STEP")  # FIXME: can be removed after debugging

    if next_s.is_terminal:
        reward = checkWinner(next_s, dealer_total)

    return next_s, reward