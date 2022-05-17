#! /usr/bin/env python3


# SETUP
from __future__ import division, print_function
import numpy as np
import pandas as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz


# x = []
# y = []
theta_err = []
d_o = []
d_g = []

vx = []
vy = []
wz = []

alldata = np.vstack((theta_err, d_o, d_g, vx, vy, wz))
