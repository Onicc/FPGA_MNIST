#include "pytorch.h"

/**
 * @brief 
 * @param  varname          My Param doc
 * @param  shape            depth, size_t channel, size_t rows, size_t cols
 * example:
    size_t shape[4] = {1, 3, 516, 516};
    pyGenerator("input_0", shape);
 */
void pyGenerator(string varname, size_t shape[4]) {
    string cmd = \
        "python ../scripts/comparison/generator.py \
        --name " + varname + " \
        --shape " + to_string(shape[0]) + " " + to_string(shape[1]) + " " + to_string(shape[2]) + " " + to_string(shape[3]) + " \
        ";
    system(cmd.data());
}

/**
 * @brief 
 * @param  inputName        My Param doc
 * @param  kernelName       My Param doc
 * @param  outoutName       My Param doc
 * @param  stride           My Param doc
 * @param  padding          My Param doc
 * example
    string input = "input_0";
    string kernel = "kernel_0";
    string output = "output_0";
    pyConvolution(input, kernel, output, 1, 0);
 */
void pyConvolution(string inputName, string kernelName, string outoutName, size_t stride, size_t padding) {
    string cmd = \
        "python ../scripts/comparison/convolution.py \
        --input_name " + inputName + " \
        --kernel_name " + kernelName + " \
        --output_name " + outoutName + " \
        --stride " + to_string(stride) + " \
        --padding " + to_string(padding) + " \
        ";
    system(cmd.data());
}

void pyBatchNorm(string inputName, string outoutName, size_t num_features) {
    string cmd = \
        "python ../scripts/comparison/normalization.py \
        --input_name " + inputName + " \
        --output_name " + outoutName + " \
        --num_features " + to_string(num_features) + " \
        ";
    system(cmd.data());
}

void pyMaxPool(string inputName, string outoutName, size_t stride, size_t padding) {
    string cmd = \
        "python ../scripts/comparison/pooling.py \
        --input_name " + inputName + " \
        --output_name " + outoutName + " \
        --stride " + to_string(stride) + " \
        --padding " + to_string(padding) + " \
        ";
    system(cmd.data());
}

void pyLeakyReLU(string inputName, string outoutName, float negativeSlope) {
    string cmd = \
        "python ../scripts/comparison/activation.py \
        --input_name " + inputName + " \
        --output_name " + outoutName + " \
        --negative_slope " + to_string(negativeSlope) + " \
        ";
    system(cmd.data());
}
