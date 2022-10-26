import numpy as np
import math as m
from random import randint
from copy import deepcopy


def sigmoid(inp):
    return 1 / (1 + m.e ** (-inp))


def get_random(acc):
    return randint(-acc, acc) / acc


class Net2:
    def __init__(self, **kwargs):
        self.acc = 1000
        self.net = []
        self.bias = []
        self.layers = 1
        self.decisions = [0, 1]
        self.decisions_am = len(self.decisions)
        self.input_am = 2
        self.neurons_per_layer = [self.input_am for a in range(self.layers)]
        self.pattern = False

        if "layers" in kwargs:
            self.layers = kwargs["layers"]
            if self.layers < 1:
                self.layers = 1
            self.neurons_per_layer = [self.input_am for a in range(self.layers)]

        if "dec" in kwargs:
            self.decisions = kwargs["dec"]
            self.decisions_am = len(self.decisions)

        if "inp_am" in kwargs:
            self.input_am = kwargs["inp_am"]

        if "npl" in kwargs:
            self.neurons_per_layer = [kwargs["npl"] for a in range(self.layers)]
            if self.neurons_per_layer[0] < 1:
                self.neurons_per_layer = [4 for a in range(self.layers)]

        if "bias" in kwargs:
            self.bias = []
            self.neurons_per_layer = []
            for layer in kwargs["bias"]:
                self.bias.append(np.array(layer))
                self.neurons_per_layer.append(len(layer))
            self.layers = len(self.bias)

        if "pattern" in kwargs:
            self.layers = len(kwargs["pattern"])
            self.neurons_per_layer = []
            for a in range(self.layers):
                self.neurons_per_layer.append(kwargs["pattern"][a])
            self.neurons_per_layer.append(self.neurons_per_layer[-1])
            self.layers += 1

        if "net" in kwargs:
            self.net = []
            self.neurons_per_layer = []
            for layer in kwargs["net"]:
                self.net.append(np.array(layer))
                self.neurons_per_layer.append(len(layer[0]))
            self.layers = len(self.net)
            self.input_am = len(self.net[0])

        if self.layers == 1 and "bias" not in kwargs:
            self.bias.append(np.ones(self.decisions_am))

        elif "bias" not in kwargs:
            self.bias.append(np.ones(self.neurons_per_layer[0]))
            for a in range(self.layers - 2):
                self.bias.append(np.ones(self.neurons_per_layer[a + 1]))
            self.bias.append(np.ones(self.decisions_am))

        if self.layers == 1 and "net" not in kwargs:
            self.net.append(np.ones((self.input_am, self.decisions_am)))

        elif "net" not in kwargs:
            self.net.append(np.ones((self.input_am, self.neurons_per_layer[0])))
            for a in range(self.layers - 2):
                self.net.append(np.ones((self.neurons_per_layer[a], self.neurons_per_layer[a + 1])))
            self.net.append(np.ones((self.neurons_per_layer[-1], self.decisions_am)))

    def decide(self, inp, **kwargs):
        if type(inp) is not np.array:
            inp = np.array(inp)
        for a in range(self.layers):
            layer = self.net[a]
            bias_ = self.bias[a]
            if "debug" in kwargs:
                if kwargs["debug"]:
                    print(inp.shape, layer.shape)
            inp = np.matmul(sigmoid(inp), layer)
            if "debug" in kwargs:
                if kwargs["debug"]:
                    print(inp.shape, bias_.shape)
            if "bias" in kwargs:
                if not kwargs["bias"]:
                    inp = inp - 1
            else:
                inp = inp - bias_
        if "debug" in kwargs:
            if kwargs["debug"]:
                return inp, list(inp).index(max(inp)), self.decisions[list(inp).index(max(inp))]
        return self.decisions[list(inp).index(max(inp))]

    def vari_net(self):
        if randint(0, 5) != 0:
            self.vari_weights()
        else:
            self.vari_bias()

    def vari_bias(self):
        layer = randint(0, self.layers - 1)
        neuron = randint(0, len(self.bias[layer]) - 1)
        new_bias = get_random(self.acc)
        self.bias[layer][neuron] = new_bias

    def vari_weights(self):
        layer = randint(0, self.layers - 1)
        neuron = randint(0, len(self.net[layer]) - 1)
        weight = randint(0, len(self.net[layer][neuron]) - 1)
        new_weight = get_random(self.acc)
        self.net[layer][neuron][weight] = new_weight

    def export(self, *args):
        exp_net = []
        exp_bias = []
        for layer in range(self.layers):
            exp_net.append(self.net[layer].tolist())
            exp_bias.append(self.bias[layer].tolist())
        if True in args:
            return exp_net, exp_bias
        return exp_net


