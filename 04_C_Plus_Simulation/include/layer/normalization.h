#ifndef NORMALIZATION_H
#define NORMALIZATION_H

#include <cmath>
#include "exception.h"
#include "matrix.h"

namespace xcen {
namespace nn {

template <typename xtype>
extern Matx<xtype> BatchNorm2d(const Matx<xtype> &X, size_t num_features, float eps = 1e-05);

} // namespace nn
} // namespace xcen

#endif