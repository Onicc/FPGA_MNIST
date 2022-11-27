/**
 * @file matrix.h
 * @brief Matrix header file
 * @author caixc (171586490@qq.com)
 * @version 1.0
 * @date 2021-05-09
 * 
 * @copyright Copyright (c) {2020}
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2021-05-09 <td>1.0     <td>caixc     <td>新建Matx类，实现二维矩阵的加减乘除、复制等操作
 * <tr><td>2021-05-20 <td>1.0     <td>caixc     <td>更改类名Matx->Matx2D，更改文件名matrix.cpp->matrix2d.cpp
 * </table>
 */

#ifndef MATRIX2D_H
#define MATRIX2D_H

#include <iostream>
#include "exception.h"

namespace xcen {

/**
 * @brief Matrix 2D class.
 * Includes new matrix, addition, subtraction, multiplication and division, copy and other operations.
 */
class Matx2D {
    private:
        int _rows, _cols;
        float **ptr;
        void newMatrix(void);
    
    public:
        Matx2D(void);
        Matx2D(int rows, int cols);
        Matx2D(int rows, int cols, float value);
        virtual ~Matx2D(void);

        Matx2D &operator = (const Matx2D &m);
        Matx2D &operator += (const Matx2D &m);
        Matx2D &operator -= (const Matx2D &m);
        Matx2D &operator *= (const Matx2D &m);
        Matx2D add(const Matx2D &m);
        Matx2D sub(const Matx2D &m);
        Matx2D mult(const Matx2D &m);
        Matx2D T(void);

        void random(int rows, int cols, float maxV);

        int rows(void) const;
        int cols(void) const;
        void show(void) const;
};

} // namespace xcen

#endif
