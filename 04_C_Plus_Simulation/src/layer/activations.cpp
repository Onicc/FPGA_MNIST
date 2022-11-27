/**
 * @file activations.cpp
 * @brief 
 * @author caixc (171586490@qq.com)
 * @version 1.0
 * @date 2021-05-29
 * 
 * @copyright Copyright (c) {2020}
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2021-05-29 <td>1.0     <td>caixc     <td>添加ELU、LeakyReLU、ReLU、ReLU6、Sigmoid、Tanh激活函数
 * <tr><td>2021-07-13 <td>1.0     <td>caixc     <td>添加函数模板及模板声明
 * </table>
 */
#include "activations.h"

namespace xcen {
namespace nn {

float ELU_Activate(float x, float alpha) {
    return (x >= 0)*x + (x < 0)*(exp(x)-1)*alpha;
}

float LeakyReLU_Activate(float x, float negative_slope) {
    return (x>0) ? x : negative_slope*x;
}

float ReLU_Activate(float x) {
    return x*(x>0);
}

float ReLU6_Activate(float x) {
    return (x >= 6.0) ? 6.0 : x*(x>0);
}

float Sigmoid_Activate(float x) {
    float a=1.6732632423543772848170429916717;
    float scale=1.0507009873554804934193349852946;
    return scale*(x*(x > 0)) + a*(exp(x)-1)*(x < 0);
}

float Tanh_Activate(float x) {
    return (exp(2*x)-1)/(exp(2*x)+1);
}

template <typename xtype>
Matx<xtype> ELU(const Matx<xtype> &X, float alpha) {
    Matx<xtype> _X;
    _X = X;
    _X.ELU(alpha);

    return _X;
}

template <typename xtype>
Matx<xtype> LeakyReLU(const Matx<xtype> &X, float negative_slope) {
    Matx<xtype> _X;
    _X = X;
    _X.LeakyReLU(negative_slope);

    return _X;
}

template <typename xtype>
Matx<xtype> ReLU(const Matx<xtype> &X) {
    Matx<xtype> _X;
    _X = X;
    _X.ReLU();

    return _X;
}

template <typename xtype>
Matx<xtype> ReLU6(const Matx<xtype> &X) {
    Matx<xtype> _X;
    _X = X;
    _X.ReLU6();

    return _X;
}

template <typename xtype>
Matx<xtype> Sigmoid(const Matx<xtype> &X) {
    Matx<xtype> _X;
    _X = X;
    _X.Sigmoid();

    return _X;
}

template <typename xtype>
Matx<xtype> Tanh(const Matx<xtype> &X) {
    Matx<xtype> _X;
    _X = X;
    _X.Tanh();

    return _X;
}

template Matx<int> ELU(const Matx<int> &X, float alpha = 1);
template Matx<int> LeakyReLU(const Matx<int> &X, float negative_slope = 0.1);
template Matx<int> ReLU(const Matx<int> &X);
template Matx<int> ReLU6(const Matx<int> &X);
template Matx<int> Sigmoid(const Matx<int> &X);
template Matx<int> Tanh(const Matx<int> &X);

template Matx<float> ELU(const Matx<float> &X, float alpha = 1);
template Matx<float> LeakyReLU(const Matx<float> &X, float negative_slope = 0.1);
template Matx<float> ReLU(const Matx<float> &X);
template Matx<float> ReLU6(const Matx<float> &X);
template Matx<float> Sigmoid(const Matx<float> &X);
template Matx<float> Tanh(const Matx<float> &X);

template Matx<double> ELU(const Matx<double> &X, float alpha = 1);
template Matx<double> LeakyReLU(const Matx<double> &X, float negative_slope = 0.1);
template Matx<double> ReLU(const Matx<double> &X);
template Matx<double> ReLU6(const Matx<double> &X);
template Matx<double> Sigmoid(const Matx<double> &X);
template Matx<double> Tanh(const Matx<double> &X);


} // namespace nn
} // namespace xcen