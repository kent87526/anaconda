import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

import pickle
import os

Frame=[]
Status=[]
Ballposition=[]
PlatformPosition=[]
Bricks=[]
filenamelist = []

log = ['D:\\anao\\MLGame-master\\games\\arkanoid\\log\\2019-10-14_23-47-24.pickle',
       'D:\\anao\\MLGame-master\\games\\arkanoid\\log\\2019-10-15_02-10-25.pickle',
       'D:\\anao\\MLGame-master\\games\\arkanoid\\log\\2019-10-15_02-23-33.pickle',
       'D:\\anao\\MLGame-master\\games\\arkanoid\\log\\2019-10-15_02-24-50.pickle',
       'D:\\anao\\MLGame-master\\games\\arkanoid\\log\\2019-10-15_02-26-11.pickle',
       'D:\\anao\\MLGame-master\\games\\arkanoid\\log\\2019-10-15_02-27-36.pickle',
       ]

for filename in log: 
    with open(filename,"rb") as f:
        data_list = pickle.load(f)
    for i in range(0,len(data_list)):
        Frame.append(data_list[i].frame)
        Status.append(data_list[i].status)
        Ballposition.append(data_list[i].ball)
        PlatformPosition.append(data_list[i].platform)
        Bricks.append(data_list[i].bricks)

import numpy as np
PlatX=np.array(PlatformPosition)[:,0][:,np.newaxis]
PlatX_next=PlatX[1:,:]
instruct=(PlatX_next-PlatX[0:len(PlatX_next),0][:,np.newaxis])/5


Ballarray=np.array(Ballposition[:-1])
pp=np.array(Ballposition[1:])
x=np.hstack((Ballarray,pp,PlatX[0:-1,0][:,np.newaxis]))

y=instruct
print(x)



from sklearn.model_selection import train_test_split


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.0001, random_state = 0)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(x_train, y_train)

print(x_test)
y_knn=neigh.predict(x_test)

acc=accuracy_score(y_knn, y_test)

filename="svc_example.sav"
pickle.dump(neigh, open(filename, 'wb'))


l_model=pickle.load(open(filename, 'rb'))
yp_l=l_model.predict(x_test)
print("acc load: %f " % accuracy_score(yp_l, y_test))# -*- coding: utf-8 -*-
