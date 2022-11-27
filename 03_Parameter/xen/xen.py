import numpy as np
import glob

def save(narray, filename):
    header = ','.join(map(str, narray.shape))
    # np.savetxt(dataPath + '/{}.txt'.format(name), narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',')\
    narray = narray.astype(str)
    np.savetxt(filename, narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',', fmt='%s')

def load(filename):
    narray = None
    with open(filename) as f:
        shape = [int(d) for d in f.__next__()[1:-1].split(',')]
        narray = np.genfromtxt(f, delimiter=',').reshape(shape)
    return narray

def load_shift(filename):
    narray = np.load(filename)
    narray = -(np.array(np.log2(narray), np.int32))
    return narray

def npy2xen(npy_path, xen_path):
    narray = np.load(npy_path)
    for i in range(4 - len(narray.shape)):
        narray = [narray]
    narray = np.array(narray)
    # loadData = loadData.reshape(-1, -1, -1, -1)
    header = ','.join(map(str, narray.shape))
    narray = narray.astype(str)
    np.savetxt(xen_path, narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',', fmt='%s')

def npy2xenlog(npy_path, xen_path):
    narray = np.load(npy_path)
    narray = np.abs(np.array(np.log2(narray), np.int32))
    for i in range(4 - len(narray.shape)):
        narray = [narray]
    narray = np.array(narray)
    # loadData = loadData.reshape(-1, -1, -1, -1)
    header = ','.join(map(str, narray.shape))
    narray = narray.astype(str)
    np.savetxt(xen_path, narray.reshape(-1, narray.shape[-1]), header=header, delimiter=',', fmt='%s')

def batch_npy2xen(npy_root, xen_root):
    npy_filenames = glob.glob(npy_root + "/*.npy")
    for npy_filename in npy_filenames:
        name = npy_filename.split("/")[-1][:-4]+".xen"
        if "shift" in npy_filename:
            npy2xenlog(npy_filename, xen_root+"/"+name)
        else:
            npy2xen(npy_filename, xen_root+"/"+name)
        # npy2xen(npy_filename, xen_root+"/"+name)


def auto_gen_xen(npy_root, xen_root):
    batch_npy2xen(npy_root, xen_root)
    # 生成shift_io文件
    shift_io_filenames = glob.glob(npy_root + "/shift_input*.npy")
    shift_io_filenames.sort()
    for i in range(1, len(shift_io_filenames)):
        filename = xen_root + "/shift_io{}.xen".format(i)
        shift_input_filename = shift_io_filenames[i-1]
        shift_output_filename = shift_io_filenames[i]
        shift_io = [load_shift(shift_input_filename), load_shift(shift_output_filename)]
        if i == 1:  # 输入不需要缩放
            shift_io[0] = 0
        shift_io = np.array([[[shift_io]]])
        save(shift_io, filename)