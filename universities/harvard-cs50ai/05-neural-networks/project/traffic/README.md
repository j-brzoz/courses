# Models

## Model from recogintion.py
1 Convolutional layer learning 32 filters using a 3x3 kernel + max-pooling layer, using 2x2 pool size + a dense hidden layer with 128 units and 50% dropout

### Results
Epoch 1/10- loss: 2.2900 - accuracy: 0.3858\
Epoch 2/10 - loss: 1.0440 - accuracy: 0.6908\
Epoch 3/10 - loss: 0.6905 - accuracy: 0.7938\
Epoch 4/10 - loss: 0.5432 - accuracy: 0.8373\
Epoch 5/10 - loss: 0.4441 - accuracy: 0.8632\
Epoch 6/10 - loss: 0.3885 - accuracy: 0.8819\
Epoch 7/10 - loss: 0.3485 - accuracy: 0.8889\
Epoch 8/10 - loss: 0.3196 - accuracy: 0.8989\
Epoch 9/10 - loss: 0.2862 - accuracy: 0.9088\
Epoch 10/10 - loss: 0.2618 - accuracy: 0.9179\
**333/333 - 2s - loss: 0.1197 - accuracy: 0.9711 - 2s/epoch - 5ms/step**

## Model from recogintion.py with doubled unit size
1 Convolutional layer learning 32 filters using a 3x3 kernel + max-pooling layer, using 2x2 pool size + a dense hidden layer with 256 units and 50% dropout

### Results
Epoch 1/10 - loss: 1.8746 - accuracy: 0.4950\
Epoch 2/10 - loss: 0.7011 - accuracy: 0.7969\
Epoch 3/10 - loss: 0.4386 - accuracy: 0.8685\
Epoch 4/10 - loss: 0.3284 - accuracy: 0.9055\
Epoch 5/10p - loss: 0.2712 - accuracy: 0.9216\
Epoch 6/10p - loss: 0.2193 - accuracy: 0.9335\
Epoch 7/10 - loss: 0.1915 - accuracy: 0.9419\
Epoch 8/10 - loss: 0.1729 - accuracy: 0.9462\
Epoch 9/10 - loss: 0.1510 - accuracy: 0.9555\
Epoch 10/10 - loss: 0.1419 - accuracy: 0.9566\
**333/333 - 2s - loss: 0.0931 - accuracy: 0.9771 - 2s/epoch - 7ms/step**\
**The same as previous model!**

## Model from recogintion.py with doubled unit size with 2 sequential sets of layers
2x(1 Convolutional layer learning 32 filters using a 3x3 kernel + max-pooling layer, using 2x2 pool size) + a dense hidden layer with 256 units and 50% dropout

### Results
Epoch 1/10 - loss: 1.8213 - accuracy: 0.5080\
Epoch 2/10 - loss: 0.6467 - accuracy: 0.8132\
Epoch 3/10 - loss: 0.4070 - accuracy: 0.8820\
Epoch 4/10 - loss: 0.3102 - accuracy: 0.9118\
Epoch 5/10 - loss: 0.2442 - accuracy: 0.9271\
Epoch 6/10 - loss: 0.2154 - accuracy: 0.9359\
Epoch 7/10 - loss: 0.1948 - accuracy: 0.9427\
Epoch 8/10 - loss: 0.1709 - accuracy: 0.9473\
Epoch 9/10 - loss: 0.1508 - accuracy: 0.9546\
Epoch 10/10 - loss: 0.1398 - accuracy: 0.9584\
**333/333 - 2s - loss: 0.1023 - accuracy: 0.9749 - 2s/epoch - 7ms/step**\
**Similar result!**