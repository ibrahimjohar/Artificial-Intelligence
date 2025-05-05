#CLASSIFICATION

#SUPPORT VECTOR MACHINE (SVM)
#set of supervised learning algos used primarily for classification tasks (can also be used for regression)

#key idea: to find the optimal hyperplane that separates the classes w/ the largest margin, thus improving generalization
#goal is to maximize the margin between the classes

#linear SVM:
# For linearly separable data, SVM finds the hyperplane that perfectly
# separates the classes. This is the simplest case, and the model does not require any additional tricks.

#non-linear SVM:
# SVM uses a kernel function to map the data into a higher-dimensional feature space, 
# where a linear decision boundary can be found.

#popular kernel functions:
## linear kernel: K(x, x’) = x^T x’
## polynomial kernel: K(x, x’) = (x^T x' + c)^d
## radial basis function (RBF) kernel: K(x, x’) = e^(−γ||x−x'||^2)

# The kernel trick allows SVM to find a non-linear decision boundary in the original
# feature space without explicitly calculating the transformation.

from sklearn import datasets
from sklearn.svm import SVC 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#load dataset 
iris = datasets.load_iris()
X = iris.data

y = iris.target
y = (y==0).astype(int) #convert binary classification problem

#split data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#train SVM model with RBF kernel
svm = SVC(kernel='rbf', C=1, gamma='scale')
svm.fit(X_train, y_train)

#make predictions
y_pred = svm.predict(X_test)

#evaluate model 
print("SVM Accuracy: ", accuracy_score(y_test, y_pred))
