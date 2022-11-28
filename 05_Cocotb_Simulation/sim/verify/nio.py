import numpy as np

dataPath = "../scripts/comparison/data"

def save(narray, name):
    header = ','.join(map(str, narray.shape))
    # np.savetxt(dataPath + '/{}.txt'.format(name), narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',')\
    narray = narray.astype(str)
    np.savetxt(dataPath + '/{}.txt'.format(name), narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',', fmt='%s')


def load(xen_path):
    narray = None
    with open(xen_path) as f:
        shape = [int(d) for d in f.__next__()[1:-1].split(',')]
        narray = np.genfromtxt(f, delimiter=',').reshape(shape)
    return narray
