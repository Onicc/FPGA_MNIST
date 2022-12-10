
import onnxruntime
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import numpy as np

INDEX = 0
BATCHSIZE = 16
ONNX_MODEL_PATH = "02_Quantization/models/final_model.onnx"

sess = onnxruntime.InferenceSession(ONNX_MODEL_PATH)

mnist = datasets.MNIST("00_Data", train=False)
label = mnist.targets[INDEX].numpy()   # 1
image = mnist.data[INDEX].numpy()       # shape 28x28
# label = np.array([label for i in range(BATCHSIZE)], dtype=np.int32)
image = np.array([[image] for i in range(BATCHSIZE)], dtype=np.float32)
image -= 128
# image *= 2

input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name
output = sess.run([output_name], {input_name : image})
output = np.array(output)
output = np.squeeze(output)
out_label = np.argmax(output, 1)[0]

if(out_label == label):
    print("Pass.")
else:
    print("Fail")

print(output[0])
# [[[3]]
# [[0]]
# [[0]]
# [[15]]
# [[0]]
# [[16]]
# [[0]]
# [[73]]
# [[0]]
# [[20]]]

print(input_name)
# output = sess.run(["PPQ_Variable_5"], {input_name : image})
# print(output)

import onnx
model = onnx.load(ONNX_MODEL_PATH)
model.graph.output.extend([onnx.ValueInfoProto(name="PPQ_Variable_5")])
sess = onnxruntime.InferenceSession(model.SerializeToString())
input_name = sess.get_inputs()[0].name

output_name = sess.get_outputs()[0].name
output1_name = sess.get_outputs()[1].name

#构造输入数据并推理
outputs = sess.run([output1_name], {input_name: image})
outputs = np.array(outputs)
print("Input:")
print(image[0][0])
print("Interlayer:")
print(outputs[0][0][0])