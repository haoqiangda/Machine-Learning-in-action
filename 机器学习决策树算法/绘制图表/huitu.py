import matplotlib.pyplot as plt  # 载入 pyplot API
decisionNode = dict(boxstyle="sawtooth", fc="0.8") # 注（a）
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")  # 箭头样式

def plotNode(nodeTxt, centerPt, parentPt, nodeType):  #  centerPt节点中心坐标  parentPt 起点坐标
	creatPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction', va="center", ha="center", bbox=nodeType, arrowprops=arrow_args) # 注（b）

def creatPlot():
	fig = plt.figure(1, facecolor='white') # 创建一个新图形
	fig.clf() 
	creatPlot.ax1 = plt.subplot(111,frameon=False)  # subplot(323)和subplot(3,2,3)是相同的
	plotNode('decision Node', (0.5,0.1), (0.1,0.5), decisionNode)
	plotNode('leaf Node', (0.8,0.1), (0.3,0.8), leafNode)
	plt.show()
if __name__ == '__main__':
	creatPlot()