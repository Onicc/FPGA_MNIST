/**
 * @file matrix.cpp
 * @brief 
 * @author caixc (171586490@qq.com)
 * @version 1.0
 * @date 2021-05-21
 * 
 * @copyright Copyright (c) {2020}
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2021-05-21 <td>1.0     <td>caixc   <td>Matx可表示1维到4维的矩阵，及其简单运算
 * <tr><td>2021-06-22 <td>1.0     <td>caixc   <td>加入sum、mean函数
 * <tr><td>2021-06-25 <td>1.0     <td>caixc   <td>加入split、load函数
 * <tr><td>2021-06-29 <td>1.0     <td>caixc   <td>加入abs、max、min、/=函数
 * </table>
 */
#include <limits>
#include "matrix.h"
#include "activations.h"

typedef std::numeric_limits< double > dbl;

namespace xcen {

/**
 * @brief Create a new matrix.
 */
template <typename xtype>
void Matx<xtype>::newMatrix(void) {
    ptr = new xtype***[_depth];
    for(int i = 0; i < _depth; i++) {
        ptr[i] = new xtype**[_channel];
        for(int j = 0; j < _channel; j++) {
            ptr[i][j] = new xtype*[_rows];
            for(int k = 0; k < _rows; k++) {
                ptr[i][j][k] = new xtype[_cols];
            }
        }
    }
}

/**
 * @brief Create a new matrix and assign a value.
 * @param  value           value
 */
template <typename xtype>
void Matx<xtype>::newMatrix(xtype value) {
    ptr = new xtype***[_depth];
    for(int i = 0; i < _depth; i++) {
        ptr[i] = new xtype**[_channel];
        for(int j = 0; j < _channel; j++) {
            ptr[i][j] = new xtype*[_rows];
            for(int k = 0; k < _rows; k++) {
                ptr[i][j][k] = new xtype[_cols];
            }
        }
    }

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
 * @brief Delete matrix.
 */
template <typename xtype>
void Matx<xtype>::deleteMatrix(void) {
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
 * @brief Construct a new Matx<xtype>:: Matx object
 */
template <typename xtype>
Matx<xtype>::Matx(void) {
    _dims = 1;
    _depth = 1;
    _channel = 1;
    _rows = 1;
    _cols = 1;
    newMatrix(0);
}

/**
 * @brief Construct a new Matx:: Matx object with rows and cols.
 * @param  rows             rows/height
 * @param  cols             cols/width
 */
template <typename xtype>
Matx<xtype>::Matx(size_t rows, size_t cols) {
    _dims = 2;
    _depth = 1;
    _channel = 1;
    _rows = rows;
    _cols = cols;
    newMatrix(0);
}

/**
 * @brief Construct a new Matx:: Matx object with channel, rows and cols.
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 */
template <typename xtype>
Matx<xtype>::Matx(size_t channel, size_t rows, size_t cols) {
    _dims = 3;
    _depth = 1;
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix(0);
}

/**
 * @brief Construct a new Matx:: Matx object with depth, channel, rows and cols.
 * @param  depth            depth
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 */
template <typename xtype>
Matx<xtype>::Matx(size_t depth, size_t channel, size_t rows, size_t cols) {
    _dims = 4;
    _depth = depth;
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix(0);
}

// /**
//  * @brief Construct a new Matx:: Matx object and assign a value.
//  * @param  value            [float]value
//  */
// template <typename xtype>
// Matx<xtype>::Matx(xtype value) {
//     _dims = 1;
//     _depth = 1;
//     _channel = 1;
//     _rows = 1;
//     _cols = 1;
//     newMatrix(value);
// }

// /**
//  * @brief Construct a new Matx:: Matx object and assign a value.
//  * @param  rows             rows/height
//  * @param  cols             cols/width
//  * @param  value            [xtype]value
//  */
// template <typename xtype>
// Matx<xtype>::Matx(size_t rows, size_t cols, xtype value) {
//     _dims = 2;
//     _depth = 1;
//     _channel = 1;
//     _rows = rows;
//     _cols = cols;
//     newMatrix(value);
// }

// /**
//  * @brief Construct a new Matx:: Matx object and assign a value.
//  * @param  channel          channel
//  * @param  rows             rows/height
//  * @param  cols             cols/width
//  * @param  value            [xtype]value
//  */
// template <typename xtype>
// Matx<xtype>::Matx(size_t channel, size_t rows, size_t cols, xtype value) {
//     _dims = 3;
//     _depth = 1;
//     _channel = channel;
//     _rows = rows;
//     _cols = cols;
//     newMatrix(value);
// }

/**
 * @brief Construct a new Matx:: Matx object and assign a value.
 * @param  depth            depth
 * @param  channel          channel
 * @param  rows             rows/height
 * @param  cols             cols/width
 * @param  value            [xtype]value
 */
template <typename xtype>
Matx<xtype>::Matx(size_t depth, size_t channel, size_t rows, size_t cols, xtype value) {
    _dims = 4;
    _depth = depth;
    _channel = channel;
    _rows = rows;
    _cols = cols;
    newMatrix(value);
}

/**
 * @brief Destroy the Matx:: Matx object.
 */
template <typename xtype>
Matx<xtype>::~Matx(void) {
    deleteMatrix();
}

/**
 * @brief  split string.
 * @param  str              string
 * @param  tokens           tokens
 * @param  delim            delim
 */
template <typename xtype>
void Matx<xtype>::split(const std::string& str, 
           std::vector<std::string>& tokens, 
           const char delim) {
    tokens.clear();
    
    std::istringstream iss(str);
    std::string tmp;
    while (std::getline(iss, tmp, delim)) {
        if (tmp != "") {
            tokens.emplace_back(std::move(tmp));
        }
    }
}

/**
 * @brief load matrix from txt file.
 * @param  xen_file         matrix name
 */
template <typename xtype>
void Matx<xtype>::load(string xen_file, int dims) {
    string filename = xen_file;
    deleteMatrix();
    ifstream fileStream(filename, ios::in);
    if (fileStream.fail()) {
        throw MyException("Matx::load: Matrix file error.");
    }
    string line;
    getline(fileStream, line, '\n');

    /** read shape */
    vector<string> tokens;
    line = line.substr(2, line.length());
    split(line, tokens, ',');
    int shape[4] = {1, 1, 1, 1};
    for(int i = tokens.size() - 1; i >= 0; i--) {
        shape[i] = atoi(tokens[i].data());
    }
    _depth = shape[0];
    _channel = shape[1];
    _rows = shape[2];
    _cols = shape[3];
    _dims = 4;
    if(_depth == 1) {
        _dims = 3;
        if(_channel == 1) {
            _dims = 2;
            if(_rows == 1) {
                _dims = 1;
            }
        }
    }
    if(dims != 0) _dims = dims;
    newMatrix();

    /** read data */
    size_t index = 0;
    size_t d = 0;
    size_t c = 0;
    size_t y = 0;
    size_t x = 0;
    while(getline(fileStream, line, '\n')) {
        split(line, tokens, ',');
        for(int i = 0; i < tokens.size(); i++) {
            d = index / (shape[1]*shape[2]*shape[3]);
            c = index / (shape[2]*shape[3]) % shape[1];
            y = index / shape[3] % shape[2];
            x = index % shape[3];
            // cout << d << " " << c << " " << y << " " << x << endl;
            if(is_same<xtype, float>::value) ptr[d][c][y][x] = atof(tokens[i].data()); else ptr[d][c][y][x] = atoi(tokens[i].data());
            index++;
        }
    }
}

/**
 * @brief Copy the matrix.
 * @param  m                Matrix object
 * @return Matx& 
 */
template <typename xtype>
Matx<xtype> &Matx<xtype>::operator = (const Matx<xtype> &m) {
    /** Self assignment */
    if(this == &m) {
        return *this;
    }

    /** Matrix sizes are inconsistent, reallocate space */
    if(_dims != m._dims || _depth != m._depth || _channel != m._channel || _rows != m._rows || _cols != m._cols) {
        deleteMatrix();

        _dims = m._dims;
        _depth = m._depth;
        _channel = m._channel;
        _rows = m._rows;
        _cols = m._cols;
        newMatrix();
    }

    /** Copy of Pointer Content */
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = m.ptr[i][j][k][u];
                }
            }
        }
    }

    return *this;
}

