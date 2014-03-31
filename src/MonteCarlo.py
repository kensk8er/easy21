from easy21.environment import step
from easy21.plot import plot_value_function
from easy21.policy import epsilon_greedy
from easy21.value import ActionValue
from utils.util import *
from easy21 import environment
from collections import defaultdict

__author__ = 'kensk8er'


if __name__ == '__main__':
    # define functions (dictionaries)
    action_value_function = ActionValue(float)
    number_state = defaultdict(int)
    number_state_action = defaultdict(int)

    # define parameters
    iteration_num = 10000000
    num_zero = 10

    # iterate over iteration_num
    for episode in xrange(iteration_num):
        if episode % 100 == 0:
            print '\repisode:', episode,

        # initialize the state
        state = environment.State()

        while state.terminal is False:
            dealer = state.dealer
            player = state.player

            # update epsilon
            epsilon = float(num_zero) / (num_zero + number_state[(dealer, player)])

            # decide an action
            action = epsilon_greedy(action_value_function, state, epsilon)

            # count state and state_action number
            number_state[(dealer, player)] += 1
            number_state_action[(dealer, player, action)] += 1

            # take an action
            reward = step(state, action)
            if reward is None:
                # assign 0 if the match hasn't finished yet
                reward = 0

            # update the action value function
            action_value_function[(dealer, player, action)] += \
                (1. / number_state_action[(dealer, player, action)]) \
                * (reward - action_value_function[(dealer, player, action)])

    print '\repisode:', episode
    print 'done!'

    # calculate value function
    value_function = action_value_function.to_value_function()

    # save the data
    result = {'value': value_function, 'action_value': action_value_function, 'number_state': number_state,
              'number_state_action': number_state_action}
    enpickle(result, 'result/MonteCarloControl.pkl')

    # plot the optimal value function
    plot_value_function(value_function, "Optimal Value Function (Monte-Carlo Control)")