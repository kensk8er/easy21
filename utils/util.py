__author__ = 'kensk8er'


def enpickle(data, file):
    import cPickle

    fo = open(file, 'w')
    cPickle.dump(data, fo, protocol=2)
    fo.close()


def unpickle(file):
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict

