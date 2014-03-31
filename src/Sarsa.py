import pylab
from easy21.environment import step
from easy21.plot import plot_value_function
from easy21.policy import epsilon_greedy
from easy21.value import ActionValue
from utils.util import *
from easy21 import environment
from collections import defaultdict

__author__ = 'kensk8er'


def calculate_mse(subject_function):
    true_result = unpickle('result/MonteCarloControl.pkl')
    true_action_value_function = true_result['action_value']

    # calculate the MSE
    MSE = 0
    denominator = 0
    for dealer in range(1, 11):
        for player in range(1, 22):
            for action in range(0, 2):
                MSE += (subject_function[(dealer, player, action)] - true_action_value_function[
                    (dealer, player, action)]) ** 2
                denominator += 1
    MSE /= denominator

    return MSE


def sarsa(lambda_value, iteration_num):
    """

    :rtype : MSE (float)
    """
    print 'lambda:', lambda_value

    # define functions (dictionaries)
    action_value_function = ActionValue(float)
    number_state = defaultdict(int)
    number_state_action = defaultdict(int)

    # define parameters
    batch = 100
    num_zero = 10

    if lambda_value == 0. or lambda_value == 1.:
        learning_curve = []

    # iterate over iteration_num
    for episode in xrange(iteration_num):
        if episode % batch == 0:
            print '\repisode:', episode,

            if lambda_value == 0. or lambda_value == 1.:
                learning_curve.append(calculate_mse(action_value_function))

        # initialize state, action, epsilon, and eligibility-trace
        state = environment.State()
        current_dealer = state.dealer
        current_player = state.player
        epsilon = float(num_zero) / (num_zero + number_state[(current_dealer, current_player)])
        current_action = epsilon_greedy(action_value_function, state, epsilon)
        eligibility = defaultdict(int)

        while state.terminal is False:
            # count state and state_action number
            number_state[(current_dealer, current_player)] += 1
            number_state_action[(current_dealer, current_player, current_action)] += 1

            # take an action
            reward = step(state, current_action)
            if reward is None:
                # assign 0 if the match hasn't finished yet
                reward = 0
            new_dealer = state.dealer
            new_player = state.player

            # update epsilon
            epsilon = float(num_zero) / (num_zero + number_state[(new_dealer, new_player)])

            # decide an action
            new_action = epsilon_greedy(action_value_function, state, epsilon)

            # update alpha, delta, and eligibility-trace
            alpha = 1. / number_state_action[(current_dealer, current_player, current_action)]
            delta = reward + action_value_function[(new_dealer, new_player, new_action)] \
                    - action_value_function[(current_dealer, current_player, current_action)]
            eligibility[(current_dealer, current_player, current_action)] += 1

            # iterate over every state and action
            # To Be Fixed: this implementation is probably slower than vectorized way
            for key in action_value_function.keys():
                dealer, player, action = key

                # update the action value function
                action_value_function[(dealer, player, action)] \
                    += alpha * delta * eligibility[(dealer, player, action)]

                # update eligibility-trace
                eligibility[(dealer, player, action)] *= lambda_value

            # update state and action
            current_dealer = new_dealer
            current_player = new_player
            current_action = new_action

    print '\repisode:', episode
    print 'done!'

    if lambda_value == 0. or lambda_value == 1.:
        learning_curve.append(calculate_mse(action_value_function))

    # plot learning curve
    if lambda_value == 0. or lambda_value == 1.:
        x = range(0, iteration_num + 1, batch)
        pylab.title('Learning curve of Mean-Squared Error against episode number: lambda = ' + str(lambda_value))
        pylab.xlabel("episode number")
        pylab.xlim([0, iteration_num])
        pylab.xticks(range(0, iteration_num + 1, batch))
        pylab.ylabel("Mean-Squared Error")
        pylab.plot(x, learning_curve)
        pylab.show()

    # calculate MSE
    print 'calculate the Mean-Squared Error...'
    MSE = calculate_mse(action_value_function)

    ## value function
    #value_function = action_value_function.to_value_function()

    ## plot the optimal value function
    #plot_value_function(value_function, "Optimal Value Function (Sarsa)")

    return MSE


if __name__ == '__main__':
    MSE = range(11)

    # iterate over every lambda
    for i in range(11):
        MSE[i] = sarsa(lambda_value=float(i) / 10, iteration_num=1000)
        print "Mean-Squared Error:", MSE[i]
        print ''

    # plot the mean squared error against lambda
    #x = range(11)
    x = [round(0.1 * i, 1) for i in range(11)]
    pylab.title('Mean-Squared Error against lambda')
    pylab.xlabel("lambda")
    pylab.xlim([0., 1.])
    pylab.xticks([round(0.1 * i, 1) for i in range(11)])
    pylab.ylabel("Mean-Squared Error")
    pylab.plot(x, MSE)
    pylab.show()
