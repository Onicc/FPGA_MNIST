#include "CpVSPy.h"

using namespace xcen;

template <typename xtype>
double conv2dVS(size_t maxChannels, size_t maxRows, size_t maxCols, size_t maxConvChannels) {
    cout << "------------conv2dVS------------" << endl;
    unsigned seed;
    seed = time(0);
    srand(seed);
    size_t chanels = rand() % maxChannels + 1;
    size_t rows = rand() % maxRows + 1;
    size_t cols = rand() % maxCols + 1;
    size_t kernelSize = rand() % min(rows, cols) + 2;
    size_t convChannels = rand() % maxConvChannels + 1;
    if(chanels == 1) {
        convChannels = 1;
    }

    string input = "input_0";
    size_t inputShape[4] = {1, chanels, rows, cols};
    string kernel = "kernel_0";
    size_t kernelShape[4] = {convChannels, chanels, kernelSize, kernelSize};
    string conv = "conv_0";

    cout << "input shape: [1, " << chanels << ", " << rows << ", " << cols << "]" << endl; 
    cout << "kernel shape: [" << convChannels << ", " << chanels << ", " << kernelSize << ", " << kernelSize << "]" << endl;  

    pyGenerator(input, inputShape);
    pyGenerator(kernel, kernelShape);
    pyConvolution(input, kernel, conv, 1, 1);

    Matx<xtype> input_0, kernel_0, conv_0;
    input_0.load("input_0");
    kernel_0.load("kernel_0");
    conv_0 = nn::Conv2D(input_0, kernel_0, 1, 1);

    Matx<xtype> py_conv_0;
    py_conv_0.load("conv_0");
    
    Matx<xtype> error = conv_0.sub(py_conv_0);
    // error /= py_conv_0;

    cout << "error: " << error.min() << ", " << error.max() << endl;

    error.abs();
    return error.mean();
}

template <typename xtype>
double batchNorm2dVS(size_t maxChannels, size_t maxRows, size_t maxCols) {
    cout << "------------batchNorm2dVS------------" << endl;
    unsigned seed;
    seed = time(0);
    srand(seed);
    size_t chanels = rand() % maxChannels + 1;
    size_t rows = rand() % maxRows + 1;
    size_t cols = rand() % maxCols + 1;

    string input = "input_0";
    size_t inputShape[4] = {1, chanels, rows, cols};
    string bn = "bn_0";

    cout << "input shape: [1, " << chanels << ", " << rows << ", " << cols << "]" << endl; 

    pyGenerator(input, inputShape);
    pyBatchNorm(input, bn, chanels);

    Matx<xtype> input_0, bn_0;
    input_0.load("input_0");
    bn_0 = nn::BatchNorm2d(input_0, chanels);

    Matx<xtype> py_bn_0;
    py_bn_0.load("bn_0");
    
    Matx<xtype> error = bn_0.sub(py_bn_0);
    // error /= py_bn_0;

    cout << "error: " << error.min() << ", " << error.max() << endl;

    error.abs();
    return error.mean();
}

template <typename xtype>
double maxpool2dVS(size_t maxChannels, size_t maxRows, size_t maxCols) {
    cout << "------------maxpool2dVS------------" << endl;
    unsigned seed;
    seed = time(0);
    srand(seed);
    size_t chanels = rand() % maxChannels + 1;
    size_t rows = rand() % maxRows + 2;
    size_t cols = rand() % maxCols + 2;

    string input = "input_0";
    size_t inputShape[4] = {1, chanels, rows, cols};
    string pool = "pool_0";

    cout << "input shape: [1, " << chanels << ", " << rows << ", " << cols << "]" << endl; 

    pyGenerator(input, inputShape);
    pyMaxPool(input, pool, 2, 2);

    Matx<xtype> input_0, pool_0;
    input_0.load("input_0");
    pool_0 = nn::MaxPool2d(input_0, 2, 2);

    Matx<xtype> py_pool_0;
    py_pool_0.load("pool_0");
    
    Matx<xtype> error = pool_0.sub(py_pool_0);
    // error /= py_pool_0;

    cout << "error: " << error.min() << ", " << error.max() << endl;

    error.abs();
    return error.mean();
}

template <typename xtype>
double LeakyReLUVS(size_t maxChannels, size_t maxRows, size_t maxCols) {
    cout << "------------LeakyReLUVS------------" << endl;
    unsigned seed;
    seed = time(0);
    srand(seed);
    size_t chanels = rand() % maxChannels + 1;
    size_t rows = rand() % maxRows + 1;
    size_t cols = rand() % maxCols + 1;

    string input = "input_0";
    size_t inputShape[4] = {1, chanels, rows, cols};
    string ac = "ac_0";

    cout << "input shape: [1, " << chanels << ", " << rows << ", " << cols << "]" << endl; 

    pyGenerator(input, inputShape);
    pyLeakyReLU(input, ac, 0.1);

    Matx<xtype> input_0, ac_0;
    input_0.load("input_0");
    ac_0 = nn::LeakyReLU(input_0, 0.1);

    Matx<xtype> py_ac_0;
    py_ac_0.load("ac_0");
    
    Matx<xtype> error = ac_0.sub(py_ac_0);
    // error /= py_ac_0;

    cout << "error: " << error.min() << ", " << error.max() << endl;

    error.abs();
    return error.mean();
}

template double conv2dVS<int>(size_t maxChannels, size_t maxRows, size_t maxCols, size_t maxConvChannels);
template double batchNorm2dVS<int>(size_t maxChannels, size_t maxRows, size_t maxCols);
template double maxpool2dVS<int>(size_t maxChannels, size_t maxRows, size_t maxCols);
template double LeakyReLUVS<int>(size_t maxChannels, size_t maxRows, size_t maxCols);

template double conv2dVS<float>(size_t maxChannels, size_t maxRows, size_t maxCols, size_t maxConvChannels);
template double batchNorm2dVS<float>(size_t maxChannels, size_t maxRows, size_t maxCols);
template double maxpool2dVS<float>(size_t maxChannels, size_t maxRows, size_t maxCols);
template double LeakyReLUVS<float>(size_t maxChannels, size_t maxRows, size_t maxCols);

template double conv2dVS<double>(size_t maxChannels, size_t maxRows, size_t maxCols, size_t maxConvChannels);
template double batchNorm2dVS<double>(size_t maxChannels, size_t maxRows, size_t maxCols);
template double maxpool2dVS<double>(size_t maxChannels, size_t maxRows, size_t maxCols);
template double LeakyReLUVS<double>(size_t maxChannels, size_t maxRows, size_t maxCols);