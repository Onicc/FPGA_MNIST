#ifndef PYTORCH_H
#define PYTORCH_H

#include <string>

using namespace std;

extern void pyGenerator(string varname, size_t shape[4]);
extern void pyConvolution(string inputName, string kernelName, string outoutName, size_t stride = 1, size_t padding = 0);
extern void pyBatchNorm(string inputName, string outoutName, size_t num_features);
extern void pyMaxPool(string inputName, string outoutName, size_t stride, size_t padding = 0);
extern void pyLeakyReLU(string inputName, string outoutName, float negativeSlope);

#endif
