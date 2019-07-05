import pandas as pd
from sklearn.tree import DecisionTreeClassifier as dt
from sklearn.metrics import accuracy_score
import time
crops=''
prediction=''
def _predict_model(model,x_test,status):
    model,x_test=model,x_test
    status.config(text='Done with prediction...')
    print('Done with prediction')
    res=model.predict(x_test)
    #print(list(zip(crops,res)))
    return res

def _create_model(x_train,y_train,status):
    x_train,y_train=x_train,y_train
    model=dt()
    model.fit(x_train,y_train)
    status.config(text='Done with modelbuilding...')
    print('Done with modelbuilding...')
    return model

def _split_data(xy,status):
    x,y=xy
    x_train,x_test=x[:-len(crops)],x[-len(crops):]
    y_train=y[:-len(crops)]
    status.config(text='Length of x_train:: '+str(len(x_train)))
    status.config(text='Length of x_test::,'+str(len(x_test)))
    status.config(text='Length of y_train::'+str(len(y_train)))
    return x_train,x_test,y_train

def _sep_feature_target(vectors,status):
    x=vectors.values[:,1:]#features
    y=vectors.values[:,0]#target
    status.config(text='Done with feature and target extraction...')
    print('Done with feature extraction...')
    return x,y

def _create_vectors(filename,data,status):
    global crops
    district,season,area=data
    all_data=pd.read_csv(filename)
    crops=list(set(all_data['Crop']))
    #return all_data
    for crop in crops:
        all_data=all_data.append({'District_Name':district,'Season':season,'Area':area,'Crop':crop,'Production':0},ignore_index=True)
    #return all_data
    vectors=pd.get_dummies(all_data)
    status.config(text='Done Dummies...')
    print('Done dummies...')
    return vectors
    
def _find_best_crop(filename,data,status):
    global  prediction
    x_train,x_test,y_train=_split_data(_sep_feature_target(_create_vectors(filename,data,status),status),status)
    predicted=_predict_model(_create_model(x_train,y_train,status),x_test,status)
    res=sorted(list(zip(crops,predicted)),key=lambda x:x[1],reverse=True)[:5]
    print(res)
    return res
def iter_find_best_crop(filename,test_data,status=None):
    print(filename,test_data)
    return [_find_best_crop(filename,data,status) for data in test_data]