/**
 * @brief Matrix self addition.
 * @param  m                Matrix object
 * @return Matx& 
 */
template <typename xtype>
Matx<xtype> &Matx<xtype>::operator += (const Matx<xtype> &m) {
    if(_dims != m._dims || _depth != m._depth || _channel != m._channel || _rows != m._rows || _cols != m._cols) {
        throw MyException("The two matrices are of different sizes.");
    }

    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] += m.ptr[i][j][k][u];
                }
            }
        }
    }

    return *this;
}

/**
 * @brief Matrix self subtraction.
 * @param  m                Matrix object
 * @return Matx& 
 */
template <typename xtype>
Matx<xtype> &Matx<xtype>::operator -= (const Matx<xtype> &m) {
    if(_dims != m._dims || _depth != m._depth || _channel != m._channel || _rows != m._rows || _cols != m._cols) {
        throw MyException("The two matrices are of different sizes.");
    }

    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] -= m.ptr[i][j][k][u];
                }
            }
        }
    }

    return *this;
}

/**
 * @brief Matrix self division.
 * @param  m                Matrix object
 * @return Matx& 
 */
template <typename xtype>
Matx<xtype> &Matx<xtype>::operator /= (const Matx<xtype> &m) {
    if(_dims != m._dims || _depth != m._depth || _channel != m._channel || _rows != m._rows || _cols != m._cols) {
        throw MyException("The two matrices are of different sizes.");
    }

    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] /= m.ptr[i][j][k][u];
                }
            }
        }
    }

    return *this;
}

