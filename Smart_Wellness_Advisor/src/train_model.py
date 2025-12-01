import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

DATA='data/lifestyle_dataset.csv'
MODEL='models/rf_model.joblib'
ENC='models/encoders.joblib'

def train():
    df=pd.read_csv(DATA)
    enc={}
    df2=df.copy()
    cat_cols=['activity_level','sugar_intake','stress_level']
    for c in cat_cols:
        le=LabelEncoder(); df2[c]=le.fit_transform(df2[c]); enc[c]=le
    le_y=LabelEncoder(); df2['risk']=le_y.fit_transform(df2['risk']); enc['risk']=le_y
    X=df2.drop(columns=['risk']); y=df2['risk']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
    clf=RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
    clf.fit(X_train,y_train)
    preds=clf.predict(X_test)
    print('Accuracy:', accuracy_score(y_test,preds))
    print(classification_report(y_test,preds,target_names=enc['risk'].classes_))
    joblib.dump(clf, MODEL)
    joblib.dump(enc, ENC)
    print(f'Saved model to {MODEL} and encoders to {ENC}')

if __name__=='__main__':
    train()
