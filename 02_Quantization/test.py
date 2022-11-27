
import onnxruntime
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import numpy as np

BATCHSIZE = 16
ONNX_MODEL_PATH = "02_Quantization/models/final_model.onnx"

sess = onnxruntime.InferenceSession(ONNX_MODEL_PATH)

mnist = datasets.MNIST("00_Data", train=False)
mnist_label = mnist.targets.view(-1, BATCHSIZE).numpy()
# print(mnist_label[0])

mnist_data = mnist.data.view(-1, BATCHSIZE, 1, 28, 28).float()
# print(mnist_data.flatten().numpy().max())
mnist_data -= 128
dataset_len = mnist_data.shape[0]

input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

coorect = 0
total = 0
for image, label in zip(mnist_data, mnist_label):
    output = sess.run([output_name], {input_name : image.numpy()})
    out = np.array(output)
    out = np.squeeze(out)
    out = np.argmax(out, 1)
    coorect += (out == label).sum()
    total += label.shape[0]
print("acc: ", coorect/total)