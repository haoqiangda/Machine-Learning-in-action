# -*- coding: utf-8 -*-
import sys 
reload(sys)
sys.setdefaultencoding('utf8')
from matplotlib.font_manager import FontProperties
from numpy import*
import matplotlib.pyplot as plt
import random
from os import listdir
import operator
'''  
基于SVM的数字识别：  
  
(1)收集数据:提供的文本文件。  
(2)准备数据:基于二值图像构造向量。  
(3)分析数据:对图像向量进行目测。  
(4)训练算法:采用两种不同的核函数，并对径向基核函数采用不同的设置来运行SMO算法。  
(5)测试算法:编写一个函数来测试不同的核函数并计算错误率。  
(6)使用算法:一个图像识别的完整应用还需要一些图像处理的知识，这里并不打算深入介绍。  
  
  
基于SVM的手写数字识别  
'''  
def loadImages(dirName):  
    from os import listdir  
    hwLabels = []  
    trainingFileList = listdir(dirName)           #load the training set  
    m = len(trainingFileList)  
    trainingMat = zeros((m,1024))  
    for i in range(m):  
        fileNameStr = trainingFileList[i]  
        fileStr = fileNameStr.split('.')[0]     #take off .txt  
        classNumStr = int(fileStr.split('_')[0])  
        if classNumStr == 9: hwLabels.append(-1)  
        else: hwLabels.append(1)  
        trainingMat[i,:] = img2vector('%s/%s' % (dirName, fileNameStr))  
    return trainingMat, hwLabels      
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect
def loadDataSet(filename):
    dataMat = []; labelMat = []
    fr =open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat
class optStruct:
    def __init__(self,dataMatIn, classLabels, C, toler, kTup):  # Initialize the structure with the parameters 
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        self.eCache = mat(zeros((self.m,2))) #first column is valid flag#误差缓存
        self.K = mat(zeros((self.m,self.m)))
        for i in range(self.m):
            self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup)

def calcEk(oS, k):
    fXk = float(multiply(oS.alphas,oS.labelMat).T*oS.K[:,k] + oS.b)
    Ek = fXk - float(oS.labelMat[k])
    return Ek
def selectJrand(i,m):
    j=i #we want to select any J not equal to i
    while (j==i):
        j = int(random.uniform(0,m))  # 一直在挑选随机数j，直到不等于i，随机数的范围在0~m
    return j  # 返回挑选好的随机数
def clipAlpha(aj,H,L):  # 最大不能超过H，最小不能低于L
    if aj > H: 
        aj = H
    if L > aj:
        aj = L
    return aj

def selectJ(i, oS, Ei):         #this is the second choice -heurstic, and calcs Ej
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCache[i] = [1,Ei]  #set valid #choose the alpha that gives the maximum delta E
    validEcacheList = nonzero(oS.eCache[:,0].A)[0]
    if (len(validEcacheList)) > 1:
        for k in validEcacheList:   #loop through valid Ecache values and find the one that maximizes delta E
            if k == i: continue #don't calc for i, waste of time
            Ek = calcEk(oS, k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = Ek #选择具有最大步长的j
        return maxK, Ej
    else:   #in this case (first time around) we don't have any valid eCache values
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
    return j, Ej

def updateEk(oS, k):#after any alpha has changed update the new value in the cache
    Ek = calcEk(oS, k)
    oS.eCache[k] = [1,Ek]
def innerL(i, oS):
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j,Ej = selectJ(i, oS, Ei) #this has been changed from selectJrand
        alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy();
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L==H: print "L==H"; return 0
        eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j] #changed for kernel
        if eta >= 0: print "eta>=0"; return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei - Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
        updateEk(oS, j) #added this for the Ecache
        if (abs(oS.alphas[j] - alphaJold) < 0.00001): print "j not moving enough"; return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*(alphaJold - oS.alphas[j])#update i by the same amount as j
        updateEk(oS, i) #added this for the Ecache                    #the update is in the oppostie direction
        b1 = oS.b - Ei- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i,i] - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[i,j]
        b2 = oS.b - Ej- oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i,j]- oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[j,j]
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1 + b2)/2.0
        return 1
    else: return 0
def smoP(dataMatIn, classLabels, C, toler, maxIter,kTup=('lin', 0)):    #full Platt SMO
    oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler, kTup)
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet:   #go over all
            for i in range(oS.m):        
                alphaPairsChanged += innerL(i,oS)
                print "fullSet, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
            iter += 1
        else:#go over non-bound (railed) alphas
            nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i,oS)
                print "non-bound, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
            iter += 1
        if entireSet: entireSet = False #toggle entire set loop
        elif (alphaPairsChanged == 0): entireSet = True  
        print "iteration number: %d" % iter
    return oS.b,oS.alphas
def calcWs(alphas,dataArr,classLabels):        #该函数是通过alpha转换为w
    X = mat(dataArr); labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w
def kernelTrans(X, A, kTup): #calc the kernel or transform data to a higher dimensional space#核转换函数
    m,n = shape(X)
    K = mat(zeros((m,1)))
    if kTup[0]=='lin': K = X * A.T   #linear kernel
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow = X[j,:] - A
            K[j] = deltaRow*deltaRow.T
        K = exp(K/(-1*kTup[1]**2)) #divide in NumPy is element-wise not matrix like Matlab
    else: raise NameError('Houston We Have a Problem -- \
    That Kernel is not recognized')
    return K
    #利用核函数进行分类的径向基测试函数  
def testDigits(kTup=('rbf', 10)):  
    dataArr,labelArr = loadImages('trainingDigits')  
    b,alphas = smoP(dataArr, labelArr, 200, 0.0001, 10000, kTup)  
    datMat=mat(dataArr); labelMat = mat(labelArr).transpose()  
    svInd=nonzero(alphas.A>0)[0]  
    print svInd
    sVs=datMat[svInd]   
    print sVs
    labelSV = labelMat[svInd];  
    print labelSV
    print "there are %d Support Vectors" % shape(sVs)[0]
    m,n = shape(datMat)  
    errorCount = 0  
    for i in range(m):  
        kernelEval = kernelTrans(sVs,datMat[i,:],kTup)  
        predict=kernelEval.T * multiply(labelSV,alphas[svInd]) + b  
        if sign(predict)!=sign(labelArr[i]): errorCount += 1  
    print "the training error rate is: %f" % (float(errorCount)/m)
    dataArr,labelArr = loadImages('testDigits')  
    errorCount = 0  
    datMat=mat(dataArr); labelMat = mat(labelArr).transpose()  
    m,n = shape(datMat)  
    for i in range(m):  
        kernelEval = kernelTrans(sVs,datMat[i,:],kTup)  
        predict=kernelEval.T * multiply(labelSV,alphas[svInd]) + b  
        if sign(predict)!=sign(labelArr[i]): errorCount += 1      
    print "the test error rate is: %f" % (float(errorCount)/m)   
if __name__ == '__main__':
    print 'a'
    testDigits(('rbf', 800))
    print 'a'