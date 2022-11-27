/**
 * @file convolution.cpp
 * @brief 
 * @author caixc (171586490@qq.com)
 * @version 1.0
 * @date 2021-05-20
 * 
 * @copyright Copyright (c) {2020}
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2021-05-20 <td>1.0     <td>caixc     <td>添加二维卷积
 * </table>
 */
#include "convolution.h"

namespace xcen {
namespace nn {

/**
 * @brief Conv2D
 * @param  input            input
 * @param  kernel           kernel
 * @param  stride           stride
 * @param  padding          padding
 * @param  dilation         dilation
 * @return Matx 
 */
template <typename xtype>
Matx<xtype> Conv2D(const Matx<xtype> &input, const Matx<xtype> &kernel, size_t stride, size_t padding, size_t dilation) {
    if(!((input.dims() == 2 && (kernel.dims() == 2 || kernel.dims() == 3)) || (input.dims() == 3 && (kernel.dims() == 3 || kernel.dims() == 4) && input.channel() == kernel.channel()))) {
        throw MyException("Conv2D: The input does not match the dimensions of the convolution kernel.");
    }

    Matx<xtype> _input, _kernel;
    _input = input;
    _kernel = kernel;
    if(padding != 0) {
        _input.padding(padding, padding);
    }
    if(dilation != 0) {
        _kernel.dilation(dilation);
    }
    _input.conv2d(_kernel, stride);
    
    return _input;
}

template <typename xtype>
Matx<xtype> Conv2D_FPGA(const Matx<xtype> &input, const Matx<int> &inout_shift, const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation) {
    if(!((input.dims() == 2 && (kernel.dims() == 2 || kernel.dims() == 3)) || (input.dims() == 3 && (kernel.dims() == 3 || kernel.dims() == 4) && input.channel() == kernel.channel()))) {
        throw MyException("Conv2D_FPGA: The input does not match the dimensions of the convolution kernel.");
    }

    Matx<xtype> _input, _kernel;
    _input = input;
    _kernel = kernel;
    if(padding != 0) {
        _input.padding(padding, padding);
    }
    if(dilation != 0) {
        _kernel.dilation(dilation);
    }
    // _input.conv2d(_kernel, stride);
    _input.conv2d_fpga(kernel, kernel_shift, bias, bias_shift, inout_shift, stride);
    
    return _input;
}


template <typename xtype>
Matx<xtype> DConv2D_FPGA(const Matx<xtype> &input, const Matx<int> &inout_shift, const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation) {
    if(!(input.dims() == 3 && kernel.dims() == 4 && input.channel() == kernel.depth())) {
        throw MyException("DConv2D_FPGA: The input does not match the dimensions of the convolution kernel.");
    }

    Matx<xtype> _input, _kernel;
    _input = input;
    _kernel = kernel;
    if(padding != 0) {
        _input.padding(padding, padding);
    }
    if(dilation != 0) {
        _kernel.dilation(dilation);
    }
    // _input.conv2d(_kernel, stride);
    _input.dconv_fpga(_kernel, kernel_shift, bias, bias_shift, inout_shift, stride);
    
    return _input;
}

template <typename xtype>
Matx<xtype> PConv2D_FPGA(const Matx<xtype> &input, const Matx<int> &inout_shift, const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift) {
    if(!(input.dims() == 3 && kernel.dims() == 4)) {
        throw MyException("PConv2D_FPGA: The input does not match the dimensions of the convolution kernel.");
    }

    Matx<xtype> _input, _kernel;
    _input = input;
    _kernel = kernel;
    _input.pconv_fpga(_kernel, kernel_shift, bias, bias_shift, inout_shift);
    
    return _input;
}


template <typename xtype>
Matx<xtype> Conv2D_PPQ_Test(const Matx<xtype> &input, const Matx<xtype> &inout_scale, const Matx<xtype> &kernel, const Matx<xtype> &kernel_scale, const Matx<xtype> &bias, const Matx<xtype> &bias_scale, size_t stride, size_t padding, size_t dilation) {
    if(!((input.dims() == 2 && (kernel.dims() == 2 || kernel.dims() == 3)) || (input.dims() == 3 && (kernel.dims() == 3 || kernel.dims() == 4) && input.channel() == kernel.channel()))) {
        throw MyException("Conv2D_PPQ_Test: The input does not match the dimensions of the convolution kernel.");
    }

    Matx<xtype> _input, _kernel;
    _input = input;
    _kernel = kernel;
    if(padding != 0) {
        _input.padding(padding, padding);
    }
    if(dilation != 0) {
        _kernel.dilation(dilation);
    }
    // _input.conv2d(_kernel, stride);
    _input.conv2d_ppq_test(kernel, kernel_scale, bias, bias_scale, inout_scale, stride);
    
    return _input;
}


template Matx<int> Conv2D(const Matx<int> &input, const Matx<int> &kernel, size_t stride, size_t padding, size_t dilation);
template Matx<float> Conv2D(const Matx<float> &input, const Matx<float> &kernel, size_t stride, size_t padding, size_t dilation);
template Matx<double> Conv2D(const Matx<double> &input, const Matx<double> &kernel, size_t stride, size_t padding, size_t dilation);
template Matx<int8_t> Conv2D(const Matx<int8_t> &input, const Matx<int8_t> &kernel, size_t stride, size_t padding, size_t dilation);


template Matx<int8_t> Conv2D_FPGA(const Matx<int8_t> &input, const Matx<int> &inout_shift, const Matx<int8_t> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation);
template Matx<int8_t> DConv2D_FPGA(const Matx<int8_t> &input, const Matx<int> &inout_shift, const Matx<int8_t> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation);
template Matx<int8_t> PConv2D_FPGA(const Matx<int8_t> &input, const Matx<int> &inout_shift, const Matx<int8_t> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift);

template Matx<int> Conv2D_FPGA(const Matx<int> &input, const Matx<int> &inout_shift, const Matx<int> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation);

template Matx<float> Conv2D_PPQ_Test(const Matx<float> &input, const Matx<float> &inout_scale, const Matx<float> &kernel, const Matx<float> &kernel_scale, const Matx<float> &bias, const Matx<float> &bias_scale, size_t stride, size_t padding, size_t dilation);

} // namespace nn
} // namespace xcen
