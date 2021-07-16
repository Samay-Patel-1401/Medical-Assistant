import pickle
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import pandas as pd

data = pd.read_csv("dataset/heart.csv")

data_c = data.copy()

category_cols = ['sex','exng','caa','cp','fbs','restecg','slp','thall']
numeric_cols = ["age","trtbps","chol","thalachh","oldpeak"]

Y = data_c['output']
X = data_c.drop(['output'],axis=1)

scaler = StandardScaler()
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

pickle.dump(scaler, open("scaler.pkl", "wb"))

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2)

clf = SVC(kernel = "rbf", gamma = 0.18, C = 1)
clf.fit(X_train, Y_train)

pickle.dump(clf, open("clf.pkl", "wb"))

from sklearn import metrics
Y_pred = clf.predict(X_train)
print("Accuracy:",metrics.accuracy_score(Y_train, Y_pred))
print("Precision:",metrics.precision_score(Y_train, Y_pred))
print("Recall:",metrics.recall_score(Y_train, Y_pred))
print()

Y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))
print("Precision:",metrics.precision_score(Y_test, Y_pred))
print("Recall:",metrics.recall_score(Y_test, Y_pred))
print()

Y_pred = clf.predict(X)
print("Accuracy:",metrics.accuracy_score(Y, Y_pred))
print("Precision:",metrics.precision_score(Y, Y_pred))
print("Recall:",metrics.recall_score(Y, Y_pred))
