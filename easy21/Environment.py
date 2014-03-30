import sys

__author__ = 'kensk8er'

from utils.util import *
import random


def step(state, action):
    """
    :param state:
    :param action: 0 (hit) or 1 (stick)
    :rtype : State next_state, int reward
    """
    # check arguments' type
    assert isinstance(state, State), 'First argument should be State!'
    assert type(action) is int, 'Second argument should be str!'

    assert state.terminal is False, 'terminal is already False!'

    def draw_black():
        return random.randint(1, 10)

    def draw_red():
        return -random.randint(1, 10)

    def draw_card():
        probability = random.random()
        if probability <= float(2) / 3:
            return draw_black()
        else:
            return draw_red()

    def check_burst(score):
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
            reward = -1
        elif dealer_burst is True:
            reward = 1
        else:
            if state.player > state.dealer:
                reward = 1
            elif state.player < state.dealer:
                reward = -1
            elif state.player == state.dealer:
                reward = 0
            else:
                sys.exit('illegal states')
    else:
        reward = None

    return reward


class State(object):
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

