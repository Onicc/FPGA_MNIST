/**
 * @file matrix4d.cpp
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
#include "matrix4d.h"

namespace xcen {

/**
 * @brief Allocation matrix space.
 */
void Matx4D::newMatrix(void) {
    ptr = new float***[_depth];
    for(int i = 0; i < _depth; i++) {
        ptr[i] = new float**[_channel];
        for(int j = 0; j < _channel; j++) {
            ptr[i][j] = new float*[_rows];
            for(int k = 0; k < _rows; k++) {
                ptr[i][j][k] = new float[_cols];
            }
        }
    }
}

/**
 * @brief Construct a new Matx 4D:: Matx 4D object
 */
Matx4D::Matx4D(void) {
    _depth = 1;
    _channel = 1;
    _rows = 1;
    _cols = 1;
    newMatrix();
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = 0.0;
                }
            }
        }
    }
}

/**
 * @brief Construct a new Matx 4D:: Matx 4D object
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 */
Matx4D::Matx4D(int depth, int channel, int rows, int cols) {
    _depth = depth;
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix();
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = 0.0;
                }
            }
        }
    }
}

/**
 * @brief Construct a new Matx 4D:: Matx 4D object
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 * @param  value            full of value
 */
Matx4D::Matx4D(int depth, int channel, int rows, int cols, float value) {
    _depth = depth;
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix();
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = value;
                }
            }
        }
    }
}

/**
 * @brief Destroy the Matx 4D:: Matx 4D object
 */
Matx4D::~Matx4D(void) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                delete[] ptr[i][j][k];
            }
            delete[] ptr[i][j];
        }
        delete[] ptr[i];
    }
    delete[] ptr;
}

/**
 * @brief depth.
 * @return int 
 */
int Matx4D::depth(void) const {
    return _depth;
}


/**
 * @brief channel.
 * @return int 
 */
int Matx4D::channel(void) const {
    return _channel;
}


/**
 * @brief rows/height.
 * @return int 
 */
int Matx4D::rows(void) const {
    return _rows;
}

/**
 * @brief cols/width.
 * @return int 
 */
int Matx4D::cols(void) const {
    return _cols;
}

/**
 * @brief Print matrix.
 */
void Matx4D::show(void) const {
    std::cout.precision(6);
    std::cout.setf(std::ios::showpoint);
    std::cout << "[";
    for(int i = 0; i < _depth; i++) {
        std::cout << "[";
        for(int j = 0; j < _channel; j++) {
            std::cout << "[";
            for(int k = 0; k < _rows; k++) {
                std::cout << "[" ;
                for(int u = 0; u < _cols-1; u++) {
                    std::cout << ptr[i][j][k][u] << " ";
                }
                std::cout << ptr[i][j][k][_cols-1];
                if(k != (_rows-1)) {
                    std::cout << "]" << std::endl << " ";
                } else {
                    std::cout << "]";
                }
            }
            std::cout << "]" << std::endl;
        }
        std::cout << "]" << std::endl;
    }
    std::cout << "]" << std::endl;
}

} // namespace xcen
