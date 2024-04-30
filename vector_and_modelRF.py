import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
import pickle
import re

warnings.filterwarnings('ignore')
# c dataet rồi thì tiến hành đọc và ở đây chỉ quan tâm đến API call thôi, do yêu cầu bài toán chỉ là phân tích hàm.
df = pd.read_csv('dataset.csv')

# Xóa 2 cột permision và intent khỏi dataset
df.drop(['permission', 'intent'],axis=1,inplace=True)
df.drop_duplicates(inplace=True)
print(df)
df.dropna(inplace=True,axis=0)
print(df)

# đoạn này chính là việc vector hóa câu chữ trong dòng của API call bằng
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text
df['APIcall']=df['APIcall'].apply(preprocess_text)

tf = TfidfVectorizer(stop_words='english',max_features=1000)
X = tf.fit_transform(df['APIcall']).toarray()
X = pd.DataFrame(X)
Y= df["label"]
print(X)
print(Y)
pickle.dump(tf,open('vectorizer.pkl','wb'))

# Train m hình là từ đây
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

rf_model = RandomForestClassifier(n_estimators=60)
rf_model.fit(X_train, Y_train)
pickle.dump(rf_model,open('rf.pkl','wb'))
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
pickle.dump(svm_model,open('svm.pkl','wb'))
predictions_svm = svm_model.predict(X_test)
tn_svm, fp_svm, fn_svm, tp_svm = confusion_matrix(y_true=Y_test, y_pred=predictions_svm).ravel()
accuracy_svm = (tp_svm + tn_svm) / (tp_svm + tn_svm + fp_svm + fn_svm)
precision_svm = tp_svm / (tp_svm + fp_svm)
recall_svm = tp_svm / (tp_svm + fn_svm)
print("accuracy_svm --> ", accuracy_svm)
print("precision_svm --> ", precision_svm)
print("recall_svm --> ", recall_svm)