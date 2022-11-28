import numpy as np

import cocotb
from cocotb.triggers import Timer, RisingEdge, ClockCycles
from collections import deque
from cocotb.binary import BinaryValue

from conv_model import mnist

N = 8

class ClockDomain(object):
    """产生时钟和复位信号
    """
    def __init__(self, clkSig, period, unit, resetSig=None, resetActiveHigh = True):
        """Init
        Args:
            clkSig: 时钟信号
            period: 时钟周期
            unit: 事件单位(timeunit)
            resetSig: 复位信号
            resetActiveHigh: 复位信号为高电平有效还是低电平有效
        """
        self.clk = clkSig
        self.reset = resetSig
        self.period = period
        self.unit = unit
        self.resetActiveHigh = resetActiveHigh
    
    async def doReset(self):
        """复位操作
        
        复位信号复位十个时钟周期后解复位
    
        cocotb基于协程方式运行,我们跨周期的驱动接口信号需将函数声明为协程,添加async声明
        """
        clcokCycle = ClockCycles(self.clk, 10, True)
        if(self. resetActiveHigh):
            self.reset.value = 1
        else:
            self.reset.value = 0

        await clcokCycle

        if(self.resetActiveHigh):
            self.reset.value = 0
        else:
            self.reset.value = 1

    async def genClk(self):
        """产生时钟

        genClk函数我们用于产生时钟信号,也添加async声明。这里根据指定的时钟周期驱动生成时钟信号
        """
        self.clk.setimmediatevalue(0)
        while True:
            await Timer(self. period/2, self.unit)
            self.clk.setimmediatevalue(1)
            await Timer(self. period/2, self.unit)
            self.clk.setimmediatevalue(0)

    async def start(self):
        """打开时钟和复位信号

        start()函数用于触发生成复位和时钟,这里通过cocotb.fork函数调用doRest及genClk分别产生时钟与复位信号
        """
        clockTh = cocotb.fork(self.genClk())
        resetTh = cocotb.fork(self.doReset())
        await resetTh.join()    # 等待复位信号执行完毕
        return clockTh

