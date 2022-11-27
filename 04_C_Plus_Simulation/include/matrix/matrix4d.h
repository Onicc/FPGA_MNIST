/**
 * @file matrix4D.h
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
 * <tr><td>2021-05-20 <td>1.0     <td>caixc     <td>添加三维矩阵的存储
 * </table>
 */
#ifndef MATRIX4D_H
#define MATRIX4D_H

#include <iostream>
#include "exception.h"

namespace xcen {

/**
 * @brief Matrix 4D class.
 * Includes new matrix, addition, subtraction, multiplication and division, copy and other operations.
 */
class Matx4D {
    private:
        int _depth, _channel, _rows, _cols;
        float ****ptr;
        void newMatrix(void);
    
    public:
        Matx4D(void);
        Matx4D(int depth, int channel, int rows, int cols);
        Matx4D(int depth, int channel, int rows, int cols, float value);
        virtual ~Matx4D(void);

        int depth(void) const;
        int channel(void) const;
        int rows(void) const;
        int cols(void) const;
        void show(void) const;
};

} // namespace xcen

#endif