/**
 * @file convolution.h
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
 * <tr><td>2021-05-20 <td>1.0     <td>caixc     <td>内容
 * </table>
 */
#ifndef CONVOLUTION_H
#define CONVOLUTION_H

#include <iostream>
#include "exception.h"
#include "matrix.h"

namespace xcen {
namespace nn {

    // // self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, kernel_size//2, bias=False)
    template <typename xtype>
    extern Matx<xtype> Conv2D(const Matx<xtype> &input, const Matx<xtype> &kernel, size_t stride = 1, size_t padding = 0, size_t dilation = 0);

    template <typename xtype>
    extern Matx<xtype> Conv2D_FPGA(const Matx<xtype> &input, const Matx<int> &inout_shift, const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation = 0);

    template <typename xtype>
    extern Matx<xtype> DConv2D_FPGA(const Matx<xtype> &input, const Matx<int> &inout_shift, const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, size_t stride, size_t padding, size_t dilation = 0);

    template <typename xtype>
    extern Matx<xtype> PConv2D_FPGA(const Matx<xtype> &input, const Matx<int> &inout_shift, const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift);

    template <typename xtype>
    extern Matx<xtype> Conv2D_PPQ_Test(const Matx<xtype> &input, const Matx<xtype> &inout_scale, const Matx<xtype> &kernel, const Matx<xtype> &kernel_scale, const Matx<xtype> &bias, const Matx<xtype> &bias_scale, size_t stride, size_t padding, size_t dilation = 0);

} // namespace nn
} // namespace xcen

#endif