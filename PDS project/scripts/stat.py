#
# Calculate Confusion Matrix and Other Statistics
# PDS 2021 - Identification of Mobile Traffic using TLS Fingerprinting
# Bc. Marian Kapisinsky, xkapis00
# 25.4.2021
#

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def usage():
	print('Usage: stat.py predicted.csv real.txt')

if len(sys.argv) != 3:
	usage()
	sys.exit(2)

predicted=[]
with open(sys.argv[1], newline='') as csvfile:
	predreader = csv.DictReader(csvfile, delimiter=';')
	for row in predreader:
		predicted.append(row['APP'])
		
real=[]
with open(sys.argv[2], 'r') as realv:
	real = [i.strip('\n') for i in realv]
real.pop(0)

predicted = [val.replace("unknown", 'x') for val in predicted]

real = [val.replace("unknown", 'x') for val in real]

confusion = confusion_matrix(predicted, real)

print(confusion)

TP = 0
FP = 0
TN = 0
FN = 0

for i in range(len(predicted)):
	if real[i]==predicted[i]!="x":
		TP += 1
	elif real[i]=="x" and predicted[i]!=real[i]:
		FP += 1
	elif real[i]==predicted[i]=="x":
		TN += 1
	else:
		FN += 1

# Recall
recall = TP/(TP+FN)

# Precision
precision = TP/(TP+FP)

# Overall accuracy
accuracy = (TP+TN)/(TP+FP+FN+TN)

print("\nStatistics:\n")
print("All:\t\t\t"+str(TP+FP+FN+TN))
print("True Positive:\t\t"+str(TP))
print("False Positive:\t\t"+str(FP))
print("True Negative:\t\t"+str(TN))
print("False Negative:\t\t"+str(FN)+"\n")
print("Accuracy:\t\t"+str(accuracy))
print("Precision:\t\t"+str(precision))
print("Recall:\t\t\t"+str(recall))


