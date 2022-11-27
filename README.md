# FPGA_MNIST
FPGA implements mnist handwritten font recognition acceleration.

# Structure

## 00 Data
存放数据集、权重(xen、npy)和coe文件

## 01 Model
包含模型构建、训练和torch环境下模型测试

## 02 Quantization
包含模型量化和量化后onnx测试

## 03 Parameter
量化后模型的参数导出，提供给C++测试和FPGA测试使用

## 04 C++ Simulation
C++平台根据量化模式(power of 2)设计推理网络

## 05 Cocotb Simulation
verilog根据量化模式(power of 2)设计rtl电路，在cocotb平台仿真电路

## 06 FPGA Verification
FPGA中验证整个推理过程