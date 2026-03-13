# Author: Lukas Frotton
# Netid: ljf109
# Aid: https://docs.pytorch.org/docs/stable/index.html

# import stuff
import sys
import numpy
import torch
from PIL import Image

d = sys.argv[1].rsplit('/', 1)[0] if '/' in sys.argv[1] else '.'
pt = lambda n: torch.load(f'{d}/{n}', weights_only=True)

w0, w1, w2 = pt('weight0.pt'), pt('weight1.pt'), pt('weight2.pt')
b0, b1, b2 = pt('bias0.pt'), pt('bias1.pt'), pt('bias2.pt')
w3, w4 = pt('weight3.pt'), pt('weight4.pt')
b3, b4 = pt('bias3.pt'), pt('bias4.pt')
#
X = torch.tensor(numpy.array(Image.open(sys.argv[1]))/255).view(1, 28, 28).float()

# Custom conv layer
def conv2d(x, w, b, stride=2):
    C_in, H, W = x.shape
    C_out, _, kH, kW = w.shape
    H_out = (H - kH) // stride + 1
    W_out = (W - kW) // stride + 1
    out = torch.zeros(C_out, H_out, W_out)
    for co in range(C_out):
        for i in range(H_out):
            for j in range(W_out):
                out[co, i, j] = (w[co] * x[:, i*stride:i*stride+kH, j*stride:j*stride+kW]).sum() + b[co]
    return out

def relu(x):
    return torch.clamp(x, min=0)


# pass through relu network
x = relu(conv2d(X, w0, b0))
x = relu(conv2d(x, w1, b1))
x = relu(conv2d(x, w2, b2))
x = x.flatten()
x = x @ w3.T + b3
out = x @ w4.T + b4

# softmax for prob

decision = torch.nn.Softmax(dim=0)
y_hat = decision(out)
prediction = torch.argmax(y_hat)
confidence = y_hat[prediction]

# done do predict
print(f"Prediction is {prediction} with confidence {confidence:3f}")