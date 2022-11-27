/**
 * @file matrix.cpp
 * @brief Matrix source file
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

#include "matrix2d.h"

namespace xcen {

/**
 * @brief Allocation matrix space.
 */
void Matx2D::newMatrix(void) {
    ptr = new float*[_rows];
    for(int i = 0; i < _rows; i++) {
        ptr[i] = new float[_cols];
    }
}

/**
 * @brief Construct a new Matx2D:: Matx2D object with nothing.
 */
Matx2D::Matx2D(void) {
    _rows = 1;
    _cols = 1;
    newMatrix();
    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] = 0.0;
        }
    }
}

/**
 * @brief Construct a new Matx2D:: Matx2D object with rows and cols.
 * @param  rows             rows/height
 * @param  cols             cols/width
 */
Matx2D::Matx2D(int rows, int cols) {
    _rows = rows;
    _cols = cols;
    newMatrix();
    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] = 0.0;
        }
    }
}

/**
 * @brief Construct a new Matx2D:: Matx2D object with set value.
 * @param  rows             rows/height
 * @param  cols             cols/width
 * @param  value            full of value
 */
Matx2D::Matx2D(int rows, int cols, float value) {
    _rows = rows;
    _cols = cols;
    newMatrix();
    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] = value;
        }
    }
}

/**
 * @brief Destroy the Matx2D:: Matx2D object
 */
Matx2D::~Matx2D(void) {
    for(int i = 0; i < _rows; i++) {
        delete[] ptr[i];
    }
    delete[] ptr;
}

/**
 * @brief Copy the matrix
 * @param  m                Matrix object
 * @return Matx2D& 
 */
Matx2D &Matx2D::operator = (const Matx2D &m) {
    /** Self assignment */
    if(this == &m) {
        return *this;
    }

    /** Matrix sizes are inconsistent, reallocate space */
    if(_rows != m._rows || _cols != m._cols) {
        for(int i = 0; i < _rows; i++) {
            delete[] ptr[i];
        }
        delete[] ptr;

        _rows = m._rows;
        _cols = m._cols;
        newMatrix();
    }

    /** Copy of Pointer Content */
    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] = m.ptr[i][j];
        }
    }

    return *this;
}

/**
 * @brief Matrix self addition.
 * @param  m                Matrix object
 * @return Matx2D& 
 */
Matx2D &Matx2D::operator += (const Matx2D &m) {
    if(_rows != m._rows || _cols != m._cols) {
        throw MyException("The two matrices are of different sizes.");
    }

    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] += m.ptr[i][j];
        }
    }

    return *this;
}

/**
 * @brief Matrix self subtraction.
 * @param  m                Matrix object
 * @return Matx2D& 
 */
Matx2D &Matx2D::operator -= (const Matx2D &m) {
    if(_rows != m._rows || _cols != m._cols) {
        throw MyException("The two matrices are of different sizes.");
    }

    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] -= m.ptr[i][j];
        }
    }

    return *this;
}

/**
 * @brief Matrix self multiplication.
 * @param  m                Matrix object
 * @return Matx2D& 
 */
Matx2D &Matx2D::operator *= (const Matx2D &m) {
    if(_cols != m._rows) {
        throw MyException("Two matrices do not satisfy the multiplication condition.");
    }

    Matx2D product_matx(_rows, m._cols);
    for(int i = 0; i < product_matx._rows; i++) {
        for(int j = 0; j < product_matx._cols; j++) {
            for(int k = 0; k < _cols; k++) {
                product_matx.ptr[i][j] += (ptr[i][k] * m.ptr[k][j]);
            }
        }
    }
    *this = product_matx;

    return *this;
}

/**
 * @brief Matrix transpose.
 * @return Matx2D 
 */
Matx2D Matx2D::T(void) {
    Matx2D t_matx(_cols, _rows);
    for(int i = 0; i < t_matx._rows; i++) {
        for(int j = 0; j < t_matx._cols; j++) {
            t_matx.ptr[i][j] = ptr[j][i];
        }
    }

    return t_matx;
}

/**
 * @brief Matrix addition.
 * @param  m                Matrix object
 * @return Matx2D 
 */
Matx2D Matx2D::add(const Matx2D &m) {
    Matx2D result_matx;
    result_matx = *this;
    result_matx += m;

    return result_matx;
}

/**
 * @brief Matrix subtraction.
 * @param  m                Matrix object
 * @return Matx2D 
 */
Matx2D Matx2D::sub(const Matx2D &m) {
    Matx2D result_matx;
    result_matx = *this;
    result_matx -= m;

    return result_matx;
}

/**
 * @brief Matrix multiplication.
 * @param  m                Matrix object
 * @return Matx2D 
 */
Matx2D Matx2D::mult(const Matx2D &m) {
    Matx2D result_matx;
    result_matx = *this;
    result_matx *= m;

    return result_matx;
}

/**
 * @brief Generate a random number matrix.
 * @param  rows             rows/height
 * @param  cols             cols/width
 * @param  maxV             Maximum Random Number
 */
void Matx2D::random(int rows, int cols, float maxV) {
    for(int i = 0; i < _rows; i++) {
        delete[] ptr[i];
    }
    delete[] ptr;

    _rows = rows;
    _cols = cols;
    newMatrix();

    for(int i = 0; i < _rows; i++) {
        for(int j = 0; j < _cols; j++) {
            ptr[i][j] = float(rand() % int(maxV*10000)) / 10000;
        }
    }
}


/**
 * @brief rows/height.
 * @return int 
 */
int Matx2D::rows(void) const {
    return _rows;
}

/**
 * @brief cols/width.
 * @return int 
 */
int Matx2D::cols(void) const {
    return _cols;
}

/**
 * @brief Print matrix.
 */
void Matx2D::show(void) const {
    std::cout.precision(18);
    std::cout.setf(std::ios::showpoint);
    std::cout << "[";
    for(int i = 0; i < _rows; i++) {
        std::cout << "[" ;
        for(int j = 0; j < _cols-1; j++) {
            std::cout << ptr[i][j] << " ";
        }
        std::cout << ptr[i][_cols-1];
        if(i != (_rows-1)) {
            std::cout << "]" << std::endl << " ";
        } else {
            std::cout << "]";
        }
    }
    std::cout << "]" << std::endl;
}

} // namespace xcen
