#ifndef POOLING_H
#define POOLING_H

#include <cmath>
#include "exception.h"
#include "matrix.h"

namespace xcen {
namespace nn {

template <typename xtype>
extern Matx<xtype> MaxPool2d(const Matx<xtype> &input, size_t kernel_size, size_t stride, size_t padding = 0);

} // namespace nn
} // namespace xcen

#endif