
import onnxruntime
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import numpy as np

INDEX = 1
BATCHSIZE = 16
ONNX_MODEL_PATH = "02_Quantization/models/final_model.onnx"

# dataloader
mnist = datasets.MNIST("00_Data", train=False)
label = mnist.targets[INDEX].numpy()   # 1
image = mnist.data[INDEX].numpy()       # shape 28x28
# label = np.array([label for i in range(BATCHSIZE)], dtype=np.int32)
image = np.array([[image] for i in range(BATCHSIZE)], dtype=np.float32)
image -= 128

layer_name = "PPQ_Variable_14"

import onnx
model = onnx.load(ONNX_MODEL_PATH)
model.graph.output.extend([onnx.ValueInfoProto(name=layer_name)])
sess = onnxruntime.InferenceSession(model.SerializeToString())
input_name = sess.get_inputs()[0].name

output_name = sess.get_outputs()[0].name
output1_name = sess.get_outputs()[1].name

#构造输入数据并推理
outputs = sess.run([output1_name], {input_name: image})
outputs = np.array(outputs)
print("Input:")
print(image[0][0])
print(layer_name)
print(outputs[0][0])