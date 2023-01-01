
import onnx
import numpy as np

from onnxtool.onnx_graph import OnnxGraph
import xen.xen as xen

dictionary = {
    "shift_input1" : "PPQ_Variable_3",
    "w1" : "onnx::Conv_74",
    "shift_w1" : "PPQ_Variable_6",
    "b1" : "onnx::Conv_75",
    "shift_b1" : "PPQ_Variable_9",

    "shift_input2" : "PPQ_Variable_15",
    "w2" : "onnx::Conv_77",
    "shift_w2" : "PPQ_Variable_18",
    "b2" : "onnx::Conv_78",
    "shift_b2" : "PPQ_Variable_21",

    "shift_input3" : "PPQ_Variable_27", 
    "w3" : "onnx::Conv_80", 
    "shift_w3" : "PPQ_Variable_30", 
    "b3" : "onnx::Conv_81", 
    "shift_b3" : "PPQ_Variable_33",

    "shift_input4" : "PPQ_Variable_39", 
    "w4" : "onnx::Conv_83", 
    "shift_w4" : "PPQ_Variable_42", 
    "b4" : "onnx::Conv_84", 
    "shift_b4" : "PPQ_Variable_45",

    "shift_input5" : "PPQ_Variable_51", 
    "w5" : "onnx::Conv_86", 
    "shift_w5" : "PPQ_Variable_54", 
    "b5" : "onnx::Conv_87", 
    "shift_b5" : "PPQ_Variable_57",

    "shift_input6" : "PPQ_Variable_63", 
    "w6" : "onnx::Conv_89", 
    "shift_w6" : "PPQ_Variable_66", 
    "b6" : "onnx::Conv_90", 
    "shift_b6" : "PPQ_Variable_69",

    "shift_input7" : "PPQ_Variable_75", 
    "w7" : "onnx::Conv_92", 
    "shift_w7" : "PPQ_Variable_78", 
    "b7" : "onnx::Conv_93", 
    "shift_b7" : "PPQ_Variable_81",

    "shift_input8" : "PPQ_Variable_87", 
    "w8" : "onnx::Conv_95", 
    "shift_w8" : "PPQ_Variable_90", 
    "b8" : "onnx::Conv_96", 
    "shift_b8" : "PPQ_Variable_93",

    "shift_input9" : "PPQ_Variable_99"
}


dictionary_branch = {
    "shift_input1" : "PPQ_Variable_3",
    "w1" : "onnx::Conv_93",
    "shift_w1" : "PPQ_Variable_6",
    "b1" : "onnx::Conv_94",
    "shift_b1" : "PPQ_Variable_9",

    "shift_input2" : "PPQ_Variable_15",
    "w2" : "onnx::Conv_96",
    "shift_w2" : "PPQ_Variable_18",
    "b2" : "onnx::Conv_97",
    "shift_b2" : "PPQ_Variable_21",

    "shift_input3" : "PPQ_Variable_27", 
    "w3" : "onnx::Conv_99", 
    "shift_w3" : "PPQ_Variable_30", 
    "b3" : "onnx::Conv_100", 
    "shift_b3" : "PPQ_Variable_33",

    "shift_input4" : "PPQ_Variable_39", 
    "w4" : "onnx::Conv_102", 
    "shift_w4" : "PPQ_Variable_42", 
    "b4" : "onnx::Conv_103", 
    "shift_b4" : "PPQ_Variable_45",

    "shift_input5" : "PPQ_Variable_51", 
    "w5" : "onnx::Conv_105", 
    "shift_w5" : "PPQ_Variable_54", 
    "b5" : "onnx::Conv_106", 
    "shift_b5" : "PPQ_Variable_57",

    "shift_input6" : "PPQ_Variable_63", 
    "w6" : "onnx::Conv_108", 
    "shift_w6" : "PPQ_Variable_66", 
    "b6" : "onnx::Conv_109", 
    "shift_b6" : "PPQ_Variable_69",

    "shift_input7" : "PPQ_Variable_75", 
    "w7" : "onnx::Conv_111", 
    "shift_w7" : "PPQ_Variable_78", 
    "b7" : "onnx::Conv_112", 
    "shift_b7" : "PPQ_Variable_81",

    "shift_input8" : "PPQ_Variable_87", 
    "w8" : "onnx::Conv_114", 
    "shift_w8" : "PPQ_Variable_90", 
    "b8" : "onnx::Conv_115", 
    "shift_b8" : "PPQ_Variable_93",

    "shift_input9" : "PPQ_Variable_117", 
    "w9" : "onnx::Conv_117", 
    "shift_w9" : "PPQ_Variable_120", 
    "b9" : "onnx::Conv_118", 
    "shift_b9" : "PPQ_Variable_123",

    "shift_input10" : "PPQ_Variable_129", 
    "w10" : "onnx::Conv_120", 
    "shift_w10" : "PPQ_Variable_132", 
    "b10" : "onnx::Conv_121", 
    "shift_b10" : "PPQ_Variable_135",

    "shift_input11" : "PPQ_Variable_141"
}

ONNX_MODEL_PATH = "02_Quantization/models/[Net_DW_Branch]final_model.onnx"
PARAM_NPY_PATH = "00_Data/Param/npy"
PARAM_XEN_PATH = "00_Data/Param/xen"

model = onnx.load(ONNX_MODEL_PATH)
onnx_graph = OnnxGraph(model.graph)

for item in dictionary.items():
    np.save(PARAM_NPY_PATH + "/" + item[0] + ".npy", onnx_graph.initializers[item[1]].to_numpy())
    # print(item[0], onnx_graph.initializers[item[1]].to_numpy())
xen.auto_gen_xen(PARAM_NPY_PATH, PARAM_XEN_PATH)