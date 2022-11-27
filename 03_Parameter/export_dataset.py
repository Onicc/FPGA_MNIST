from torchvision import datasets
import numpy as np

def npy2xen(narray, xen_path):
    for i in range(4 - len(narray.shape)):
        narray = [narray]
    narray = np.array(narray)
    # loadData = loadData.reshape(-1, -1, -1, -1)
    header = ','.join(map(str, narray.shape))
    narray = narray.astype(str)
    np.savetxt(xen_path, narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',', fmt='%s')

XEN_PATH = "00_Data/MNIST/xen"
DATASET_PATH = "00_Data"

mnist = datasets.MNIST(DATASET_PATH, train=False, download=True)
mnist_label = mnist.targets.view(-1, 1).numpy()

mnist_data = mnist.data.view(-1, 1, 1, 28, 28).float().numpy()
mnist_data -= 128
dataset_len = mnist_data.shape[0]

for i in range(100):
# for i in range(dataset_len):
    npy2xen(np.array(mnist_data[i], dtype=np.int32), XEN_PATH + '/input_{}.xen'.format(i))
    npy2xen(np.array(mnist_label[i], dtype=np.int32), XEN_PATH + '/output_{}.xen'.format(i))
