# System Modules
import chess
import numpy as np
import tensorflow as tf


# Custom Modules
import state_action_table_generator as satg
from lib.board_operations import generators
from lib.board_operations import serializers


#define basic parameters
epochs = 50000
white_input_size, black_input_size, white_hlayer_size, black_hlayer_size, hlayer_one_size, output_size = 193, 193, 193, 193, 512, satg.ACTIONS.count
learning_rate = 0.8
discount_factor = 0.95
w_white_hlayer = np.random.uniform(size=(white_input_size, white_hlayer_size))
w_black_hlayer = np.random.uniform(size=(black_input_size, black_hlayer_size))
w_hlayer_one = np.random.uniform(size=(white_hlayer_size + black_hlayer_size, hlayer_one_size))
w_output = np.random.uniform(size=(hlayer_one_size, output_size))


# A function for training the Deep Q-Network.
def train(white_inputs, black_inputs, target_states):
    # Push the data forward into the network.
    white_hidden = tf.sigmoid(np.dot(white_inputs, w_white_hlayer))  # Feed through the first hidden layer for white.
    black_hidden = tf.sigmoid(np.dot(black_inputs, w_black_hlayer))  # Feed through the first hidden layer for black.
    l_one_hidden = tf.sigmoid(np.dot(np.concatenate((white_hidden, black_hidden), axis=None), w_hlayer_one)) # Feed both hidden layers through connected layer.
    output = np.dot(l_one_hidden, w_output)

    # Calculate the error.


    # Backpropagate through the network.


    return None


# The feed forward function for our network.
# This will take the inputs for white and black and feed them into the network.
def forward(white_inputs, black_inputs):
    # Push the data forward into the network.
    white_hidden = tf.sigmoid(np.dot(white_inputs, w_white_hlayer))  # Feed through the first hidden layer for white.
    black_hidden = tf.sigmoid(np.dot(black_inputs, w_black_hlayer))  # Feed through the first hidden layer for black.
    l_one_hidden = tf.sigmoid(np.dot(np.concatenate((white_hidden, black_hidden), axis=None), w_hlayer_one)) # Feed both hidden layers through connected layer.
    output = np.dot(l_one_hidden, w_output)
    return output


# A function for backpropagation of the neural network.
def backprop():
    return None