// template <typename xtype>
// xtype*** Matx<xtype>::operator [] (int x) {
//     if(x >= _depth) {
//         throw MyException("operator [] Error.");
//     }

//     return ptr[x];
// }

/**
 * @brief Matrix addition.
 * @param  m                Matrix object
 * @return Matx 
 */
template <typename xtype>
Matx<xtype> Matx<xtype>::add(const Matx<xtype> &m) {
    Matx result_matx;
    result_matx = *this;
    result_matx += m;

    return result_matx;
}

/**
 * @brief Matrix subtraction.
 * @param  m                Matrix object
 * @return Matx 
 */
template <typename xtype>
Matx<xtype> Matx<xtype>::sub(const Matx<xtype> &m) {
    Matx result_matx;
    result_matx = *this;
    result_matx -= m;

    return result_matx;
}

/**
 * @brief Generate a random number matrix.
 * @param  maxV             The maximum value of a random number
 */
template <typename xtype>
void Matx<xtype>::random(xtype maxV) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(float(rand() % int(maxV*10000)) / 10000);
                }
            }
        }
    }
}

template <typename xtype>
Matx<xtype> Matx<xtype>::abs(void) {
    Matx result_matx;
    result_matx = *this;
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    if(result_matx.ptr[i][j][k][u] < 0) {
                        result_matx.ptr[i][j][k][u] = -result_matx.ptr[i][j][k][u];
                    }
                }
            }
        }
    }

    return result_matx;
}

/**
 * @brief Matrix sum.
 * @return double 
 */
template <typename xtype>
double Matx<xtype>::sum(void) {
    double sum = 0.0;
    for(int d = 0; d < _depth; d++) {
        for(int c = 0; c < _channel; c++) {
            for(int y = 0; y < _rows; y++) {
                for(int x = 0; x < _cols; x++) {
                    sum += double(ptr[d][c][y][x]);
                }
            }
        }
    }
    return sum;
}

/**
 * @brief The mean matrix.
 * @return double 
 */
template <typename xtype>
double Matx<xtype>::mean(void) {
    double mean = 0.0;
    double ele = double(_depth*_channel*_rows*_cols);
    mean = sum()/ele;
    return mean;
}

template <typename xtype>
xtype Matx<xtype>::max(void) {
    xtype max = ptr[0][0][0][0];
    for(int d = 0; d < _depth; d++) {
        for(int c = 0; c < _channel; c++) {
            for(int y = 0; y < _rows; y++) {
                for(int x = 0; x < _cols; x++) {
                    if(ptr[d][c][y][x] > max) {
                        max = ptr[d][c][y][x];
                    }
                }
            }
        }
    }
    return max;
}

template <typename xtype>
xtype Matx<xtype>::min(void) {
    xtype min = ptr[0][0][0][0];
    for(int d = 0; d < _depth; d++) {
        for(int c = 0; c < _channel; c++) {
            for(int y = 0; y < _rows; y++) {
                for(int x = 0; x < _cols; x++) {
                    if(ptr[d][c][y][x] < min) {
                        min = ptr[d][c][y][x];
                    }
                }
            }
        }
    }
    return min;
}

template <typename xtype>
vector<int> Matx<xtype>::maxval_index(void) {
    xtype max = ptr[0][0][0][0];
    vector<int> index = {0, 0, 0, 0};
    for(int d = 0; d < _depth; d++) {
        for(int c = 0; c < _channel; c++) {
            for(int y = 0; y < _rows; y++) {
                for(int x = 0; x < _cols; x++) {
                    if(ptr[d][c][y][x] > max) {
                        max = ptr[d][c][y][x];
                        index = {d, c, y, x};
                    }
                }
            }
        }
    }
    return index;
}

/**
 * @brief Add pad around the matrix.
 * @param  pad_rows         Pad the number of rows
 * @param  pad_cols         Pad the number of cols
 * @param  value            The value of the pad
 */
template <typename xtype>
void Matx<xtype>::padding(size_t pad_rows, size_t pad_cols, xtype value) {
    Matx padding_matx(_depth, _channel, _rows + pad_rows*2, _cols + pad_cols*2, value);
    padding_matx._dims = _dims;

    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    padding_matx.ptr[i][j][k + pad_rows][u + pad_cols] = ptr[i][j][k][u];
                }
            }
        }
    }

    *this = padding_matx;
}

