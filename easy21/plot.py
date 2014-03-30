from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pylab

__author__ = 'kensk8er'


def plot_value_function(value_function, title):
    """
    plot the value function
    :param value_function: dictionary[(dealer, player)]
    :param title: str
    """
    # plot the value function
    x = range(1, 11)  # dealer
    y = range(1, 22)  # player
    X, Y = np.meshgrid(x, y)
    Z = np.array([[0. for i in range(len(x))] for j in range(len(y))])
    for i in x:
        for j in y:
            Z[j - 1][i - 1] = value_function[(i, j)]
    fig = pylab.figure()
    ax = Axes3D(fig)
    pylab.title(title)
    ax.set_xlabel("Dealer Showing")
    pylab.xlim([1, 10])
    pylab.xticks(range(1, 11))
    ax.set_ylabel("Player Sum")
    pylab.ylim([1, 21])
    pylab.yticks(range(1, 22))
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1)
    pylab.show()
