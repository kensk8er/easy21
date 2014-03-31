import pylab
from easy21.environment import step, State
from easy21.plot import plot_linear_value_function
from easy21.policy import epsilon_greedy_linear
from easy21.value import ActionValueLinearApproximation, LinearFunction
from utils.util import *
from easy21 import environment
from collections import defaultdict
import numpy as np

__author__ = 'kensk8er'


def calculate_mse(subject_function):
    true_result = unpickle('result/MonteCarloControl.pkl')
    true_action_value_function = true_result['action_value']
    linear_function = LinearFunction()

    # calculate the MSE
    MSE = 0
    denominator = 0
    for dealer in range(1, 11):
        for player in range(1, 22):
            for action in range(0, 2):
                state = State(dealer=dealer, player=player)
                linear_function.update(state)
                features = linear_function.get_features()

                MSE += (subject_function[(features, action)] - true_action_value_function[
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
    action_value_function = ActionValueLinearApproximation(float)
    linear_function = LinearFunction()
    parameters_hit = np.array([0 for i in range(3 * 6)])
    parameters_stick = np.array([0 for i in range(3 * 6)])

    # define parameters
    batch = 100
    num_zero = 10
    epsilon = 0.1
    alpha = 0.01
    HIT = 0
    STICK = 1

    if lambda_value == 0. or lambda_value == 1.:
        learning_curve = []

    # iterate over iteration_num
    for episode in xrange(iteration_num):
        if episode % batch == 0:
            print '\repisode:', episode,

            if lambda_value == 0. or lambda_value == 1.:
                learning_curve.append(calculate_mse(action_value_function))

        # initialize state, action, and eligibility-trace
        state = environment.State()
        linear_function.update(state)
        current_features = linear_function.get_features()
        action = epsilon_greedy_linear(action_value_function, current_features, epsilon)
        eligibility_hit = np.array([0 for i in range(3 * 6)])
        eligibility_stick = np.array([0 for i in range(3 * 6)])

        while state.terminal is False:
            # update delta, and eligibility-trace
            if action == HIT:
                eligibility_hit = np.add(eligibility_hit, np.array(current_features))
            else:
                eligibility_stick = np.add(eligibility_stick, np.array(current_features))

            # take an action
            reward = step(state, action)
            if reward is None:
                # assign 0 if the match hasn't finished yet
                reward = 0
            linear_function.update(state)
            new_features = linear_function.get_features()

            # update delta
            delta_hit = reward - np.array(new_features).dot(parameters_hit)
            delta_stick = reward - np.array(new_features).dot(parameters_stick)

            # update Action Value Function
            if action == HIT:
                action_value_function.update_value((new_features, action), parameters_hit)
            else:
                action_value_function.update_value((new_features, action), parameters_stick)

            # update delta, parameters, and eligibility-trace
            if action == HIT:
                delta_hit += action_value_function[(new_features, HIT)]
            else:
                delta_stick += action_value_function[(new_features, STICK)]
            parameters_hit = np.add(parameters_hit, alpha * delta_hit * eligibility_hit)
            parameters_stick = np.add(parameters_stick, alpha * delta_stick * eligibility_stick)
            eligibility_hit = eligibility_hit * lambda_value
            eligibility_stick = eligibility_stick * lambda_value

            # decide an action
            action = epsilon_greedy_linear(action_value_function, new_features, epsilon)

            # update state and action
            current_features = new_features

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
    #plot_linear_value_function(action_value_function, "Optimal Value Function (Linear Approximation)")

    return MSE


if __name__ == '__main__':
    MSE = [0 for i in range(11)]

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
