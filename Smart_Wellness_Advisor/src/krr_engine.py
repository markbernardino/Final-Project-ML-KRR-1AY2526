import joblib
import numpy as np
MODEL='models/rf_model.joblib'
ENC='models/encoders.joblib'
_model=None; _enc=None

def load_model_enc():
    global _model,_enc
    if _model is None:
        _model=joblib.load(MODEL)
    if _enc is None:
        _enc=joblib.load(ENC)
    return _model,_enc

def ml_predict(user):
    model,enc=load_model_enc()
    X=[float(user.get('age',30)),
       float(user.get('bmi',25.0)),
       float(user.get('sleep_hours',7.0)),
       float(user.get('water_intake_l',1.8)),
       int(enc['activity_level'].transform([user.get('activity_level','moderate')])[0]),
       int(enc['sugar_intake'].transform([user.get('sugar_intake','low')])[0]),
       int(enc['stress_level'].transform([user.get('stress_level','low')])[0])]
    X_arr=np.array(X).reshape(1,-1)
    y_pred=model.predict(X_arr)[0]
    label=enc['risk'].inverse_transform([y_pred])[0]
    probs=model.predict_proba(X_arr)[0]
    prob_dict={enc['risk'].classes_[i]:float(probs[i]) for i in range(len(probs))}
    return label, prob_dict

def apply_rules(user, ml_label):
    label=ml_label; recs=[]
    try:
        bmi=float(user.get('bmi',0)); sleep=float(user.get('sleep_hours',7)); water=float(user.get('water_intake_l',1.8))
        activity=user.get('activity_level','moderate'); sugar=user.get('sugar_intake','low'); stress=user.get('stress_level','low')
    except:
        return ml_label, []
    if bmi>=30 and activity=='low':
        label='high'; recs.append('High BMI + low activity — consult provider and increase activity.')
    if sleep<5 and label!='high':
        if label=='low': label='moderate'
        recs.append('Improve sleep: aim for 7-8 hours.')
    if sugar=='high' and label=='moderate':
        label='high'; recs.append('Reduce sugar intake.')
    if stress=='high':
        recs.append('Practice stress reduction techniques.')
    if water<1.2:
        recs.append('Increase daily water intake to 1.5–2 L.')
    recs=list(dict.fromkeys(recs))
    return label, recs

def assess(user):
    ml_label, probs = ml_predict(user)
    final_label, recs = apply_rules(user, ml_label)
    return {'ml_label':ml_label, 'ml_probs':probs, 'final_label':final_label, 'recommendations':recs}

if __name__=='__main__':
    print(assess({'age':32,'bmi':28.5,'sleep_hours':5.5,'activity_level':'low','water_intake_l':1.0,'sugar_intake':'high','stress_level':'high'}))
