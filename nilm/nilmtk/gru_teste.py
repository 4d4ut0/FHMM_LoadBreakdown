import numpy as np
import pandas as pd
import math
import sklearn
import sklearn.preprocessing
import datetime
import os
import matplotlib.pyplot as plt
import tensorflow.compat.v1 as tf

valid_set_size_percentage = 10
test_set_size_percentage = 10
seq_len = 20


def load_data(stock, seq_len):
    data_raw = stock.as_matrix()
    data = []
    for index in range(len(data_raw) - seq_len):
        data.append(data_raw[index: index + seq_len])
    data = np.array(data)
    valid_set_size = int(np.round(valid_set_size_percentage/100*data.shape[0]))
    test_set_size = int(np.round(test_set_size_percentage/100*data.shape[0]))
    train_set_size = data.shape[0] - (valid_set_size + test_set_size)
    x_train = data[:train_set_size, :-1, :]
    y_train = data[:train_set_size, -1, :]
    x_valid = data[train_set_size:train_set_size+valid_set_size, :-1, :]
    y_valid = data[train_set_size:train_set_size+valid_set_size, -1, :]
    x_test = data[train_set_size+valid_set_size:, :-1, :]
    y_test = data[train_set_size+valid_set_size:, -1, :]
    return [x_train, y_train, x_valid, y_valid, x_test, y_test]


def normalize_data(df):
    min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    df['Open'] = min_max_scaler.fit_transform(df.Open.values.reshape(-1, 1))
    df['High'] = min_max_scaler.fit_transform(df.High.values.reshape(-1, 1))
    df['Low'] = min_max_scaler.fit_transform(df.Low.values.reshape(-1, 1))
    df['Close'] = min_max_scaler.fit_transform(df['Close'].values.reshape(-1, 1))
    return df


# pegando os dados
dataset = pd.read_csv('RELIANCE2000-01-012017-10-29.csv', index_col=0)
df_stock = dataset.copy()
df_stock = df_stock.dropna()
df_stock = df_stock[['Open', 'High', 'Low', 'Close']]


# Normalizando
df_stock_norm = df_stock.copy()
df_stock_norm = normalize_data(df_stock_norm)


# Setando dados $ parametros & placeholders
x_train, y_train, x_valid, y_valid, x_test, y_test = load_data(df_stock_norm, seq_len)
n_steps = seq_len-1
n_inputs = 4
n_neurons = 200
n_outputs = 4
n_layers = 2
learning_rate = 0.001
batch_size = 1
n_epochs = 100
train_set_size = x_train.shape[0]
test_set_size = x_test.shape[0]
tf.disable_v2_behavior()
X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
Y = tf.placeholder(tf.float32, [None, n_outputs])

index_in_epoch = 0
perm_array = np.arange(x_train.shape[0])
np.random.shuffle(perm_array)


def get_next_batch(batch_size):
    global index_in_epoch, x_train, perm_array
    start = index_in_epoch
    index_in_epoch += batch_size
    if index_in_epoch > x_train.shape[0]:
        np.random.shuffle(perm_array)
        start = 0
        index_in_epoch = batch_size
    end = index_in_epoch
    return x_train[perm_array[start:end]], y_train[perm_array[start:end]]


# RNN
# layers = [tf.contrib.rnn.BasicRNNCell(num_units=n_neurons, activation=tf.nn.elu) for layer in range(n_layers)]

# LSTM
# layers = [tf.contrib.rnn.BasicLSTMCell(num_units=n_neurons, activation=tf.nn.elu) for layer in range(n_layers)]

# LSTM with peephole connections
# layers = [tf.contrib.rnn.BasicRNNCell(num_units=n_neurons, activation=tf.nn.leaky_relu, use_peepholes=True) for layer in range(n_layers)]

# GRU
layers = [tf.nn.rnn_cell.GRUCell(num_units=n_neurons, activation=tf.nn.leaky_relu) for layer in range(n_layers)]


multi_layer_cell = tf.nn.rnn_cell.MultiRNNCell(layers)
rnn_outputs, states = tf.nn.dynamic_rnn(multi_layer_cell, X, dtype=tf.float32)
stacked_outputs = tf.reshape(rnn_outputs, [-1, n_neurons])
outputs = tf.reshape(stacked_outputs, [-1, n_steps, n_outputs])
outputs = outputs[:, n_steps-1, :]


# Função custo
loss = tf.reduce_mean(tf.square(outputs - Y))


# Optimizer
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(loss)


# Fitting
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for iteration in range(int(n_epochs*train_set_size/batch_size)):
        x_batch, y_batch = get_next_batch(batch_size)
        sess.run(training_op, feed_dict={X: x_batch, Y: y_batch})
        if iteration % int(5*train_set_size/batch_size) == 0:
            mse_train = loss.eval(feed_dict={X: x_train, Y: y_train})
            mse_valid = loss.eval(feed_dict={X: x_valid, Y: y_valid})
            print('%.2f epochs: MSE train/valid = %.6f/%.6f' %
                  (iteration*batch_size/train_set_size, mse_train, mse_valid))

# Predicoes
    y_test_pred = sess.run(outputs, feed_dict={X: x_test})


# Grafico
comp = pd.DataFrame({'Column1': y_test[:, 3], 'Column2': y_test_pred[:, 3]})
plt.figure(figsize=(10, 5))
plt.plot(comp['Column1'], color='blue', label='Original')
plt.plot(comp['Column2'], color='black', label='Predição')
plt.legend()
plt.show()
