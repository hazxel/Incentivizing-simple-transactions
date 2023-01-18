import matplotlib.pyplot as plt
import numpy as np

CONFIDENCE_80 = 1.28
CONFIDENCE_90 = 1.64
CONFIDENCE_95 = 1.96
CONFIDENCE_99 = 2.58


def plot(original_throughput, simplified_throughput):
    rounds = len(original_throughput)
    samples = len(original_throughput[0])

    original_mean = []
    original_ceil = []
    original_floor = []
    simplified_mean = []
    simplified_ceil = []
    simplified_floor = []

    for samples in original_throughput:
        mean = np.mean(samples)
        std = np.std(samples)
        original_mean.append(mean)
        original_ceil.append(mean + CONFIDENCE_80 * std)
        original_floor.append(mean - CONFIDENCE_80 * std)
    for samples in simplified_throughput:
        mean = np.mean(samples)
        std = np.std(samples)
        simplified_mean.append(mean)
        simplified_ceil.append(mean + CONFIDENCE_80 * std)
        simplified_floor.append(mean - CONFIDENCE_80 * std)
    
    fig, ax = plt.subplots()

    x = range(rounds)
    original_line, = ax.plot(x, original_mean, 's-', markersize = 5, linestyle='dotted', color='indianred', label="ATT-RLSTM")
    simplified_line, = ax.plot(x, simplified_mean, 'o-', markersize = 5, linestyle='dashed', color='seagreen', label="CNN-RLSTM")

    ax.fill_between(x, original_ceil, original_floor, color='indianred', alpha = 0.3)
    ax.fill_between(x, simplified_ceil,simplified_floor, color='seagreen', alpha = 0.3)
   
    plt.xlabel('block')
    plt.ylabel('throughput')
    plt.locator_params(nbins=rounds/4)

    plt.grid(linestyle = '--')

    ax.legend(handles=[original_line,simplified_line],labels=['original','simplified'], loc='best')
    plt.show()