# model/cnn_model.py

import tensorflow as tf

class VisualCustomCNN(tf.Module):
    def __init__(self):
        super().__init__()
        initializer = tf.initializers.GlorotUniform()

        self.w1 = tf.Variable(initializer([3, 3, 3, 32]), trainable=True)
        self.b1 = tf.Variable(tf.zeros([32]), trainable=True)

        self.w2 = tf.Variable(initializer([3, 3, 32, 64]), trainable=True)
        self.b2 = tf.Variable(tf.zeros([64]), trainable=True)

        self.w3 = tf.Variable(initializer([3, 3, 64, 128]), trainable=True)
        self.b3 = tf.Variable(tf.zeros([128]), trainable=True)

    def __call__(self, x):
        visualizations = []

        x = tf.nn.conv2d(x, self.w1, strides=1, padding='SAME')
        x = tf.nn.bias_add(x, self.b1)
        x = tf.nn.relu(x)
        visualizations.append(("Conv1 + ReLU", x))

        x = tf.nn.max_pool2d(x, ksize=2, strides=2, padding='SAME')
        visualizations.append(("MaxPool1", x))

        x = tf.nn.conv2d(x, self.w2, strides=1, padding='SAME')
        x = tf.nn.bias_add(x, self.b2)
        x = tf.nn.relu(x)
        visualizations.append(("Conv2 + ReLU", x))

        x = tf.nn.max_pool2d(x, ksize=2, strides=2, padding='SAME')
        visualizations.append(("MaxPool2", x))

        x = tf.nn.conv2d(x, self.w3, strides=1, padding='SAME')
        x = tf.nn.bias_add(x, self.b3)
        x = tf.nn.relu(x)
        visualizations.append(("Conv3 + ReLU", x))

        x = tf.nn.max_pool2d(x, ksize=2, strides=2, padding='SAME')
        visualizations.append(("MaxPool3", x))

        return x, visualizations