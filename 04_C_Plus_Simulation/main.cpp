#include "matrix.h"
#include "convolution.h"
#include "activations.h"
#include "normalization.h"
#include "pooling.h"
#include <iostream>
#include <map>

using namespace xcen;

int main() {
    std::map<string,string> weight_map;
    weight_map["b1"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b1.xen";
    weight_map["b2"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b2.xen";
    weight_map["b3"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b3.xen";
    weight_map["b4"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b4.xen";
    weight_map["b5"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b5.xen";
    weight_map["b6"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b6.xen";
    weight_map["b7"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b7.xen";
    weight_map["b8"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/b8.xen";
    weight_map["shift_b1"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b1.xen";
    weight_map["shift_b2"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b2.xen";
    weight_map["shift_b3"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b3.xen";
    weight_map["shift_b4"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b4.xen";
    weight_map["shift_b5"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b5.xen";
    weight_map["shift_b6"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b6.xen";
    weight_map["shift_b7"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b7.xen";
    weight_map["shift_b8"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_b8.xen";
    weight_map["shift_input1"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input1.xen";
    weight_map["shift_input2"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input2.xen";
    weight_map["shift_input3"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input3.xen";
    weight_map["shift_input4"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input4.xen";
    weight_map["shift_input5"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input5.xen";
    weight_map["shift_input6"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input6.xen";
    weight_map["shift_input7"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input7.xen";
    weight_map["shift_input8"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_input8.xen";
    weight_map["shift_io1"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io1.xen";
    weight_map["shift_io2"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io2.xen";
    weight_map["shift_io3"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io3.xen";
    weight_map["shift_io4"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io4.xen";
    weight_map["shift_io5"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io5.xen";
    weight_map["shift_io6"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io6.xen";
    weight_map["shift_io7"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io7.xen";
    weight_map["shift_io8"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_io8.xen";
    weight_map["shift_w1"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w1.xen";
    weight_map["shift_w2"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w2.xen";
    weight_map["shift_w3"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w3.xen";
    weight_map["shift_w4"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w4.xen";
    weight_map["shift_w5"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w5.xen";
    weight_map["shift_w6"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w6.xen";
    weight_map["shift_w7"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w7.xen";
    weight_map["shift_w8"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/shift_w8.xen";
    weight_map["w1"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w1.xen";
    weight_map["w2"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w2.xen";
    weight_map["w3"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w3.xen";
    weight_map["w4"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w4.xen";
    weight_map["w5"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w5.xen";
    weight_map["w6"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w6.xen";
    weight_map["w7"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w7.xen";
    weight_map["w8"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/Param/xen/w8.xen";

    weight_map["inout_root"] = "/Users/caixc/Documents/Work/Project/IC/NNA/FPGA_MNIST/00_Data/MNIST/xen/";


    Matx<int8_t> w1;
    Matx<int> b1;
    Matx<int> shift_io1, shift_w1, shift_b1;
    w1.load(weight_map["w1"], 4);
    b1.load(weight_map["b1"]);
    shift_io1.load(weight_map["shift_io1"]);
    shift_w1.load(weight_map["shift_w1"]);
    shift_b1.load(weight_map["shift_b1"]);

    Matx<int8_t> w2;
    Matx<int> b2;
    Matx<int> shift_io2, shift_w2, shift_b2;
    w2.load(weight_map["w2"]);
    b2.load(weight_map["b2"]);
    shift_io2.load(weight_map["shift_io2"]);
    shift_w2.load(weight_map["shift_w2"]);
    shift_b2.load(weight_map["shift_b2"]);

    Matx<int8_t> w3;
    Matx<int> b3;
    Matx<int> shift_io3, shift_w3, shift_b3;
    w3.load(weight_map["w3"]);
    b3.load(weight_map["b3"]);
    shift_io3.load(weight_map["shift_io3"]);
    shift_w3.load(weight_map["shift_w3"]);
    shift_b3.load(weight_map["shift_b3"]);

    Matx<int8_t> w4;
    Matx<int> b4;
    Matx<int> shift_io4, shift_w4, shift_b4;
    w4.load(weight_map["w4"]);
    b4.load(weight_map["b4"]);
    shift_io4.load(weight_map["shift_io4"]);
    shift_w4.load(weight_map["shift_w4"]);
    shift_b4.load(weight_map["shift_b4"]);

    Matx<int8_t> w5;
    Matx<int> b5;
    Matx<int> shift_io5, shift_w5, shift_b5;
    w5.load(weight_map["w5"]);
    b5.load(weight_map["b5"]);
    shift_io5.load(weight_map["shift_io5"]);
    shift_w5.load(weight_map["shift_w5"]);
    shift_b5.load(weight_map["shift_b5"]);

    Matx<int8_t> w6;
    Matx<int> b6;
    Matx<int> shift_io6, shift_w6, shift_b6;
    w6.load(weight_map["w6"]);
    b6.load(weight_map["b6"]);
    shift_io6.load(weight_map["shift_io6"]);
    shift_w6.load(weight_map["shift_w6"]);
    shift_b6.load(weight_map["shift_b6"]);

    Matx<int8_t> w7;
    Matx<int> b7;
    Matx<int> shift_io7, shift_w7, shift_b7;
    w7.load(weight_map["w7"]);
    b7.load(weight_map["b7"]);
    shift_io7.load(weight_map["shift_io7"]);
    shift_w7.load(weight_map["shift_w7"]);
    shift_b7.load(weight_map["shift_b7"]);

    Matx<int8_t> w8;
    Matx<int> b8;
    Matx<int> shift_io8, shift_w8, shift_b8;
    w8.load(weight_map["w8"]);
    b8.load(weight_map["b8"]);
    shift_io8.load(weight_map["shift_io8"]);
    shift_w8.load(weight_map["shift_w8"]);
    shift_b8.load(weight_map["shift_b8"]);

    Matx<int8_t> input;
    Matx<int> output;

    // int i = 1;
    // input.load(weight_map["inout_root"] + "input_" + to_string(i) + ".xen", 3);
    // output.load(weight_map["inout_root"] + "output_" + to_string(i) + ".xen", 3);
    // // cout << "conv1" << endl;
    // Matx<int8_t> conv_1 = nn::DConv2D_FPGA(input, shift_io1, w1, shift_w1, b1, shift_b1, 2, 1);
    // Matx<int8_t> conv_2 = nn::PConv2D_FPGA(conv_1, shift_io2, w2, shift_w2, b2, shift_b2);

    // // cout << "conv2" << endl;
    // Matx<int8_t> conv_3 = nn::DConv2D_FPGA(conv_2, shift_io3, w3, shift_w3, b3, shift_b3, 3, 1);
    // Matx<int8_t> conv_4 = nn::PConv2D_FPGA(conv_3, shift_io4, w4, shift_w4, b4, shift_b4);

    // // cout << "conv3" << endl;
    // Matx<int8_t> conv_5 = nn::DConv2D_FPGA(conv_4, shift_io5, w5, shift_w5, b5, shift_b5, 3, 1);
    // Matx<int8_t> conv_6 = nn::PConv2D_FPGA(conv_5, shift_io6, w6, shift_w6, b6, shift_b6);

    // // cout << "conv4" << endl;
    // Matx<int8_t> conv_7 = nn::DConv2D_FPGA(conv_6, shift_io7, w7, shift_w7, b7, shift_b7, 2, 1);
    // Matx<int8_t> conv_8 = nn::PConv2D_FPGA(conv_7, shift_io8, w8, shift_w8, b8, shift_b8);

    // conv_8.show();
    // vector<int> softmax = conv_8.maxval_index();
    // output.show();
    // cout << softmax[1] << endl;


    int correct_num = 0;
    int sum_num = 0;
    for(int i = 0; i < 100; i++) {
        input.load(weight_map["inout_root"] + "input_" + to_string(i) + ".xen", 3);
        // input.load(weight_map["input"], 3);
        output.load(weight_map["inout_root"] + "output_" + to_string(i) + ".xen", 3);
        // cout << "conv1" << endl;
        Matx<int8_t> conv_1 = nn::DConv2D_FPGA(input, shift_io1, w1, shift_w1, b1, shift_b1, 2, 1);
        // conv_1.show();
        Matx<int8_t> conv_2 = nn::PConv2D_FPGA(conv_1, shift_io2, w2, shift_w2, b2, shift_b2);
        // conv_2.show();
        // cout << conv_2.depth() << ", " << conv_2.channel() << ", " << conv_2.rows() << ", " << conv_2.cols() << endl;
        // cout << "conv2" << endl;
        Matx<int8_t> conv_3 = nn::DConv2D_FPGA(conv_2, shift_io3, w3, shift_w3, b3, shift_b3, 3, 1);
        Matx<int8_t> conv_4 = nn::PConv2D_FPGA(conv_3, shift_io4, w4, shift_w4, b4, shift_b4);

        // cout << "conv3" << endl;
        Matx<int8_t> conv_5 = nn::DConv2D_FPGA(conv_4, shift_io5, w5, shift_w5, b5, shift_b5, 3, 1);
        Matx<int8_t> conv_6 = nn::PConv2D_FPGA(conv_5, shift_io6, w6, shift_w6, b6, shift_b6);

        // cout << "conv4" << endl;
        Matx<int8_t> conv_7 = nn::DConv2D_FPGA(conv_6, shift_io7, w7, shift_w7, b7, shift_b7, 2, 1);
        Matx<int8_t> conv_8 = nn::PConv2D_FPGA(conv_7, shift_io8, w8, shift_w8, b8, shift_b8);

        // conv_8.show();
        vector<int> softmax = conv_8.maxval_index();
        // cout << softmax[1] << endl;
        if(softmax[1] == output.ptr[0][0][0][0]) {
            correct_num++;
        }
        sum_num++;
    }
    cout << "acc:" << double(correct_num)/double(sum_num) << endl;
}