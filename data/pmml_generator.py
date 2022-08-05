def load_data():
    '''
    此处为加载鸢尾花数据集，并划分数据集
    return:训练数据、测试数据
    '''
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    """-----------------加载数据----------------------------"""
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target 
    """-------------------划分数据集------------------------"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    print("数据准备完毕！！")
    return X_train, X_test, y_train, y_test 
 
 
def modelTrain(X_train, X_test, y_train, y_test):
    '''
    定义逻辑回归模型
    return ：模型评估和模型
    '''
    print("---------------开始训练-------------------------")
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    """-------------------模型训练---  -------------------"""
    lr = LogisticRegression(C=5, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='multinomial',
              n_jobs=None, penalty='l2', random_state=None, solver='lbfgs',
              tol=0.0001, verbose=0, warm_start=False)
    
    
    from sklearn2pmml.pipeline import PMMLPipeline
    
    pmmPipe = PMMLPipeline([
            ('scaler',StandardScaler()),
            ('logisticRegression',lr)])
    
    pmmPipe.fit(X_train, y_train)
    #模型评估
    pipescore = pmmPipe.score(X_test,y_test)
    
    
    return pipescore,pmmPipe
    
def modelSave(path,pipmodel):
    '''
    path：保存路径
    pipmodel：需要保存的模型
    '''
    
    from sklearn2pmml import sklearn2pmml
    sklearn2pmml(pipmodel,path,with_repr = True) 
    print("模型保存成功")
    
    
def loadModel(path):
    '''
    path：模型加载路径
    '''
    """-------------------加载模型----------------------"""
    from pypmml import Model
    model = Model.fromFile(path)
    print("-------------模型加载完成--------------------")
    return model

if "__main__" == __name__:
    import numpy as np
    #加载数据
    X_train, X_test, y_train, y_test  = load_data()
    #模型训练
    pipescore,pipeline = modelTrain(X_train, X_test, y_train, y_test)
    path = './irisLogisticregress.pmml'
    #模型保存
    modelSave(path,pipeline)
    #模型的加载
    model = loadModel(path)
    print(X_test)
    result = np.array(model.predict(X_test))
    print(f'res:{result}')
    #将概率值转换为类别
    y_test_pred = np.argmax(result, axis=1)
    print("预测结果：\n",y_test_pred)
 
    