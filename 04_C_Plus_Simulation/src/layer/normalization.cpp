#include "normalization.h"

namespace xcen {
namespace nn {

template <typename xtype>
Matx<xtype> BatchNorm2d(const Matx<xtype> &X, size_t num_features, float eps) {
    Matx<xtype> _X;
    _X = X;
    _X.batchNorm2d(num_features, eps);

    return _X;
}

template Matx<int> BatchNorm2d(const Matx<int> &X, size_t num_features, float eps);
template Matx<float> BatchNorm2d(const Matx<float> &X, size_t num_features, float eps);
template Matx<double> BatchNorm2d(const Matx<double> &X, size_t num_features, float eps);

} // namespace nn
} // namespace xcen