import sys
reload(sys)
sys.setdefaultencoding('utf8')
import matplotlib
from numpy import *
import operator
import matplotlib.pyplot as plt
def file2matrix(filename):
        fr =open(filename)
        arrayOLines = fr.readlines()
        numberOfLines   = len(arrayOLines)
        returnMat = zeros((numberOfLines,3))
        classLabelVector = []
        index =0
        for line in arrayOLines:
                line = line.strip()
                listFromLine = line.split('\t')
                returnMat[index,:]=listFromLine[0:3]
                classLabelVector.append(int(listFromLine[-1]))
                index+=1
        return  returnMat,classLabelVector
def autoNorm(dataSet):
        minVals = dataSet.min(0)
        maxVals = dataSet.max(0)
        ranges = maxVals - minVals
        normDataSet = zeros(shape(dataSet))
        m = dataSet.shape[0]
        normDataSet = dataSet -tile(minVals,(m,1))
        normDataSet = normDataSet/tile(ranges,(m,1))
        return normDataSet,ranges,minVals
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
def datingClassTest():
        hoRatio =0.10
        datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
        normMat,ranges,minVals = autoNorm(datingDataMat)
        m = normMat.shape[0]
        numTestVecs = int(m*hoRatio)
        errorCount = 0.0
        for i in range(numTestVecs):
               classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
               print ("the classifier came back with:  %d , the real answer is :  %d"% (classifierResult, datingLabels[i]))
               if (classifierResult !=datingLabels[i]):errorCount+=1.0
        print ("the total error rate is :%f" %(errorCount/float(numTestVecs)))
def  classifyPerson():
         resultList  = ['not at all','in small does','in large does']
         percentTats = float(input("percentage of time spent playing video games?"))
         ffMiles = float(input("frequent flier miles earned per year?"))
         iceCream = float(input("liters of ice cream consumed per year?"))
         datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
         normMat,ranges,minVals = autoNorm(datingDataMat)
         inArr = array([ffMiles,percentTats,iceCream])
         classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
         print ("You will probably like this person :",)
         print (resultList[classifierResult-1])
if __name__=="__main__":
         datingDataMat,datingLabels= file2matrix('datingTestSet2.txt')
         fig = plt.figure()
         ax =fig.add_subplot(121)
         ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
         ax =fig.add_subplot(122)
         ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
         #datingClassTest()
         classifyPerson()
         plt.show()
         print  (datingDataMat)
         print  (datingLabels)