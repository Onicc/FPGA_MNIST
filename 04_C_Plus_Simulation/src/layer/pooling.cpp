#include "pooling.h"

namespace xcen {
namespace nn {

template <typename xtype>
Matx<xtype> MaxPool2d(const Matx<xtype> &input, size_t kernel_size, size_t stride, size_t padding) {
    Matx<xtype> _input;
    _input = input;
    if(padding != 0) {
        _input.padding(padding, padding);
    }
    _input.maxPool2d(kernel_size, stride);
    
    return _input;
}

template Matx<int> MaxPool2d(const Matx<int> &input, size_t kernel_size, size_t stride, size_t padding);
template Matx<float> MaxPool2d(const Matx<float> &input, size_t kernel_size, size_t stride, size_t padding);
template Matx<double> MaxPool2d(const Matx<double> &input, size_t kernel_size, size_t stride, size_t padding);

} // namespace nn
} // namespace xcen
