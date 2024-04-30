import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
import pickle
import re
import nltk
from nltk.corpus import stopwords
import string

nltk.download('stopwords')
warnings.filterwarnings('ignore')

df = pd.read_csv('dataset.csv')
df.drop(['permission', 'intent'],axis=1,inplace=True)
df.drop_duplicates(inplace=True)
print(df)
df.dropna(inplace=True,axis=0)
print(df)

def textPreprocessor(featureRecord):
    #Remove punctuations
    removePunctuation = [char for char in featureRecord if char not in string.punctuation]
    sentences =''.join(removePunctuation)

    #convert sentences to words
    words = sentences.split(" ")

    #normalize
    wordNormalized=[word.lower() for word in words]

    #remove stropwords
    finalWords=[word for word in wordNormalized if word not in stopwords.words("english")]

    return finalWords

features = df.iloc[:,0].values
label=df.iloc[:,[1]].values

wordVector = CountVectorizer(analyzer=textPreprocessor)

#Build Vocab
finalWordVocab = wordVector.fit(features)
bagOfWords = finalWordVocab.transform(features)
tfIdfObject = TfidfTransformer().fit(bagOfWords)

finalFeature = tfIdfObject.transform(bagOfWords)
pickle.dump(finalFeature,open('vectorizer1.pkl','wb'))

X_train,X_test,Y_train,Y_test = train_test_split(finalFeature,label, test_size=0.2,random_state=42)
print(X_train)

rf_model = RandomForestClassifier(n_estimators=60)
rf_model.fit(X_train, Y_train)
pickle.dump(rf_model,open('rf1.pkl','wb'))
predictions_rf = rf_model.predict(X_test)
tn_rf, fp_rf, fn_rf, tp_rf = confusion_matrix(y_true=Y_test, y_pred=predictions_rf).ravel()
accuracy_rf = (tp_rf + tn_rf) / (tp_rf + tn_rf + fp_rf + fn_rf)
precision_rf = tp_rf / (tp_rf + fp_rf)
recall_rf = tp_rf / (tp_rf + fn_rf)
print("accuracy_rf --> ", accuracy_rf)
print("precision_rf --> ", precision_rf)
print("recall_rf --> ", recall_rf)

svm_model = svm.LinearSVC()
svm_model.fit(X_train, Y_train)
pickle.dump(svm_model,open('svm1.pkl','wb'))
predictions_svm = svm_model.predict(X_test)
tn_svm, fp_svm, fn_svm, tp_svm = confusion_matrix(y_true=Y_test, y_pred=predictions_svm).ravel()
accuracy_svm = (tp_svm + tn_svm) / (tp_svm + tn_svm + fp_svm + fn_svm)
precision_svm = tp_svm / (tp_svm + fp_svm)
recall_svm = tp_svm / (tp_svm + fn_svm)
print("accuracy_svm --> ", accuracy_svm)
print("precision_svm --> ", precision_svm)
print("recall_svm --> ", recall_svm)
