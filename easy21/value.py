from collections import defaultdict
from easy21.environment import State
import numpy as np

__author__ = 'kensk8er'


class ActionValue(defaultdict):
    """
    dictionary for Action Value function.
    key should be specified by the tuple of State.dealer, State.player, and Action (int, 0 or 1).
    """
    def __getitem__(self, (dealer, player, action)):
        assert isinstance(dealer, int), 'first argument of tuple must be int'
        assert isinstance(player, int), 'second argument of tuple must be int'
        assert isinstance(action, int), 'third argument of tuple must be int'

        return dict.__getitem__(self, (dealer, player, action))

    def __setitem__(self, (dealer, player, action), value):
        assert isinstance(dealer, int), 'first argument of tuple must be int'
        assert isinstance(player, int), 'second argument of tuple must be int'
        assert isinstance(action, int), 'third argument of tuple must be int'
        assert type(value) is float, 'value must be float'

        dict.__setitem__(self, (dealer, player, action), value)

    def to_value_function(self):
        """
        convert Action Value Function into Value Function
        """
        value_function = Value(float)
        keys = self.keys()
        HIT = 0
        STICK = 1

        for key in keys:
            dealer = key[0]
            player = key[1]
            action = key[2]

            if self.get((dealer, player, HIT)) > self.get((dealer, player, STICK)):
                value_function[(dealer, player)] = self.get((dealer, player, HIT))
            else:
                value_function[(dealer, player)] = self.get((dealer, player, STICK))

        return value_function


class ActionValueLinearApproximation(ActionValue):
    """
    Linear Approximation of Action Value Function
    key should be specified by the list of features (3 * 6 = 18 dimensions list, binary) and action.
    """
    def __getitem__(self, (features, action)):
        if isinstance(features, tuple):
            features = list(features)
        assert isinstance(features, list), 'argument must be list'
        assert isinstance(features[0], int), 'features must be a tuple of int'
        assert isinstance(action, int), 'action must be int'

        return dict.__getitem__(self, (tuple(features), action))

    def __setitem__(self, (features, action), value):
        if isinstance(features, tuple):
            features = list(features)
        assert isinstance(features, list), 'argument must be list'
        assert isinstance(features[0], int), 'features must be a tuple of int'
        assert isinstance(action, int), 'action must be int'

        dict.__setitem__(self, (tuple(features), action), value)

    def update_value(self, (features, action), parameters):
        """
        update the Action Value Function by applying the new parameters
        """
        features = np.array(features)
        new_value = features.dot(parameters)
        features = list(features)

        self.__setitem__((features, action), new_value)


class LinearFunction():
    """
    this class convert the State into features used in Linear Function Approximation
    """
    features = [0 for i in range(3 * 6)]
    feature_template_dealer = [{1, 2, 3, 4}, {4, 5, 6, 7}, {7, 8, 9, 10}]
    feature_template_player = [
        {1, 2, 3, 4, 5, 6}, {4, 5, 6, 7, 8, 9}, {7, 8, 9, 10, 11, 12}, {10, 11, 12, 13, 14, 15},
        {13, 14, 15, 16, 17, 18}, {16, 17, 18, 19, 20, 21}
    ]

    def __init__(self):
        pass

    def get_features(self):
        return self.features

    def update(self, state):
        """
        update the features based on given State information
        """
        assert isinstance(state, State), 'first argument must be State'
        dealer = state.dealer
        player = state.player
        dealer_feature = []
        player_feature = []

        for i in range(len(self.feature_template_dealer)):
            if dealer in self.feature_template_dealer[i]:
                dealer_feature.append(1)
            else:
                dealer_feature.append(0)

        for i in range(len(self.feature_template_player)):
            if player in self.feature_template_player[i]:
                player_feature.append(1)
            else:
                player_feature.append(0)

        for i in range(len(self.features)):
            j = i // len(self.feature_template_player)
            k = i % len(self.feature_template_player)
            self.features[i] = dealer_feature[j] * player_feature[k]


class Value(defaultdict):
    """
    dictionary for Value function.
    key should be specified by the tuple of State.dealer and State.player.
    """
    def __getitem__(self, (dealer, player)):
        assert isinstance(dealer, int), 'first argument of tuple must be int'
        assert isinstance(player, int), 'second argument of tuple must be int'

        return dict.__getitem__(self, (dealer, player))

    def __setitem__(self, (dealer, player), value):
        assert isinstance(dealer, int), 'first argument of tuple must be int'
        assert isinstance(player, int), 'second argument of tuple must be int'
        assert type(value) is float, 'value must be float'

        dict.__setitem__(self, (dealer, player), value)

