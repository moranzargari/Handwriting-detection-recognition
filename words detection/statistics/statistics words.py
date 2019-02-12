import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

####################################################################
def calc_algo_rate(algo, num_words):
    sum = 0
    for a, b in zip(algo, num_words):
        sum += a/b
    return sum/len(num_words)

####################################################################

def extract(data):

    vectors = dict()
    for i in data.columns:
        temp = list()
        for j in range(data.shape[0]):
            if math.isnan(float(data[str(i)][j])) == False:
                temp.append(data[str(i)][j])
        vectors[str(i)] = temp
    return vectors

####################################################################

data = pd.read_csv("statistics words.csv")
print (data)
dict_data = extract(data)
print (dict_data)
sum_pixels_rate = calc_algo_rate(dict_data['sumpixels'],dict_data['num of words'])
contours_rate = calc_algo_rate(dict_data['contours'],dict_data['num of words'])

print(sum_pixels_rate)
print(contours_rate)
print("-------------")
print (sum(dict_data['sumpixels'])/sum(dict_data['num of words']))
print (sum(dict_data['contours'])/sum(dict_data['num of words']))

font = {'color': 'darkred', 'size': '12', 'family': 'serif'}

############################################################################# algo score 1
algorithms = ['Sum Pixels words', 'Dynamic Dilation']
y_pos = np.arange(len(algorithms))
avgs = [sum_pixels_rate, contours_rate]

plt.bar(y_pos, avgs, align='center', alpha=0.5, color=['green', 'blue'])
plt.xticks(y_pos, algorithms)
plt.ylabel('Algorithm Score', fontdict=font)
plt.xlabel('Algorithm', fontdict=font)
plt.title('Statistics')
plt.show()

############################################################################# algo score 2
algorithms = ['Sum Pixels words', 'Dynamic Dilation']
y_pos = np.arange(len(algorithms))
avgs = [sum(dict_data['sumpixels'])/sum(dict_data['num of words']),sum(dict_data['contours'])/sum(dict_data['num of words'])]

plt.bar(y_pos, avgs, align='center', alpha=0.5, color=['green', 'blue'])
plt.xticks(y_pos, algorithms)
plt.ylabel('Algorithm Score', fontdict=font)
plt.xlabel('Algorithm', fontdict=font)
plt.title('Statistics')
plt.show()