class Conv2dDrive(object):
    """模型驱动,负责控制模型的输入输出及验证

    """
    def __init__(self, clk, rst_n, ce, input_vld, input_din, 
                dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
                dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
                dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
                dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4, \
                conv_dout, conv_dout_vld, conv_dout_end):
        # system
        self.clk = clk
        self.rst_n = rst_n
        # input
        self.ce = ce
        self.input_vld = input_vld
        self.input_din = input_din
        self.dconv_weight_din_1 = dconv_weight_din_1
        self.pconv_weight_din_1 = pconv_weight_din_1
        self.dconv_bias_din_1 = dconv_bias_din_1
        self.pconv_bias_din_1 = pconv_bias_din_1
        self.dconv_shift_din_1 = dconv_shift_din_1
        self.pconv_shift_din_1 = pconv_shift_din_1

        self.dconv_weight_din_2 = dconv_weight_din_2
        self.pconv_weight_din_2 = pconv_weight_din_2
        self.dconv_bias_din_2 = dconv_bias_din_2
        self.pconv_bias_din_2 = pconv_bias_din_2
        self.dconv_shift_din_2 = dconv_shift_din_2
        self.pconv_shift_din_2 = pconv_shift_din_2

        self.dconv_weight_din_3 = dconv_weight_din_3
        self.pconv_weight_din_3 = pconv_weight_din_3
        self.dconv_bias_din_3 = dconv_bias_din_3
        self.pconv_bias_din_3 = pconv_bias_din_3
        self.dconv_shift_din_3 = dconv_shift_din_3
        self.pconv_shift_din_3 = pconv_shift_din_3

        self.dconv_weight_din_4 = dconv_weight_din_4
        self.pconv_weight_din_4 = pconv_weight_din_4
        self.dconv_bias_din_4 = dconv_bias_din_4
        self.pconv_bias_din_4 = pconv_bias_din_4
        self.dconv_shift_din_4 = dconv_shift_din_4
        self.pconv_shift_din_4 = pconv_shift_din_4
        # output
        self.conv_dout = conv_dout
        self.conv_dout_vld = conv_dout_vld
        self.conv_dout_end = conv_dout_end
        # input init
        self.ce.setimmediatevalue(1)
        self.input_vld.setimmediatevalue(0)
        self.input_din.setimmediatevalue(0)

        self.dconv_weight_din_1.setimmediatevalue(0)
        self.pconv_weight_din_1.setimmediatevalue(0)
        self.dconv_bias_din_1.setimmediatevalue(0)
        self.pconv_bias_din_1.setimmediatevalue(0)
        self.dconv_shift_din_1.setimmediatevalue(0)
        self.pconv_shift_din_1.setimmediatevalue(0)

        self.dconv_weight_din_2.setimmediatevalue(0)
        self.pconv_weight_din_2.setimmediatevalue(0)
        self.dconv_bias_din_2.setimmediatevalue(0)
        self.pconv_bias_din_2.setimmediatevalue(0)
        self.dconv_shift_din_2.setimmediatevalue(0)
        self.pconv_shift_din_2.setimmediatevalue(0)

        self.dconv_weight_din_3.setimmediatevalue(0)
        self.pconv_weight_din_3.setimmediatevalue(0)
        self.dconv_bias_din_3.setimmediatevalue(0)
        self.pconv_bias_din_3.setimmediatevalue(0)
        self.dconv_shift_din_3.setimmediatevalue(0)
        self.pconv_shift_din_3.setimmediatevalue(0)

        self.dconv_weight_din_4.setimmediatevalue(0)
        self.pconv_weight_din_4.setimmediatevalue(0)
        self.dconv_bias_din_4.setimmediatevalue(0)
        self.pconv_bias_din_4.setimmediatevalue(0)
        self.dconv_shift_din_4.setimmediatevalue(0)
        self.pconv_shift_din_4.setimmediatevalue(0)

        # input output deque
        self.input_weight = deque()
        self.model_output = deque()
        self.expected_output = 0
        # self.model_output = ""
        self.sum_event = 0
        self.true_event = 0

    async def input_driver(self):
        edge = RisingEdge(self.clk)
        while True:
            if(len(self.input_weight)):
                cocotb.log.info("get a transaction in Input Driver")
                input_din, \
                dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
                dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
                dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
                dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4 = self.input_weight.popleft()

                for element in input_din:
                    self.input_vld.value = 1                                # 设置输入有效
                    self.input_din.value = BinaryValue(element)             # 设置data1

                    self.dconv_weight_din_1.value = BinaryValue(dconv_weight_din_1)
                    self.pconv_weight_din_1.value = BinaryValue(pconv_weight_din_1)
                    self.dconv_bias_din_1.value = BinaryValue(dconv_bias_din_1)
                    self.pconv_bias_din_1.value = BinaryValue(pconv_bias_din_1)
                    self.dconv_shift_din_1.value = BinaryValue(dconv_shift_din_1)
                    self.pconv_shift_din_1.value = BinaryValue(pconv_shift_din_1)

                    self.dconv_weight_din_2.value = BinaryValue(dconv_weight_din_2)
                    self.pconv_weight_din_2.value = BinaryValue(pconv_weight_din_2)
                    self.dconv_bias_din_2.value = BinaryValue(dconv_bias_din_2)
                    self.pconv_bias_din_2.value = BinaryValue(pconv_bias_din_2)
                    self.dconv_shift_din_2.value = BinaryValue(dconv_shift_din_2)
                    self.pconv_shift_din_2.value = BinaryValue(pconv_shift_din_2)

                    self.dconv_weight_din_3.value = BinaryValue(dconv_weight_din_3)
                    self.pconv_weight_din_3.value = BinaryValue(pconv_weight_din_3)
                    self.dconv_bias_din_3.value = BinaryValue(dconv_bias_din_3)
                    self.pconv_bias_din_3.value = BinaryValue(pconv_bias_din_3)
                    self.dconv_shift_din_3.value = BinaryValue(dconv_shift_din_3)
                    self.pconv_shift_din_3.value = BinaryValue(pconv_shift_din_3)

                    self.dconv_weight_din_4.value = BinaryValue(dconv_weight_din_4)
                    self.pconv_weight_din_4.value = BinaryValue(pconv_weight_din_4)
                    self.dconv_bias_din_4.value = BinaryValue(dconv_bias_din_4)
                    self.pconv_bias_din_4.value = BinaryValue(pconv_bias_din_4)
                    self.dconv_shift_din_4.value = BinaryValue(dconv_shift_din_4)
                    self.pconv_shift_din_4.value = BinaryValue(pconv_shift_din_4)

                    await edge                                              # 等待上升沿
                    self.input_vld.value = 0                                # 关闭输入有效
                    # for i in range(19):
                    for i in range(N + 3):
                        await edge                                          # 等待上升沿
            else:
                await edge

    async def output_monitor(self):
        edge = RisingEdge(self.clk)
        while True:
            if(self.conv_dout_vld.value and self.conv_dout_end == 0):
                self.model_output.appendleft(self.conv_dout.value)
            await edge

    async def wait_completion(self):
        edge = RisingEdge(self.conv_dout_end)
        await edge
        cocotb.log.info("get a transaction in Output Monitor")


    def add_input_output(self, input_din, verift_model_output, \
                        dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
                        dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
                        dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
                        dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4):
        self.input_weight.append((input_din, \
                                dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
                                dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
                                dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
                                dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4))
        self.expected_output = int(verift_model_output)

    def check(self):
        self.model_output.reverse()
        model_output_bin = []
        for i, d in enumerate(self.model_output):
            model_output_bin.append(str(d))
        # print(model_output_bin)
        model_output = []
        for i in range(10):
            model_output.append(model_output_bin[0][i*8:(i+1)*8])
        model_output = [int(d, 2) for d in model_output]
        model_output = np.array(model_output)

        self.sum_event += 1
        print("------------------------------------------------")
        if(model_output.argmax() == self.expected_output):
            self.true_event += 1
            print("\033[32m model output: {} , expected output: {} \033[0m".format(model_output.argmax(), self.expected_output))
        else:
            print("\033[31m model output: {} , expected output: {} \033[0m".format(model_output.argmax(), self.expected_output))
        print("\033[32m true: {} \033[0m".format(self.true_event/self.sum_event))
        print("------------------------------------------------")

        # assert self.expected_output == model_output.argmax()

        self.model_output.clear()
        
        