/**
 * @brief Dilation matrix.
 * @param  dilation         The number of dilation.
 */
template <typename xtype>
void Matx<xtype>::dilation(size_t dilation) {
    if(dilation != 0) {
        Matx dilation_matx(_depth, _channel, (_rows - 1)*dilation + _rows, (_cols - 1)*dilation + _cols, 0);
        dilation_matx._dims = _dims;

        for(int i = 0; i < _depth; i++) {
            for(int j = 0; j < _channel; j++) {
                for(int k = 0; k < _rows; k++) {
                    for(int u = 0; u < _cols; u++) {
                        dilation_matx.ptr[i][j][k*(dilation+1)][u*(dilation+1)] = ptr[i][j][k][u];
                    }
                }
            }
        }

        *this = dilation_matx;
    }
}

/**
 * @brief dims.
 * @return int 
 */
template <typename xtype>
int Matx<xtype>::dims(void) const {
    return _dims;
}

/**
 * @brief depth.
 * @return int 
 */
template <typename xtype>
int Matx<xtype>::depth(void) const {
    return _depth;
}

/**
 * @brief channel.
 * @return int 
 */
template <typename xtype>
int Matx<xtype>::channel(void) const {
    return _channel;
}


/**
 * @brief rows/height.
 * @return int 
 */
template <typename xtype>
int Matx<xtype>::rows(void) const {
    return _rows;
}

/**
 * @brief cols/width.
 * @return int 
 */
template <typename xtype>
int Matx<xtype>::cols(void) const {
    return _cols;
}


/**
 * @brief Print matrix.
 */
template <typename xtype>
void Matx<xtype>::show(void) const {
    std::cout.precision(2);
    // std::cout.precision(dbl::max_digits10);
    // std::cout.setf(std::ios::showpoint);
    std::cout << "[";
    for(int i = 0; i < _depth; i++) {
        if(_dims >= 4) std::cout << "[";
        for(int j = 0; j < _channel; j++) {
            if(_dims >= 3) std::cout << "[";
            for(int k = 0; k < _rows; k++) {
                if(_dims >= 2) std::cout << "[";
                for(int u = 0; u < _cols-1; u++) {
                    if(is_same<xtype, uint8_t>::value || is_same<xtype, int8_t>::value)
                        std::cout << int(ptr[i][j][k][u]) << " ";
                    else
                        std::cout << ptr[i][j][k][u] << " ";
                }
                if(is_same<xtype, uint8_t>::value || is_same<xtype, int8_t>::value)
                    std::cout << int(ptr[i][j][k][_cols-1]);
                else
                    std::cout << ptr[i][j][k][_cols-1];
                if(_dims >= 2) {
                    if(k != (_rows - 1)) {
                        std::cout << "]" << std::endl << " ";
                    } else {
                        std::cout << "]" ;
                    }
                }
            }
            if(_dims >= 3) {
                if(j != (_channel - 1)) {
                    std::cout << "]" << std::endl;
                } else {
                    std::cout << "]" ;
                }
            }
        }
        if(_dims >= 4) {
            if(i != (_depth - 1)) {
                std::cout << "]" << std::endl;
            } else {
                std::cout << "]" ;
            }
        }
    }
    std::cout << "]" << std::endl << std::endl;
}


/**activate**/


/**
 * @brief ELU
 * @param  alpha            alpha
 */
template <typename xtype>
void Matx<xtype>::ELU(float alpha) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(nn::ELU_Activate(ptr[i][j][k][u], alpha));
                }
            }
        }
    }
}

/**
 * @brief LeakyReLU
 * @param  negative_slope   
 */
template <typename xtype>
void Matx<xtype>::LeakyReLU(float negative_slope) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(nn::LeakyReLU_Activate(ptr[i][j][k][u], negative_slope));
                }
            }
        }
    }
}

/**
 * @brief ReLU
 */
template <typename xtype>
void Matx<xtype>::ReLU(void) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(nn::ReLU_Activate(ptr[i][j][k][u]));
                }
            }
        }
    }
}

/**
 * @brief ReLU6
 */
template <typename xtype>
void Matx<xtype>::ReLU6(void) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(nn::ReLU6_Activate(ptr[i][j][k][u]));
                }
            }
        }
    }
}

/**
 * @brief Sigmoid
 */
template <typename xtype>
void Matx<xtype>::Sigmoid(void) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(nn::Sigmoid_Activate(ptr[i][j][k][u]));
                }
            }
        }
    }
}

/**
 * @brief Tanh
 */
template <typename xtype>
void Matx<xtype>::Tanh(void) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    ptr[i][j][k][u] = xtype(nn::Tanh_Activate(ptr[i][j][k][u]));
                }
            }
        }
    }
}

