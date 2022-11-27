#ifndef CPVSPY_H
#define CPVSPY_H

#include <string>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include "matrix.h"
#include "convolution.h"
#include "pooling.h"
#include "activations.h"
#include "normalization.h"
#include "pytorch.h"

using namespace std;

template <typename xtype>
extern double conv2dVS(size_t maxChannels, size_t maxRows, size_t maxCols, size_t maxConvChannels);
template <typename xtype>
extern double batchNorm2dVS(size_t maxChannels, size_t maxRows, size_t maxCols);
template <typename xtype>
extern double maxpool2dVS(size_t maxChannels, size_t maxRows, size_t maxCols);
template <typename xtype>
extern double LeakyReLUVS(size_t maxChannels, size_t maxRows, size_t maxCols);


#endif
