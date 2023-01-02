/**
 * @file matrix.h
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
 * <tr><td>2021-05-21 <td>1.0     <td>caixc   <td>Matx四维矩阵
 * </table>
 */
#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include "exception.h"

namespace xcen {

/**
 * @brief Matrix class.
 * Includes new matrix, addition, subtraction, multiplication and division, copy and other operations.
 */
template <typename xtype>
class Matx {
    private:
        void newMatrix(void);
        void newMatrix(xtype value);
        void deleteMatrix(void);
        void split(const std::string& str, std::vector<std::string>& tokens, const char delim = ' ');

    public:
        Matx(void);
        Matx(size_t rows, size_t cols);
        Matx(size_t channel, size_t rows, size_t cols);
        Matx(size_t depth, size_t channel, size_t rows, size_t cols);

        // Matx(xtype value);
        // Matx(size_t rows, size_t cols, xtype value);
        // Matx(size_t channel, size_t rows, size_t cols, xtype value);   
        Matx(size_t depth, size_t channel, size_t rows, size_t cols, xtype value);
        virtual ~Matx(void);

        xtype ****ptr;
        size_t _dims;
        size_t _depth, _channel, _rows, _cols;

        void load(string varname, int dims = 0);

        /** operator */
        Matx &operator = (const Matx &m);
        Matx &operator += (const Matx &m);
        Matx &operator -= (const Matx &m);
        Matx &operator /= (const Matx &m);
        // xtype*** operator [] (int x);
        Matx add(const Matx &m);
        Matx sub(const Matx &m);
        Matx cat(const Matx &m);

        void random(xtype maxV);

        Matx abs(void);
        double sum(void);
        double mean(void);
        xtype max(void);
        xtype min(void);
        vector<int> maxval_index(void);
        
        /** batchnorm */
        double channelMean(size_t nC);
        double channelVar(double mean, size_t nC);
        void batchNorm2d(size_t num_features, float eps = 1e-05);

        /** convolution */
        void padding(size_t pad_rows, size_t pad_cols, xtype value = 0);
        void dilation(size_t dilation);
        void conv2d(const Matx &kernel, size_t stride = 1);
        void conv2d_fpga(const Matx &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift, size_t stride = 1);
        void dconv_fpga(const Matx &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift, size_t stride = 1);
        void pconv_fpga(const Matx &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift);
        void quantization(const Matx<int> &shift);
        void conv2d_ppq_test(const Matx<xtype> &kernel, const Matx<xtype> &kernel_scale, const Matx<xtype> &bias, const Matx<xtype> &bias_scale, const Matx<xtype> &inout_scale, size_t stride);

        /** pooling */
        void maxPool2d(size_t kernel_size, size_t stride = 1);

        /** activations */
        void ELU(float alpha = 1);
        void LeakyReLU(float negative_slope = 0.1);
        void ReLU(void);
        void ReLU6(void);
        void Sigmoid(void);
        void Tanh(void);

        /** parameter */
        int dims(void) const;
        int depth(void) const;
        int channel(void) const;
        int rows(void) const;
        int cols(void) const;
        void show(void) const;
};

} // namespace xcen

#endif