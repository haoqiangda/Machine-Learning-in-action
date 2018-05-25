# -*- coding:utf-8 -*-
from numpy import *
import feedparser
#RSS源分类器及高频词去除函数
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict={}
    for token in vocabList:  #遍历词汇表中的每个词
        freqDict[token]=fullText.count(token)  #统计每个词在文本中出现的次数
    sortedFreq=sorted(freqDict.iteritems(),key=operator.itemgetter(1),reverse=True)  #根据每个词出现的次数从高到底对字典进行排序
    return sortedFreq[:30]   #返回出现次数最高的30个单词
#创建一个包含在所有文档中出现的不重复词的列表
def createVocabList(dataSet):
    vocabSet=set([])    #创建一个空集
    for document in dataSet:
        vocabSet=vocabSet|set(document)   #创建两个集合的并集
    return list(vocabSet)
def setOfWords2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)  #创建一个其中所含元素都为0的向量
    for word in inputSet:
        if word in vocabList:
                returnVec[vocabList.index(word)]+=1
    return returnVec
#另一种模型    
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec
#朴素贝叶斯分类器训练函数
def trainNBO(trainMatrix,trainCategory):
    numTrainDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numTrainDocs)
    p0Num=ones(numWords);p1Num=ones(numWords)   #计算p(w0|1)p(w1|1),避免其中一个概率值为0，最后的乘积为0
    p0Demo=2.0;p1Demo=2.0  #初始化概率
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
               p1Num+=trainMatrix[i]
               p1Demo+=sum(trainMatrix[i])
        else:
               p0Num+=trainMatrix[i]
               p0Demo+=sum(trainMatrix[i])
    #p1Vect=p1Num/p1Demo
    #p0Vect=p0Num/p0Demo
    p1Vect=log(p1Num/p1Demo) #计算p(w0|1)p(w1|1)时，大部分因子都非常小，程序会下溢出或得不到正确答案（相乘许多很小数，最后四舍五入会得到0）
    p0Vect=log(p0Num/p0Demo)
    return p0Vect,p1Vect,pAbusive
#朴素贝叶斯分类函数
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0
#解析文档的函数
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]
def localWords(feed1,feed0):
    import feedparser
    docList=[];classList=[];fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'][i]['summary'])   #每次访问一条RSS源
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList=textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList=createVocabList(docList)
    top30Words=calcMostFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList:vocabList.remove(pairW[0])    #去掉出现次数最高的那些词
    trainingSet=range(2*minLen);testSet=[]
    for i in range(20):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNBO(array(trainMat),array(trainClasses))
    errorCount=0
    for docIndex in testSet:
        wordVector=bagOfWords2VecMN(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount+=1
    print 'the error rate is:',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V
def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]
if __name__ == '__main__':
    ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    #localWords(ny,sf)
    getTopWords(ny,sf)