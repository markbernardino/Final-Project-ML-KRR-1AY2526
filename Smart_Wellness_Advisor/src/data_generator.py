import numpy as np
import pandas as pd
import random

RND=42
np.random.seed(RND)
random.seed(RND)

def generate_row():
    age = int(np.clip(np.random.normal(30,8),16,80))
    bmi = round(np.random.normal(25,4),1)
    sleep = round(np.random.normal(7,1.5),1)
    activity = np.random.choice(['low','moderate','high'], p=[0.4,0.4,0.2])
    water = round(np.random.normal(1.8,0.5),1)
    sugar = np.random.choice(['low','high'], p=[0.7,0.3])
    stress = np.random.choice(['low','medium','high'], p=[0.5,0.35,0.15])
    score = 0
    if bmi>27: score+=2
    elif bmi>24: score+=1
    if activity=='low': score+=2
    elif activity=='moderate': score+=1
    if sleep<6: score+=1
    if sugar=='high': score+=1
    if stress=='high': score+=1
    risk = 'high' if score>=4 else ('moderate' if score>=2 else 'low')
    return {'age':age,'bmi':bmi,'sleep_hours':sleep,'activity_level':activity,'water_intake_l':water,'sugar_intake':sugar,'stress_level':stress,'risk':risk}

def generate_dataset(n=1200, out_path='data/lifestyle_dataset.csv'):
    rows=[generate_row() for _ in range(n)]
    df=pd.DataFrame(rows)
    df.to_csv(out_path,index=False)
    print(f'Generated {n} rows to {out_path}')
    return df

if __name__=='__main__':
    generate_dataset()