class conv2d_tb(object):
    def __init__(self, dut):
        self.dut = dut
        self.model_drive = Conv2dDrive(dut.clk, dut.rst_n, dut.ce, dut.input_vld, dut.input_din, 
            dut.dconv_weight_din_1, dut.pconv_weight_din_1, dut.dconv_bias_din_1, dut.pconv_bias_din_1, dut.dconv_shift_din_1, dut.pconv_shift_din_1, \
            dut.dconv_weight_din_2, dut.pconv_weight_din_2, dut.dconv_bias_din_2, dut.pconv_bias_din_2, dut.dconv_shift_din_2, dut.pconv_shift_din_2, \
            dut.dconv_weight_din_3, dut.pconv_weight_din_3, dut.dconv_bias_din_3, dut.pconv_bias_din_3, dut.dconv_shift_din_3, dut.pconv_shift_din_3, \
            dut.dconv_weight_din_4, dut.pconv_weight_din_4, dut.dconv_bias_din_4, dut.pconv_bias_din_4, dut.dconv_shift_din_4, dut.pconv_shift_din_4, \
            dut.conv_dout, dut.conv_dout_vld, dut.conv_dout_end)
        self.clock_ctrl = ClockDomain(self.dut.clk, 10, 'ns', self.dut.rst_n, False)

    async def init(self):
        self.input_driver_thread = cocotb.fork(self.model_drive.input_driver())
        self.output_monitor_thread = cocotb.fork(self.model_drive.output_monitor())
        self.clock_thread = await self.clock_ctrl.start()

    def stop(self):
        self.input_driver_thread.kill()
        self.output_monitor_thread.kill()
        self.clock_thread.kill()

@cocotb.test()
async def run_test(dut):
    tb = conv2d_tb(dut)
    await tb.init()

    # input_din, verift_model_output, \
    # dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
    # dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
    # dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
    # dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4  = mnist(1, bitwidth = N)
    # tb.model_drive.add_input_output(input_din, verift_model_output, \
    #                                 dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
    #                                 dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
    #                                 dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
    #                                 dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4)
    # await tb.model_drive.wait_completion()
    # tb.model_drive.check()

    # await Timer(500, "ns")

    for i in range(0, 10000):
        print("{}th".format(i))
        input_din, verift_model_output, \
        dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
        dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
        dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
        dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4  = mnist(i, bitwidth = N)
        tb.model_drive.add_input_output(input_din, verift_model_output, \
                                        dconv_weight_din_1, pconv_weight_din_1, dconv_bias_din_1, pconv_bias_din_1, dconv_shift_din_1, pconv_shift_din_1, \
                                        dconv_weight_din_2, pconv_weight_din_2, dconv_bias_din_2, pconv_bias_din_2, dconv_shift_din_2, pconv_shift_din_2, \
                                        dconv_weight_din_3, pconv_weight_din_3, dconv_bias_din_3, pconv_bias_din_3, dconv_shift_din_3, pconv_shift_din_3, \
                                        dconv_weight_din_4, pconv_weight_din_4, dconv_bias_din_4, pconv_bias_din_4, dconv_shift_din_4, pconv_shift_din_4)
        await tb.model_drive.wait_completion()
        tb.model_drive.check()

    await Timer(200, "us")
    tb.stop()
    
