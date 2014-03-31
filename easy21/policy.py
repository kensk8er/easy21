import random
from easy21.environment import State
from easy21.value import ActionValue, ActionValueLinearApproximation

__author__ = 'kensk8er'


def epsilon_greedy(action_value, state, epsilon):
    """
    epsilon greedy policy (used in Monte-Carlo Control)
    :type action_value: action (int)
    :param action_value: Action Value Function (ActionValue)
    :param state: State
    :param epsilon: float
    """
    assert isinstance(action_value, ActionValue), 'first argument must be ActionValue'
    assert isinstance(state, State), 'second argument must be State'
    assert isinstance(epsilon, float), 'third argument must be float'

    # constants
    HIT = 0
    STICK = 1

    if random.random() > epsilon:
        # exploit
        value_HIT = action_value[(state.dealer, state.player, HIT)]
        value_STICK = action_value[(state.dealer, state.player, STICK)]
        if value_HIT > value_STICK:
            return HIT
        elif value_HIT < value_STICK:
            return STICK
        else:
            # return random action when both value functions are same
            if random.random() > 0.5:
                return HIT
            else:
                return STICK
    else:
        # explore
        if random.random() > 0.5:
            return HIT
        else:
            return STICK


def epsilon_greedy_linear(action_value, features, epsilon):
    """
    epsilon greedy policy (used in Monte-Carlo Control)
    :type action_value: action (int)
    :param action_value: Action Value Function (ActionValueLinearApproximation)
    :param features: list
    :param epsilon: float
    """
    assert isinstance(action_value,
                      ActionValueLinearApproximation), 'first argument must be ActionValueLinearApproximation'
    assert isinstance(features, list), 'second argument must be list'
    assert isinstance(epsilon, float), 'third argument must be float'

    # constants
    HIT = 0
    STICK = 1

    if random.random() > epsilon:
        # exploit
        value_HIT = action_value[(features, HIT)]
        value_STICK = action_value[(features, STICK)]
        if value_HIT > value_STICK:
            return HIT
        elif value_HIT < value_STICK:
            return STICK
        else:
            # return random action when both value functions are same
            if random.random() > 0.5:
                return HIT
            else:
                return STICK
    else:
        # explore
        if random.random() > 0.5:
            return HIT
        else:
            return STICK