/**conv**/

/**
 * @brief convolution
 * @param  kernel           kernel
 * @param  stride           stride
 */
template <typename xtype>
void Matx<xtype>::conv2d(const Matx<xtype> &kernel, size_t stride) {
    if(!((_dims == 2 && (kernel._dims == 2 || kernel._dims == 3)) || (_dims == 3 && (kernel._dims == 3 || kernel._dims == 4) && _channel == kernel._channel))) {
        throw MyException("Matx::conv2d: The input does not match the dimensions of the convolution kernel.");
    }

    int layer_rows = int((_rows - kernel._rows)/stride + 1);
    int layer_cols = int((_cols - kernel._cols)/stride + 1);
    // if(layer_rows != int(float(_rows - kernel._rows)/stride + 1.99999) || layer_cols != int(float(_cols - kernel._cols)/stride + 1.99999)) {
    //     throw MyException("Matrix conv2d is incomplete.");
    // }

    if(_dims == 2 && (kernel._dims == 2 || kernel._dims == 3)) {
        int layer_channel = kernel._channel;
        Matx layer(layer_channel, layer_rows, layer_cols);
        layer._dims = kernel._dims;

        for(int c = 0; c < layer_channel; c++) {
            for(int i = 0; i < layer_rows; i++) {
                for(int j = 0; j < layer_cols; j++) {
                    for(int u = 0; u < kernel._rows; u++) {
                        for(int v = 0; v < kernel._cols; v++) {
                            layer.ptr[0][c][i][j] += (kernel.ptr[0][c][u][v] * ptr[0][0][i*stride + u][j*stride + v]);
                        }
                    }
                }
            }
        }
        *this = layer;
    }else if(_dims == 3 && (kernel._dims == 3 || kernel._dims == 4) && _channel == kernel._channel) {
        int layer_channel = kernel._depth;
        Matx layer(layer_channel, layer_rows, layer_cols);
        layer._dims = kernel._dims - 1;

        for(int lc = 0; lc < layer_channel; lc++) {
            for(int c = 0; c < kernel._channel; c++) {
                for(int i = 0; i < layer_rows; i++) {
                    for(int j = 0; j < layer_cols; j++) {
                        for(int u = 0; u < kernel._rows; u++) {
                            for(int v = 0; v < kernel._cols; v++) {
                                layer.ptr[0][lc][i][j] += (kernel.ptr[lc][c][u][v] * ptr[0][c][i*stride + u][j*stride + v]);
                            }
                        }
                    }
                }
            }
        }
        *this = layer;
    }
}


/**
 * @brief  conv of fpga, kernel_shift大小为核个数，bias_shift大小为核个数, 带relu
 * @tparam xtype 
 * @param  kernel           default is int8
 * @param  kernel_shift     default is int8
 * @param  bias             default is int32
 * @param  bias_shift       default is int8
 * @param  inout_shift      default is int8
 * @param  stride           default is size_t
 */
