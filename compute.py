import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sklearn.metrics import confusion_matrix
from subprocess import check_call
#from sklearn.datasets import load_iris
import pydot

#names = ['id', 'ct', 'ucsi', 'ucsh', 'ma', 'secs','bn','bc', 'nm','mi','class']
def computeTarget(a,b,c,d,e,f,g,h,i):

    engine = create_engine(URL(
    drivername="mysql",
    username="root",
    password="",
    host="localhost",
    database="soumitradata"
    ))

    conn = engine.connect()

    dataset = pd.read_sql(sql='SELECT  ct, ucsi, ucsh, ma, secs, bn, bc, nm, mi, class FROM breast_cancer' , con=conn)

    print(dataset.head())

    dataset = dataset[['ct', 'ucsi','ucsh', 'ma','secs', 'bn', 'bc', 'nm', 'mi', 'class']]

    #dataset = dataset.dropna()

    X = dataset.drop('class', axis =1)
    y = dataset['class']

    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state = 1)
    model = tree.DecisionTreeClassifier(random_state= 1)
    print(dataset.head())
    #print(model)

    #iris = load_iris()
    k = a
    l = b
    m = c
    n=  d
    o = e
    p = f
    q = g
    r = h
    s = i
    print(model.fit(X_train, y_train))
    values = np.array([[k, l, m, n, o, p, q, r, s]], dtype=np.float64)
    #print(values)
    print(model.predict(values))
    #return model.predict(values)
    #tree.export_graphviz(model, out_file = 'tree.png')
    #(graph,) = pydot.graph_from_dot_file('C:/Users/Soumi/ThesisWork/tree.dot')
    #graph.write_png('tree.png')

    #dot = "C:\Users\Soumi\ThesisWork\graphviz-2.38\release\bin\dot.exe"
    #dot 'C:\Users\Soumi\ThesisWork\tree.dot' -Tpng -O 'C:\Users\Soumi\ThesisWork\tree.png'
'''if __name__ == '__main__':
    print (computeTarget(a,b,c,d,e,f,g,h,i))
'''    