class Net:
    def __init__(self, layer_amount: int, inp_am: int, outp_val):
        self.net = Net2(layers=layer_amount, inp_am=inp_am, dec=outp_val)

    def vari_layers(self):
        self.net.vari_weights()

    def export(self):
        return self.net.export()

    def decide(self, inp):
        return self.net.decide(inp, bias=False)


class GenNet:
    def __init__(self, decisions, net):
        self.net = Net2(net=net, dec=decisions)

    def vari_layers(self):
        self.net.vari_weights()

    def export(self):
        return self.net.export()

    def decide(self, inp):
        return self.net.decide(inp, bias=False)


class Trainer:
    def __init__(self, data, **kwargs):
        self.trainingdata,  self.trainingsol = data
        if "net" in kwargs and "bias" in kwargs and "dec" in kwargs:
            self.net = Net2(dec=kwargs["dec"], net=kwargs["net"], bias=kwargs["bias"])
        else:
            self.net = Net2(layers=1, dec=["l", "r", "u", "d", "f"], inp_am=2)
            for a in range(100):
                self.net.vari_net()
        self.score = -1
        self.step = 0.01

    def train(self, *args, **kwargs):
        last = 0
        while True:
            self.score = self.get_score()
            for a in range(self.net.layers):
                for b in range(len(self.net.net[a])):
                    for c in range(len(self.net.net[a][b])):
                        old = self.net.net[a][b][c]
                        self.net.net[a][b][c] = 1
                        while self.net.net[a][b][c] > -1:
                            new_score = self.get_score()
                            if self.score < new_score:
                                self.score = new_score
                                break
                            elif self.net.net[a][b][c] - self.step > -1:
                                self.net.net[a][b][c] = round(self.net.net[a][b][c] - self.step, 2)
                            else:
                                self.net.net[a][b][c] = old
                                break
            for a in range(self.net.layers):
                for b in range(len(self.net.bias[a])):
                    old = self.net.bias[a][b]
                    self.net.bias[a][b] = 1
                    while self.net.bias[a][b] > -1:
                        new_score = self.get_score()
                        if self.score < new_score:
                            self.score = new_score
                            break
                        elif self.net.bias[a][b] - self.step > -1:
                            self.net.bias[a][b] = round(self.net.bias[a][b] - self.step, 2)
                        else:
                            self.net.bias[a][b] = old
                            break
            if True in args:
                print(self.score, last)
            if self.score == last:
                break
            else:
                last = self.score

        if "score" in kwargs:
            if kwargs["score"]:
                return self.net.export(True), self.score
        return self.net.export(True)

    def hybrid_train(self, *args):
        last = 0
        best = self.net.export(True)
        while self.score < len(self.trainingdata):
            self.score = 0
            for a in range(self.net.layers):
                for b in range(len(self.net.net[a])):
                    for c in range(len(self.net.net[a][b])):
                        old = self.net.net[a][b][c]
                        self.net.net[a][b][c] = 1
                        while self.net.net[a][b][c] > -1:
                            new_score = self.get_score()
                            if self.score < new_score:
                                self.score = new_score
                                break
                            elif self.net.net[a][b][c] - self.step > -1:
                                self.net.net[a][b][c] -= self.step
                            else:
                                self.net.net[a][b][c] = old
                                break
            for a in range(self.net.layers):
                for b in range(len(self.net.bias[a])):
                    old = self.net.bias[a][b]
                    self.net.bias[a][b] = 1
                    while self.net.bias[a][b] > -1:
                        new_score = self.get_score()
                        if self.score < new_score:
                            self.score = new_score
                            break
                        elif self.net.bias[a][b] - self.step > -1:
                            self.net.bias[a][b] -= self.step
                        else:
                            self.net.bias[a][b] = old
                            break
            if True in args:
                print(self.score)
            if last < self.score:
                best = deepcopy(self.net.export(True))
            if last == self.score:
                last = 0
                self.net = Net2(dec=["l", "r", "u", "d", "f"], net=best[0], bias=best[1])
                for a in range(self.net.layers * 3):
                    self.net.vari_net()
                if True in args:
                    print("reset")

            else:
                last = self.score
        return self.net.export(True)

    def get_score(self):
        score_ = 0
        for a in range(len(self.trainingdata)):
            if self.net.decide(self.trainingdata[a]) == self.trainingsol[a]:
                score_ += 1
        return score_