template <typename xtype>
void Matx<xtype>::conv2d_fpga(const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift, size_t stride) {
    if(!((_dims == 2 && (kernel._dims == 2 || kernel._dims == 3)) || (_dims == 3 && (kernel._dims == 3 || kernel._dims == 4) && _channel == kernel._channel))) {
        throw MyException("Matx::conv2d_fpga: The input does not match the dimensions of the convolution kernel.");
    }

    int layer_rows = int((_rows - kernel._rows)/stride + 1);
    int layer_cols = int((_cols - kernel._cols)/stride + 1);

    if(_dims == 2 && (kernel._dims == 2 || kernel._dims == 3)) {
        int layer_channel = kernel._channel;
        Matx layer(layer_channel, layer_rows, layer_cols);
        layer._dims = kernel._dims;
        // cout << kernel_shift.ptr[0][0][0][0] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][0] << endl;
        for(int c = 0; c < layer_channel; c++) {
            for(int i = 0; i < layer_rows; i++) {
                for(int j = 0; j < layer_cols; j++) {
                    int sum = bias.ptr[0][0][0][0] << (kernel_shift.ptr[0][0][0][0] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][0]);
                    for(int u = 0; u < kernel._rows; u++) {
                        for(int v = 0; v < kernel._cols; v++) {
                            sum += (kernel.ptr[0][c][u][v] * ptr[0][0][i*stride + u][j*stride + v]);
                        }
                    }
                    sum >>= kernel_shift.ptr[0][0][0][0] + inout_shift.ptr[0][0][0][0] - inout_shift.ptr[0][0][0][1];
                    // ReLU
                    if(sum < 0) {
                        sum = 0;
                    } else if(sum > 127) {
                        sum = 127;
                    }
                    layer.ptr[0][c][i][j] = sum;
                }
            }
        }
        *this = layer;
    }else if(_dims == 3 && (kernel._dims == 3 || kernel._dims == 4) && _channel == kernel._channel) {
        int layer_channel = kernel._depth;
        Matx layer(layer_channel, layer_rows, layer_cols);
        layer._dims = kernel._dims - 1;
        // kernel_shift.show();
        // cout << kernel_shift.ptr[0][0][0][0] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][0] << endl;
        // cout << kernel_shift.ptr[0][0][0][0] << endl;
        // cout << inout_shift.ptr[0][0][0][0] << endl;
        // cout << bias_shift.ptr[0][0][0][0] << endl;
        for(int lc = 0; lc < layer_channel; lc++) {
            // cout << (kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][lc]) << endl;
            // cout << (kernel_shift.ptr[0][0][0][lc] + bias_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][1]) << endl;
            for(int i = 0; i < layer_rows; i++) {
                for(int j = 0; j < layer_cols; j++) {
                    int sum = bias.ptr[0][0][0][lc];
                    sum <<= (kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][lc]);
                    // int sum = bias.ptr[0][0][0][lc];
                    // sum <<= (kernel_shift.ptr[0][0][0][0] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][0]);
                    for(int c = 0; c < kernel._channel; c++) {
                        for(int u = 0; u < kernel._rows; u++) {
                            for(int v = 0; v < kernel._cols; v++) {
                                sum += (kernel.ptr[lc][c][u][v] * ptr[0][c][i*stride + u][j*stride + v]);
                            }
                        }
                    }
                    sum >>= kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - inout_shift.ptr[0][0][0][1];
                    // sum >>= kernel_shift.ptr[0][0][0][0] + inout_shift.ptr[0][0][0][0] - inout_shift.ptr[0][0][0][1];
                    // ReLU
                    if(sum < 0) {
                        sum = 0;
                    } else if(sum > 255) {
                        sum = 255;
                    }
                    layer.ptr[0][lc][i][j] = sum;
                }
            }
        }
        *this = layer;
    }
}

template <typename xtype>
void Matx<xtype>::dconv_fpga(const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift, size_t stride) {
    // [C, H, W] x [C, 1, K, K] = [C, Ho, Wo]
    if(!(_dims == 3 && kernel._dims == 4 && _channel == kernel._depth)) {
        cout << _dims << endl;
        cout << kernel._dims << endl;
        cout << _channel << endl;
        cout << "input next:" << kernel.depth() << endl;
        throw MyException("Matx::dconv_fpga: The input does not match the dimensions of the convolution kernel.");
    }

    int layer_rows = int((_rows - kernel._rows)/stride + 1);
    int layer_cols = int((_cols - kernel._cols)/stride + 1);

    int layer_channel = _channel;
    Matx layer(layer_channel, layer_rows, layer_cols);
    layer._dims = _dims;
    for(int lc = 0; lc < layer_channel; lc++) {
        for(int i = 0; i < layer_rows; i++) {
            for(int j = 0; j < layer_cols; j++) {
                int sum = bias.ptr[0][0][0][lc];
                sum <<= (kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][lc]);
                // for(int c = 0; c < kernel._channel; c++) {
                    for(int u = 0; u < kernel._rows; u++) {
                        for(int v = 0; v < kernel._cols; v++) {
                            sum += (kernel.ptr[lc][0][u][v] * ptr[0][lc][i*stride + u][j*stride + v]);
                        }
                    }
                // }
                sum >>= kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - inout_shift.ptr[0][0][0][1];
                // ReLU
                if(sum < 0) {
                    sum = 0;
                } else if(sum > 127) {
                    sum = 127;
                }
                layer.ptr[0][lc][i][j] = sum;
            }
        }
    }
    *this = layer;
}
// template <typename xtype>
// void Matx<xtype>::dconv_fpga(const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift, size_t stride) {
//     // [C, H, W] x [C, 1, K, K] = [C, Ho, Wo]
//     if(!(_dims == 3 && kernel._dims == 4 && _channel == kernel._depth)) {
//         cout << _dims << endl;
//         cout << kernel._dims << endl;
//         cout << _channel << endl;
//         cout << "input next:" << kernel.depth() << endl;
//         throw MyException("Matx::dconv_fpga: The input does not match the dimensions of the convolution kernel.");
//     }

//     int layer_rows = int((_rows - kernel._rows)/stride + 1);
//     int layer_cols = int((_cols - kernel._cols)/stride + 1);

