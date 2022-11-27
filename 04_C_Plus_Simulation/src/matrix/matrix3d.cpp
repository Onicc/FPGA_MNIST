/**
 * @file matrix3d.cpp
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
#include "matrix3d.h"

namespace xcen {

/**
 * @brief Allocation matrix space.
 */
void Matx3D::newMatrix(void) {
    ptr = new float**[_channel];
    for(int i = 0; i < _channel; i++) {
        ptr[i] = new float*[_rows];
        for(int j = 0; j < _rows; j++) {
            ptr[i][j] = new float[_cols];
        }
    }
}

/**
 * @brief Construct a new Matx 3D:: Matx 3D object
 */
Matx3D::Matx3D(void) {
    _channel = 1;
    _rows = 1;
    _cols = 1;
    newMatrix();
    for(int i = 0; i < _channel; i++) {
        for(int j = 0; j < _rows; j++) {
            for(int k = 0; k < _cols; k++) {
                ptr[i][j][k] = 0.0;
            }
        }
    }
}

/**
 * @brief Construct a new Matx 3D:: Matx 3D object
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 */
Matx3D::Matx3D(int channel, int rows, int cols) {
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix();
    for(int i = 0; i < _channel; i++) {
        for(int j = 0; j < _rows; j++) {
            for(int k = 0; k < _cols; k++) {
                ptr[i][j][k] = 0.0;
            }
        }
    }
}

/**
 * @brief Construct a new Matx 3D:: Matx 3D object
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 * @param  value            full of value
 */
Matx3D::Matx3D(int channel, int rows, int cols, float value) {
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix();
    for(int i = 0; i < _channel; i++) {
        for(int j = 0; j < _rows; j++) {
            for(int k = 0; k < _cols; k++) {
                ptr[i][j][k] = value;
            }
        }
    }
}

/**
 * @brief Destroy the Matx 3D:: Matx 3D object
 */
Matx3D::~Matx3D(void) {
    for(int i = 0; i < _channel; i++) {
        for(int j = 0; j < _rows; j++) {
            delete[] ptr[i][j];
        }
        delete[] ptr[i];
    }
    delete[] ptr;
}

/**
 * @brief channel.
 * @return int 
 */
int Matx3D::channel(void) const {
    return _channel;
}


/**
 * @brief rows/height.
 * @return int 
 */
int Matx3D::rows(void) const {
    return _rows;
}

/**
 * @brief cols/width.
 * @return int 
 */
int Matx3D::cols(void) const {
    return _cols;
}

/**
 * @brief Print matrix.
 */
void Matx3D::show(void) const {
    std::cout.precision(6);
    std::cout.setf(std::ios::showpoint);
    std::cout << "[";
    for(int i = 0; i < _channel; i++) {
        std::cout << "[";
        for(int j = 0; j < _rows; j++) {
            std::cout << "[" ;
            for(int k = 0; k < _cols-1; k++) {
                std::cout << ptr[i][j][k] << " ";
            }
            std::cout << ptr[i][j][_cols-1];
            if(j != (_rows-1)) {
                std::cout << "]" << std::endl << " ";
            } else {
                std::cout << "]";
            }
        }
        std::cout << "]" << std::endl;
    }
    std::cout << "]" << std::endl;
}

} // namespace xcen
