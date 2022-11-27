/*/**
 * @file activations.h
 * @brief 
 * @author caixc (171586490@qq.com)
 * @version 1.0
 * @date 2021-06-02
 * 
 * @copyright Copyright (c) 2021  XC
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2021-06-02 <td>1.0     <td>caixc   <td>内容
 * </table>
 */
#ifndef ACTIVATIONS_H
#define ACTIVATIONS_H

#include <cmath>
#include "exception.h"
#include "matrix.h"

namespace xcen {
namespace nn {

extern float ELU_Activate(float x, float alpha = 1);
extern float LeakyReLU_Activate(float x, float negative_slope = 0.1);
extern float ReLU_Activate(float x);
extern float ReLU6_Activate(float x);
extern float Sigmoid_Activate(float x);
extern float Tanh_Activate(float x);

template <typename xtype>
extern Matx<xtype> ELU(const Matx<xtype> &X, float alpha = 1);
template <typename xtype>
extern Matx<xtype> LeakyReLU(const Matx<xtype> &X, float negative_slope = 0.1);
template <typename xtype>
extern Matx<xtype> ReLU(const Matx<xtype> &X);
template <typename xtype>
extern Matx<xtype> ReLU6(const Matx<xtype> &X);
template <typename xtype>
extern Matx<xtype> Sigmoid(const Matx<xtype> &X);
template <typename xtype>
extern Matx<xtype> Tanh(const Matx<xtype> &X);

} // namespace nn
} // namespace xcen

#endif