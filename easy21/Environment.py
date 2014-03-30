import sys
import random

__author__ = 'kensk8er'


def step(state, action):
    """
    :param state: State
    :param action: 0 (hit) or 1 (stick)
    :rtype : State next_state, int reward
    """
    # check arguments' type
    assert isinstance(state, State), 'First argument should be State!'
    assert type(action) is int, 'Second argument should be str!'

    assert state.terminal is False, 'terminal is already False!'

    def draw_black():
        """ draw a black (plus) card between 1 and 10 """
        return random.randint(1, 10)

    def draw_red():
        """ draw a red (minus) card between 1 and 10 """
        return -random.randint(1, 10)

    def draw_card():
        """ draw black with probability 2/3, otherwise draw red """
        probability = random.random()
        if probability <= float(2) / 3:
            return draw_black()
        else:
            return draw_red()

    def check_burst(score):
        """ check if a user is burst or not """
        if 1 <= score <= 21:
            return False
        else:
            return True

    # constants
    HIT = 0
    STICK = 1

    # initial values
    player_burst = False
    dealer_burst = False

    ## main routine
    if action == HIT:
        # player
        state.player += draw_card()
        state.turn += 1
        player_burst = check_burst(state.player)

        if player_burst is True:
            state.terminal = True

    elif action == STICK:
        state.turn += 1

        # dealer
        dealer_action = HIT
        dealer_burst = False
        while dealer_action == HIT and dealer_burst is False:
            state.dealer += draw_card()
            dealer_burst = check_burst(state.dealer)
            dealer_action = HIT if 1 <= state.dealer <= 16 else STICK

        state.terminal = True

    else:
        sys.exit('illegal action')

    # calculate reward
    if state.terminal is True:
        if player_burst is True:
            # if a player is burst, the player always loses
            reward = -1
        elif dealer_burst is True:
            # if a dealer is burst, the player always wins
            reward = 1
        else:
            if state.player > state.dealer:
                # player wins
                reward = 1
            elif state.player < state.dealer:
                # player loses
                reward = -1
            elif state.player == state.dealer:
                # draw match
                reward = 0
            else:
                # there's something wrong if all the above conditions are not satisfied
                sys.exit('illegal states')
    else:
        # return None if a match is not finished yet
        reward = None

    return reward


class State(object):
    """
    State of both player and dealer (only initial state)
    """
    def __init__(self, dealer=None, player=None):
        if dealer is not None and player is not None:
            self.dealer = dealer
            self.player = player
        elif dealer is None and player is None:
            self.dealer = random.randint(1, 10)
            self.player = random.randint(1, 10)
        else:
            sys.exit('illegal arguments')

    turn = 0
    terminal = False

    def __str__(self):
        return """State:
        dealer: %s
        player: %s
        turn: %s
        terminal: %s""" % (self.dealer, self.player, self.turn, self.terminal)


# main routine for debugging
if __name__ == '__main__':
    # CONSTANT
    HIT = 0
    STICK = 1
    GAMMA = 1.

    print 'policy: HIT'
    s = State()
    a = HIT

    print 'initial state:', s

    while s.terminal is False:
        r = step(s, a)
        print s

    print 'reward:', r

    s = State()
    a = STICK
    print '\npolicy: STICK'

    print 'initial state:', s

    while s.terminal is False:
        r = step(s, a)
        print s

    print 'reward:', r

