import pandas as pd
import pickle

with open('/Users/vineeshreddy/Desktop/venv/ensemblemodel.pkl', 'rb') as m:
    disease_predictor = pickle.load(m)

dataset_path="/Users/vineeshreddy/Desktop/venv/dataset/dataset.csv"
df=pd.read_csv(dataset_path)

precautions_df=pd.read_csv("/Users/vineeshreddy/Desktop/venv/dataset/disease_precaution.csv")

disease_names = list(disease_predictor.classes_)

def getsymptoms():
    symptoms=df.columns[1:].tolist()
    return symptoms

def calculateThreshold(threshold):
    combinations_to_check = [[10, 10], [10, 9], [9, 10], [9, 9]]
    exists_combination = any(set(combination).issubset(threshold) for combination in combinations_to_check)
    if exists_combination:
        return 1
    if (10 in threshold) or (9 in threshold):
        return 2
    else:
        return 3

def cleaninput(syms):
    age,gender=syms[0],syms[1]
    syms=syms[2:]
    symptoms=[]
    threshold=[]
    for i in range(len(syms)):
        if i%2==0:
            symptoms.append(syms[i])
        else:
            threshold.append(int(syms[i]))
    return age,gender,symptoms,threshold

def calculateforagegender(threshold,age,gender):
    pass

def recommend(warning):
    if warning==1:
        message="If you experience severe symptoms, it is crucial to consult a doctor immediately for a comprehensive evaluation and appropriate medical intervention."
    elif warning==2:
        message="For any health concerns or symptoms, it is advisable to consult a doctor for a professional assessment and guidance on the best course of action."
    else:
        message="While following the listed precautions is important, in case of persistent or worsening symptoms, it is recommended to consult a doctor for personalized advice and further medical evaluation."    
    return message   


def predictDisease(user_symptoms, top_n=2):
    user_input = {}
    for s in df.columns[1:]:
        user_input[s] = 1 if s in user_symptoms else 0
    user_data = pd.DataFrame([user_input])
    feature_names = list(user_data.columns)
    symptoms_array = user_data.to_numpy()
    predicted_probabilities = disease_predictor.predict_proba(symptoms_array)[0]
    top_disease_indices = predicted_probabilities.argsort()[-top_n:][::-1]
    top_diseases = [disease_names[i] for i in top_disease_indices]
    return top_diseases


def getPrecaution(diseases):
    info_disease1 = precautions_df[precautions_df['label_dis'] == diseases[0]].iloc[0]
    des1=info_disease1.iloc[1:2].tolist()
    pre1 = info_disease1.iloc[2:7].tolist()

    info_disease2 = precautions_df[precautions_df['label_dis'] == diseases[1]].iloc[0]
    des2=info_disease2.iloc[1:2].tolist()
    pre2 = info_disease2.iloc[2:7].tolist()

    description=des1+des2
    precaution=pre1+pre2
    return description,precaution

def getData(syms):
    age,gender,symptoms,threshold=cleaninput(syms)
    warning=calculateThreshold(threshold)
    message=recommend(warning)
    diseases=predictDisease(symptoms)
    description,precaution=getPrecaution(diseases)
    return diseases,description,precaution,message