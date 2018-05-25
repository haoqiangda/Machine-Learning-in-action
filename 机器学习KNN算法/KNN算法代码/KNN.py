from numpy import *
import operator
from os import listdir
import matplotlib.pyplot as plt
def createDataSet():
	group = array([[1.0,1.1],
		          [1.0,1.0],
		          [0,0],
		          [0,0.1]])
	labels =['A','A','B','B']
	return group,labels
def  classify0(inX,dataSet,labels,k):
	dataSetSize = dataSet.shape[0];
	diffMat = tile(inX,(dataSetSize,1)) - dataSet
	sqDiffMat = diffMat**2
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	sortedDistIndicies = distances.argsort();
	classCount = { }
	for i  in range(k):
	        voteIlabel = labels[sortedDistIndicies[i]]
	        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
	        sortedClassCount =sorted(classCount.items(),key=operator.itemgetter(1),reverse =True)
	return sortedClassCount[0][0]
def firstTest():
        test1 = [1.0, 1.2]
        test2 = [0.0, 0.4]
        dataset, labels = createDataSet()
        conclusion1 = classify0(test1, dataset, labels, 3)
        conclusion2 = classify0(test2, dataset, labels, 3)
        print(str(test1) + "分类后的结果是属于" + conclusion1 + "类")
        print(str(test2) + "分类后的结果是属于" + conclusion2 + "类")

if __name__ == "__main__":
         firstTest()
      

