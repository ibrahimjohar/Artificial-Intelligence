#DECISION TREE CLASSIFIER
#most powerful and popular tool for classification and prediction.

# DECISION TREE TERMINOLOGIES
# 1. Root Node: The first split which decides the entire population or sample data should further get divided into two or more homogeneous sets
# 2. Splitting: It is a process of dividing a node into two or more sub-nodes
# 3. Decision Node: This node decides whether/when a sub-node splits into further sub-nodes or not
# 4. Leaf Node: Terminal Node that predicts the outcome (categorical or continuous value).
# 5. Branch: A subsection of the entire tree is called branch or sub-tree.
# 6. Parent Node: A node divided into sub-nodes is called a parent node of sub-nodes whereas sub-nodes are the child of a parent node.

#STEPS TO IMPLEMENT DECISION TREE

## step 1 -> begin the tree w/ root node, says S, which contains the complete dataset
## step 2 -> find best attribute in the dataset using ASM (attribute selection measure)
## step 3 -> divide the S into subsets that contain possible values for the best attribute
## step 4 -> generate the decision tree node containing the best attribute
## step 5 -> recursively make new decision trees using the subsets of the dataset created in step3

## continue this process until a stage is reached - cannot further classify the node and call the final node a leaf node

from sklearn.tree import DecisionTreeClassifier

#initialize the DecisionTreeClassifier
DT = DecisionTreeClassifier()



#train the model 
ModelDT = DT.fit(X_train, Y_train)

#model testing (prediction) 
PredictionDT = DT.predict(X_test)
print("predictions: ", PredictionDT)

#model training accuracy
print('====================DT Training Accuracy===============')
tracDT = DT.score(X_train, Y_train) #score method gives accuracy directly
TrainingAccDT = tracDT * 100
print(f"Training Accuracy: {TrainingAccDT:.2f}%")


#model testing accuracy
print('====================DT Training Accuracy===============')
teacDT = accuracy_score(Y_test, PredictionDT)
testingAccDT = teacDT * 100
print(f"Testing Accuracy: {testingAccDT:.2f}%")