//     int layer_channel = _channel;
//     Matx layer(layer_channel, layer_rows, layer_cols);
//     layer._dims = _dims;
//     for(int lc = 0; lc < layer_channel; lc++) {
//         for(int i = 0; i < layer_rows; i++) {
//             for(int j = 0; j < layer_cols; j++) {
//                 int sum = 0;
//                 for(int u = 0; u < kernel._rows; u++) {
//                     for(int v = 0; v < kernel._cols; v++) {
//                         sum += (kernel.ptr[lc][0][u][v] * ptr[0][lc][i*stride + u][j*stride + v]);
//                     }
//                 }
//                 sum >>= kernel_shift.ptr[0][0][0][lc];
//                 int _bias = bias.ptr[0][0][0][lc];
//                 _bias >>= bias_shift.ptr[0][0][0][lc];
//                 sum += _bias;
//                 // ReLU
//                 if(sum < 0) {
//                     sum = 0;
//                 } else if(sum > 255) {
//                     sum = 255;
//                 }
//                 layer.ptr[0][lc][i][j] = sum;
//             }
//         }
//     }
//     *this = layer;
// }

template <typename xtype>
void Matx<xtype>::pconv_fpga(const Matx<xtype> &kernel, const Matx<int> &kernel_shift, const Matx<int> &bias, const Matx<int> &bias_shift, const Matx<int> &inout_shift) {
    // [C, H, W] x [N, C, 1, 1] = [N, Ho, Wo]
    // [1, H, W] x [N, 1, 1, 1] = [N, Ho, Wo]
    if(!(_dims == 3 && kernel._dims == 4)) {
        throw MyException("Matx::pconv_fpga: The input does not match the dimensions of the convolution kernel.");
    }

    int layer_channel = kernel._depth;
    int layer_rows = _rows;
    int layer_cols = _cols;
    Matx layer(layer_channel, layer_rows, layer_cols);
    layer._dims = kernel._dims - 1;

    for(int lc = 0; lc < layer_channel; lc++) {
        for(int i = 0; i < layer_rows; i++) {
            for(int j = 0; j < layer_cols; j++) {
                int sum = bias.ptr[0][0][0][lc];
                sum <<= (kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - bias_shift.ptr[0][0][0][lc]);
                for(int c = 0; c < kernel._channel; c++) {
                    sum += (kernel.ptr[lc][c][0][0] * ptr[0][c][i][j]);
                }
                sum >>= kernel_shift.ptr[0][0][0][lc] + inout_shift.ptr[0][0][0][0] - inout_shift.ptr[0][0][0][1];
                // ReLU
                if(sum < 0) {
                    sum = 0;
                } else if(sum > 127) {
                    sum = 127;
                }
                layer.ptr[0][lc][i][j] = sum;
            }
        }
    }
    *this = layer;
}


template <typename xtype>
void Matx<xtype>::quantization(const Matx<int> &shift) {
    for(int i = 0; i < _depth; i++) {
        for(int j = 0; j < _channel; j++) {
            for(int k = 0; k < _rows; k++) {
                for(int u = 0; u < _cols; u++) {
                    int _shift = shift.ptr[0][0][0][0];
                    // if(_shift >= 0) ptr[i][j][k][u] = (ptr[i][j][k][u] << _shift);
                    // if(_shift < 0) ptr[i][j][k][u] = (ptr[i][j][k][u] >> (-_shift));
                    ptr[i][j][k][u] = ceil(ptr[i][j][k][u] * pow(2, _shift));
                    ptr[i][j][k][u] = ceil(ptr[i][j][k][u] * pow(2, -_shift));
                }
            }
        }
    }
}

