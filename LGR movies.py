import numpy as np
from operator import itemgetter
import csv,os
class kNNClassifier(object):
    def __init__(self): #like constructor
        self.training_features=None
        self.training_labels=None #gloabl variable
        self.test_features=None
        self.elegantResult="Most lokely,{0},'{1}' is of type of '{2}'." #build meaningful result
    def createSampleTrainingData(self):
        self.tarining_features=np.array([[1.0,1.1],[1.0,1.0],[0.0,0.1],[0.0,0.0]])
        self.training_labels=['A','A','B','B']
        self.test_features=np.array([1,1,1],dtype=float)
    def loadTrainingDataFromFile(self,file_path):
        if file_path is not None and os.path.exists(file_path):
            features=[]
            self.training_labels=[]
            with open(file_path,'r') as training_data_file:
                reader=csv.DictReader(training_data_file) #reads all the data of file
                for row in reader: #runs 7 times here
                    if row['moviename']!='?':
                        features.append([float(row['kicks']),float(row['kisses'])])
                        self.training_labels.append(row['movietype'])
                    else:
                        self.test_features=np.array([float(row['kicks']),float(row['kisses'])])
            if len(features)>0:
                self.training_features=np.array(features)
            print "self.training_features: \n",self.training_features
            print "self.training_labels: ",self.training_labels
            print "self.test_features:",self.test_features
    def classifyTestData(self,test_data=None,k=0): #k=3 or 5 or 7
        print "classifyTestData: test_data",test_data
        if test_data is not None:
            self.test_features=np.array(test_data,dtype=float)
        print "classifyTestData: self.test_features:",self.test_features
        if self.test_features is not None and self.training_features is not None and self.training_labels is not None and k>0:
            print "ClassifyTestData says self.test.features: ",self.test_features
            print "self.training_labels: ",self.training_labels
            featureVectorSize=self.training_features.shape[0]
            print "featuresVectorSize:",featureVectorSize
            tileOfTestData=np.tile(self.test_features,(featureVectorSize,1)) #tile== repeat the value
            print "after tile,temp:\n",tileOfTestData
            diffMat=self.training_features-tileOfTestData
            print "difMat:\n",diffMat
            sqDiffMat = diffMat ** 2
            print "sqDiffMat\n",sqDiffMat
            sqDistances=sqDiffMat.sum(axis=1)
            print "(Row wise sum)sqDistances:",sqDistances
            distances=sqDistances ** 0.5
            print "distances(square root of sqDistances):",distances
            sortedDistanceIndices=distances.argsort()
            print "SortDistancesIndices:",sortedDistanceIndices
            print "self.training_labels:",self.training_labels
            classCount={}
            for i in range(k): #k=3
                print "sortedDistanceIndices[",i,"]: ",sortedDistanceIndices[i]
                voteILabel=self.training_labels[sortedDistanceIndices[i]]
                print "voteIlabel:",voteILabel
                classCount[voteILabel]=classCount.get(voteILabel,0)+1
                #classCount={"Romance":2,"Action":1}
            print "classCount=",classCount
            sortedClassCount=sorted(classCount.iteritems(),key=itemgetter(1),reverse=True)
            # sortedclassCount={"Romance":2,"Action":1}
            print "sortedClassCount=",sortedClassCount
            print "sortedClassCount[0]:",sortedClassCount[0]
            print "sortedClassCount[0][0]:",sortedClassCount[0][0]
            return sortedClassCount[0][0]
        else:
            return  "can't determine result for empty test-data."
def predictSampleDataClass():
    test_data=o[0.1,0.2]
    instance=kNNClassifier()
    instance.createSampleTrainingData()
    classOfTestData=instance.classifyTestData(test_data=test_data,k=3)
    return instance.elegantResult.format('record',str(instance.test_features),classOfTestData)
def predictMovieType():
    instance=kNNClassifier()
    instance.loadTrainingDataFromFile('LgR_Movies_kNN_classifier.csv')
    classOfTestData=instance.classifyTestData(test_data=None,k=3)
    print "predictMovieType classOfTestData=",classOfTestData
    return instance.elegantResult.format('movie',str(instance.test_features),classOfTestData)
if __name__=='__main__':
    print predictMovieType()