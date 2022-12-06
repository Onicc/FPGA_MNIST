TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)

# # Conv2d parameters
# N ?= 8
# INPUT_CHANNEL ?= 1
# INPUT_SIZE ?= 28
# OUTPUT_CHANNEL ?= 32
# OUTPUT_SIZE ?= 14
# KERNEL_SIZE ?= 3
# STRIDE ?= 2
# PADDING ?= 1
# DILATION ?= 0

# 导入python脚本
export PYTHONPATH := $(PWD)/verify:$(PYTHONPATH)
# export PYTHONPATH := $(PWD)/verify/utils:$(PYTHONPATH)

# 导入Verilog文件
VERILOG_SOURCES = $(PWD)/../rtl/base/*.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/conv_unit.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/dconv.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/pconv_unit.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/pconv.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/padding.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/dwconv.v
VERILOG_SOURCES += $(PWD)/../rtl/top/mnist.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/dwconv_c1.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/pconv_c1.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/pconv_unit_c1.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/dwconv_c6.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/pconv_c6.v
VERILOG_SOURCES += $(PWD)/../rtl/nn/pconv_unit_c6.v

# # 设置参数
# # Set module parameters
# COMPILE_ARGS += \
# 	-P dwconv.N=$(N) \
# 	-P dwconv.INPUT_CHANNEL=$(INPUT_CHANNEL) \
# 	-P dwconv.INPUT_SIZE=$(INPUT_SIZE) \
# 	-P dwconv.OUTPUT_CHANNEL=$(OUTPUT_CHANNEL) \
# 	-P dwconv.OUTPUT_SIZE=$(OUTPUT_SIZE) \
# 	-P dwconv.KERNEL_SIZE=$(KERNEL_SIZE) \
# 	-P dwconv.STRIDE=$(STRIDE) \
# 	-P dwconv.PADDING=$(PADDING) \
# 	-P dwconv.DILATION=$(DILATION)


TOPLEVEL := mnist			# rtl 顶层模块名
MODULE   := conv_unit_test	# verify 验证使用的python脚本名

include $(shell cocotb-config --makefiles)/Makefile.sim
