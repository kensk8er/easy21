from collections import defaultdict

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

