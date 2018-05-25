import matplotlib.pyplot as plt 
import pickle
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
##获取节点的数目和树的层数 
def getNumLeafs(myTree):
        numLeafs = 0
#firstStr = myTree.keys()[0]
        firstSides = list(myTree.keys())
        firstStr = firstSides[0]#找到输入的第一个元素
        secondDict = myTree[firstStr]
        for key in secondDict.keys():
                if type(secondDict[key]) == dict:
                        numLeafs += getNumLeafs(secondDict[key])
                else: 
                        numLeafs += 1
        return numLeafs

def getTreeDepth(myTree):
        maxDepth = 1
        firstSides = list(myTree.keys())
        firstStr = firstSides[0]#找到输入的第一个元素
#firstStr = myTree.keys()[0]
        secondDict = myTree[firstStr]
        for key in secondDict.keys():
                if type(secondDict[key]) == dict:
                        thisDepth = 1 + getTreeDepth(secondDict[key])
                else: 
                        thisDepth = 1
                if thisDepth > maxDepth: maxDepth = thisDepth
        return maxDepth

def retrieveTree(i):
        listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
        {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
        ]
        return listOfTrees[i]
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
        createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
                xytext=centerPt, textcoords='axes fraction',
                va="center", ha="center", bbox=nodeType, arrowprops=arrow_args )
    
def plotMidText(cntrPt, parentPt, txtString):
        xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
        yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
        createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

def plotTree(myTree, parentPt, nodeTxt):
        numLeafs = getNumLeafs(myTree)  
        depth = getTreeDepth(myTree)
        firstSides = list(myTree.keys())
        firstStr = firstSides[0]#找到输入的第一个元素
        cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
        plotMidText(cntrPt, parentPt, nodeTxt)
        plotNode(firstStr, cntrPt, parentPt, decisionNode)
        secondDict = myTree[firstStr]
        plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
        for key in secondDict.keys():
                if type(secondDict[key]).__name__=='dict':   
                        plotTree(secondDict[key],cntrPt,str(key))        
                else:   
                        plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
                        plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
                        plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
        plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD
def createPlot(inTree):
        fig = plt.figure(1, facecolor='white')
        fig.clf()
        axprops = dict(xticks=[], yticks=[])
        createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    
        plotTree.totalW = float(getNumLeafs(inTree))
        plotTree.totalD = float(getTreeDepth(inTree))
        plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
        plotTree(inTree, (0.5,1.0), '')
        plt.show()
def classify(inputTree,featLabels,testVec):
        firstSides = list(inputTree.keys())
        firstStr = firstSides[0]#找到输入的第一个元素
        secondDict = inputTree[firstStr]
        featIndex  =  featLabels.index(firstStr)
        for key in secondDict.keys():
            if testVec[featIndex] == key:
                if type(secondDict[key]).__name__=='dict':
                    classLabel = classify(secondDict[key],featLabels,testVec)
                else:
                    classLabel=secondDict[key]
        return  classLabel 
# ======================
# 输入：
#        myTree:    决策树
# 输出：
#        决策树文件
# ======================
def storeTree(inputTree,filename):
    #'保存决策树'
        fw = open(filename,'wb')
        pickle.dump(inputTree,fw)
        fw.close()
    
# ========================
# 输入：
#        filename:    决策树文件名
# 输出：
#        pickle.load(fr):    决策树
# ========================    
def grabTree(filename):
    #'打开决策树'
        #import pickle
        fr = open(filename,'rb')
        return pickle.load(fr)

if __name__ == '__main__':#测试
        mytree = retrieveTree(0)
        storeTree(mytree,'classifierStorage.txt')
        m1 = grabTree('classifierStorage.txt')
        print(m1)
        labels = ['no surfacing','flippers']
        print(classify(mytree,labels,[1,0]))
        print(classify(mytree,labels,[1,1]))
        print(mytree)
        createPlot(mytree)
        print(getNumLeafs(mytree))
        print(getTreeDepth(mytree))