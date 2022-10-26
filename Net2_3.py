import numpy as np
import math as m
from random import randint


def sigmoid(inp):
    return 1 / (1 + m.e ** (-inp))


class Net:
    def __init__(self, **kwargs):
        self.layers = 1
        self.output = [1, 0]
        self.pattern = [2]
        self.net = []
        self.input_am = 2
        self.output_am = 2
        self.got_net = False

        if "layers" in kwargs:
            self.layers = kwargs["layers"]
            self.pattern = [self.output_am for a in range(self.layers)]

        if "input_am" in kwargs:
            self.input_am = kwargs["input_am"]

        if "dec" in kwargs:
            self.output = kwargs["dec"]
            self.output_am = len(self.output)
            self.pattern = [self.output_am for a in range(self.layers)]

        if "pattern" in kwargs:
            if len(kwargs["pattern"]) != 0:
                self.pattern = kwargs["pattern"]
                if self.pattern[-1] != self.output_am:
                    self.pattern.append(self.output_am)
                self.layers = len(self.pattern)

        if "net" in kwargs:
            self.net = kwargs["net"]
            self.layers = len(self.net)
            self.got_net = True

        elif self.layers > 1:
            self.net.append([np.ones((self.input_am, self.pattern[0])), np.ones(self.pattern[0])])
            for a in range(self.layers - 1):
                self.net.append([np.ones((self.pattern[a], self.pattern[a + 1])),
                                 np.ones(self.pattern[a + 1])])

        elif self.layers == 1:
            self.net.append([np.ones((self.input_am, self.output_am)), np.ones(self.output_am)])

        # print(self.net)
        # print(self.layers)
        # print(self.pattern)

    def decide(self, inp, *args):
        inp = np.array(inp)
        for layer in self.net:
            if True in args:
                print(inp, layer[0])
                print(inp.shape,  layer[0].shape)
            inp = np.matmul(sigmoid(inp), layer[0])
            inp = inp - layer[1]
        inp_ = list(inp)
        if True in args:
            print(inp)
        decision = self.output[inp_.index(max(inp))]
        return decision

    def export(self):
        outp = []
        if self.got_net:
            return self.net
        for layer in self.net:
            outp.append([layer[0].tolist(), layer[1].tolist()])
        return outp

    def vari_net(self):
        new_val = randint(-100, 100) / 100
        layer = randint(0, self.layers - 1)
        b_w = randint(0, 1)
        if b_w == 0:
            weight = randint(0, len(self.net[layer][b_w]) - 1)
            neuron = randint(0, len(self.net[layer][b_w][weight]) - 1)
            self.net[layer][b_w][weight][neuron] = new_val

        else:
            neuron = randint(0, len(self.net[layer][b_w]) - 1)
            self.net[layer][b_w][neuron] = new_val