template <typename xtype>
void Matx<xtype>::conv2d_ppq_test(const Matx<xtype> &kernel, const Matx<xtype> &kernel_scale, const Matx<xtype> &bias, const Matx<xtype> &bias_scale, const Matx<xtype> &inout_scale, size_t stride) {
    if(!((_dims == 2 && (kernel._dims == 2 || kernel._dims == 3)) || (_dims == 3 && (kernel._dims == 3 || kernel._dims == 4) && _channel == kernel._channel))) {
        throw MyException("Matx::conv2d_ppq_test: The input does not match the dimensions of the convolution kernel.");
    }

    int layer_rows = int((_rows - kernel._rows)/stride + 1);
    int layer_cols = int((_cols - kernel._cols)/stride + 1);

    if(_dims == 2 && (kernel._dims == 2 || kernel._dims == 3)) {
        int layer_channel = kernel._channel;
        Matx layer(layer_channel, layer_rows, layer_cols);
        layer._dims = kernel._dims;

        for(int c = 0; c < layer_channel; c++) {
            for(int i = 0; i < layer_rows; i++) {
                for(int j = 0; j < layer_cols; j++) {
                    xtype sum = bias.ptr[0][0][0][0]*bias_scale.ptr[0][0][0][0];
                    for(int u = 0; u < kernel._rows; u++) {
                        for(int v = 0; v < kernel._cols; v++) {
                            sum += (kernel.ptr[0][c][u][v] * ptr[0][0][i*stride + u][j*stride + v]*kernel_scale.ptr[0][0][0][0]);
                        }
                    }
                    // sum /= kernel_scale.ptr[0][0][0][0] + inout_scale.ptr[0][0][0][0] - inout_scale.ptr[0][0][0][1];
                    // ReLU
                    if(sum < 0) sum = 0;
                    layer.ptr[0][c][i][j] = sum;
                }
            }
        }
        *this = layer;
    }else if(_dims == 3 && (kernel._dims == 3 || kernel._dims == 4) && _channel == kernel._channel) {
        int layer_channel = kernel._depth;
        Matx layer(layer_channel, layer_rows, layer_cols);
        layer._dims = kernel._dims - 1;
        for(int lc = 0; lc < layer_channel; lc++) {
            for(int i = 0; i < layer_rows; i++) {
                for(int j = 0; j < layer_cols; j++) {
                    xtype sum = bias.ptr[0][0][0][lc]*bias_scale.ptr[0][0][0][lc];
                    for(int c = 0; c < kernel._channel; c++) {
                        for(int u = 0; u < kernel._rows; u++) {
                            for(int v = 0; v < kernel._cols; v++) {
                                sum += (kernel.ptr[lc][c][u][v] * kernel_scale.ptr[0][0][0][lc] * ptr[0][c][i*stride + u][j*stride + v]);
                            }
                        }
                    }
                    sum *= 0.5;
                    // ReLU
                    if(sum < 0) sum = 0;
                    layer.ptr[0][lc][i][j] = sum;
                }
            }
        }
        *this = layer;
    }
}


/**normalization**/

template <typename xtype>
double Matx<xtype>::channelMean(size_t nC) {
    if(nC >= _channel)
        throw MyException("Channel overflow.");

    double sum = 0.0;
    double mean = 0.0;
    double ele = _depth*_rows*_cols;
    
    for(int d = 0; d < _depth; d++) {
        for(int y = 0; y < _rows; y++) {
            for(int x = 0; x < _cols; x++) {
                sum += ptr[d][nC][y][x];
            }
        }
    }
    mean = sum / ele;

    return mean;
}

template <typename xtype>
double Matx<xtype>::channelVar(double mean, size_t nC) {
    double accum = 0.0;
    double var = 0.0;
    double ele = _depth*_rows*_cols;

    for(int d = 0; d < _depth; d++) {
        for(int y = 0; y < _rows; y++) {
            for(int x = 0; x < _cols; x++) {
                accum += pow((ptr[d][nC][y][x] - mean), 2);
            }
        }
    }
    var = accum / ele;

    return var;
}

template <typename xtype>
void Matx<xtype>::batchNorm2d(size_t num_features, float eps) {
    if(num_features != _channel)
        throw MyException("Channel mismatch.");
    
    double mean = 0.0;
    double var = 0.0;
    for(int c = 0; c < num_features; c++) {
        mean = channelMean(c);
        var = channelVar(mean, c);
        for(int d = 0; d < _depth; d++) {
            for(int y = 0; y < _rows; y++) {
                for(int x = 0; x < _cols; x++) {
                    ptr[d][c][y][x] = xtype(((double)ptr[d][c][y][x] - mean)/sqrt(var + eps));
                }
            }
        }
    }
}

/**pooling**/

template <typename xtype>
void Matx<xtype>::maxPool2d(size_t kernel_size, size_t stride) {
    if(_rows < kernel_size || _cols < kernel_size) {
        throw MyException("Matx::maxPool2d: The kernel size is too large.");
    }

    int layer_rows = int((_rows - kernel_size)/stride + 1);
    int layer_cols = int((_cols - kernel_size)/stride + 1);

    Matx<xtype> layer(_channel, layer_rows, layer_cols);
    layer._dims = _dims;
    for(int c = 0; c < _channel; c++) {
        for(int i = 0; i < layer_rows; i++) {
            for(int j = 0; j < layer_cols; j++) {
                xtype maxVal = ptr[0][c][i*stride][j*stride];
                for(int y = i*stride; y < i*stride+kernel_size; y++) {
                    for(int x = j*stride; x < j*stride+kernel_size; x++) {
                        if(ptr[0][c][y][x] > maxVal) {
                            maxVal = ptr[0][c][y][x];
                        }
                    }
                }
                layer.ptr[0][c][i][j] = maxVal;
            }
        }
    }
    *this = layer;
}


} // namespace xcen

template class xcen::Matx<int>;
template class xcen::Matx<float>;
template class xcen::Matx<double>;
template class xcen::Matx<int8_t>;
template class xcen::Matx<uint8_t>;