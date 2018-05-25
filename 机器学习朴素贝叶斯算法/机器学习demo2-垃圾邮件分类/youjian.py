#coding=utf-8
from numpy import *

#解析文档的函数
def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]
    
    
#创建一个带有所有单词的列表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)
    
def setOfWords2Vec(vocabList, inputSet):
    retVocabList = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            retVocabList[vocabList.index(word)] = 1
        else:
            print 'word ',word ,'not in dict'
    return retVocabList

#另一种模型    
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def trainNB0(trainMatrix,trainCatergory):
    numTrainDoc = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCatergory)/float(numTrainDoc)
    #防止多个概率的成绩当中的一个为0
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDoc):
        if trainCatergory[i] == 1:
            p1Num +=trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num +=trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)#处于精度的考虑，否则很可能到限归零
    p0Vect = log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive
    
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else: 
        return 0
        
def spamTest(spamFloder, hamFloder):
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse(open(spamFloder+str(i)+'.txt').read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open(hamFloder+str(i)+'.txt').read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trianClasses = []
    print trainingSet
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        #trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trianClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trianClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        #wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            print "classification error",docList[docIndex]
    print 'the error rate is: ',float(errorCount)/len(testSet)
    #return vocabList,fullText
    
    
def main():
    spamTest('email/spam/','email/ham/')
    
if __name__ == '__main__':
    main()