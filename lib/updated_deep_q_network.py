from __future__ import absolute_import, division, print_function
import chess
import numpy as np
import random
import tensorflow as tf
from tensorflow import keras
from lib.board_operations import serializers
import os

# Define basic parameters
episodes = 50000
network_input = tf.keras.layers.Input(shape=(193,))
hidden_input_layer = tf.keras.layers.Dense(193, activation=tf.nn.relu)(network_input)
hidden_layer_one = tf.keras.layers.Dense(512, activation=tf.nn.relu)(hidden_input_layer)
network_output = tf.keras.layers.Dense(40, activation=tf.nn.softmax)(hidden_layer_one)
model = tf.keras.Model(network_input, network_output)

def get_move(board):
    # Get the prediction
    board_array = serializers.krk_board_to_array(board)
    print(board_array)
    print(network_input)
    try:
        predictions = model(board_array)
    except Exception as e:
        predictions = e
    print(predictions)
    test = tf.argmax(predictions)
    print(test)


    # Return a move
    return predictions