import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


################################################################################################
def extract(data):

    vectors = dict()
    for i in range(1, data.shape[1]+1):
        temp = list()
        for j in range(data.shape[0]):
            if math.isnan(float(data[str(i)][j])) == False:
                temp.append(data[str(i)][j])
        vectors[str(i)] = temp
    return vectors

################################################################################################
def line_Score(original_upper, original_lower, algo_upper, algo_lower):
        if algo_lower == algo_upper:
            return 0
        max_upper = np.maximum(original_upper, algo_upper)
        min_lower = np.minimum(original_lower, algo_lower)
        min_upper = np.minimum(original_upper, algo_upper)
        max_lower = np.maximum(original_lower, algo_lower)

        LineScore = (max_upper - min_lower) / (min_upper - max_lower)
        return LineScore

################################################################################################
def Documents_Score(original_vectors,algo_vectors):
    documents = dict()
    sum = 0
    for i in range(1, 41):
        sum = 0
        for j in range(0, len(original_vectors[str(i)]), 2):
            original = original_vectors[str(i)]
            algo = algo_vectors[str(i)]
            sum += line_Score(original[j], original[j+1], algo[j], algo[j+1])
        documents[str(i)] = abs((sum / (len(original_vectors[str(i)]) / 2))*100)
    return documents

################################################################################################
def Algorithem_Score(docs):

    sum = 0
    for i in range(1, 41):
        sum += docs[str(i)]
    return sum / 40


################################################################################################

## main


original = pd.read_csv("real.csv")
mser = pd.read_csv("mser.csv")
sumPixels = pd.read_csv("sumPixels.csv")
contuors = pd.read_csv("contuors.csv")
reduce = pd.read_csv("reduce.csv")

original_vectors = extract(original)
mser_vectors = extract(mser)
sumPixels_vectors = extract(sumPixels)
contuors_vectors = extract(contuors)
reduce_vectors = extract(reduce)

font = {'color': 'darkred', 'size': '12', 'family': 'serif'}


#################################################################### graph for MSER Algorithm
docs = Documents_Score(original_vectors, mser_vectors)
avg_mser = Algorithem_Score(docs)
g = [docs[str(i)] for i in docs]
plt.bar(np.arange(len(docs)),g, align='center', alpha=0.5, color=['red'])
plt.xticks(np.arange(len(docs)), range(1, 41))
plt.title('MSER')
plt.ylabel('Document Score', fontdict=font)
plt.xlabel('Document number', fontdict=font)
plt.show()

#################################################################### graph for Sum Pixels Algorithm
docs = Documents_Score(original_vectors, sumPixels_vectors)
avg_sumPixels = Algorithem_Score(docs)
g = [docs[str(i)] for i in docs]
plt.bar(np.arange(len(docs)),g, align='center', alpha=0.5, color=['green'])
plt.xticks(np.arange(len(docs)), range(1, 41))
plt.title('Sum Pixels (ours algorithm)')
plt.ylabel('Document Score', fontdict=font)
plt.xlabel('Document number', fontdict=font)
plt.show()

#################################################################### graph for Contours Algorithm
docs = Documents_Score(original_vectors, contuors_vectors)
avg_contours = Algorithem_Score(docs)
g = [docs[str(i)] for i in docs]
plt.bar(np.arange(len(docs)),g, align='center', alpha=0.5, color=['blue'])
plt.xticks(np.arange(len(docs)), range(1, 41))
plt.title('Find Contours')
plt.ylabel('Document Score', fontdict=font)
plt.xlabel('Document number', fontdict=font)
plt.show()

#################################################################### graph for Reduce Algorithm
docs = Documents_Score(original_vectors, reduce_vectors)
avg_reduce = Algorithem_Score(docs)
g = [docs[str(i)] for i in docs]
plt.bar(np.arange(len(docs)),g, align='center', alpha=0.5, color=['cyan'])
plt.xticks(np.arange(len(docs)), range(1, 41))
plt.title('Reduce')
plt.ylabel('Document Score', fontdict=font)
plt.xlabel('Document number', fontdict=font)
plt.show()

##################################################################### Graph for all algorithms scores

algorithms = ['MSER', 'Sum Pixels (ours algorithm)', 'Find Contours', 'Reduce']
y_pos = np.arange(len(algorithms))
avgs = [avg_mser, avg_sumPixels, avg_contours, avg_reduce]

plt.bar(y_pos, avgs, align='center', alpha=0.5, color=['red', 'green', 'blue', 'cyan'])
plt.xticks(y_pos, algorithms)
plt.ylabel('Algorithm Score', fontdict=font)
plt.xlabel('Algorithm', fontdict=font)
plt.title('Statistics')
plt.show()
