#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv('dataset.csv')


# In[3]:


df.head()


# # Preprocessing And Feature Engineering

# In[4]:


df1 = df[['id', 'gender', 'age', 'hypertension', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke']]


# In[5]:


df1.head()


# In[6]:


df1.gender.value_counts()


# In[7]:


df1.drop('id', inplace=True, axis=1)


# In[8]:


df1 = df1[df1['gender'] != 'Other']


# In[9]:


df1.ever_married.value_counts()


# In[10]:


df1.work_type.value_counts()


# In[11]:


df1.Residence_type.value_counts()


# In[12]:


df1.smoking_status.value_counts()


# In[13]:


df1.head()


# In[18]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# In[15]:


X = df1.drop(columns=["stroke"])
y = df1["stroke"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# In[16]:


numeric_features = ["age", "avg_glucose_level", "bmi"]
categorical_features = [
    "gender",
    "ever_married",
    "work_type",
    "Residence_type",
    "smoking_status"
]


# In[19]:


numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Categorical transformer (impute most frequent + one hot encoding)
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])


# In[20]:


preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ],
    remainder="passthrough"  # This keeps hypertension as it is
)


# In[46]:


model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        penalty="l1",
        solver="liblinear"
    ))
])


# In[47]:


model.fit(X_train, y_train)
y_proba = model.predict_proba(X_test)[:, 1]


# In[48]:


threshold = 0.75
y_pred = (y_proba >= threshold).astype(int)


# In[49]:


print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


# In[50]:


import joblib
joblib.dump(model, "stroke_model.pkl")
print("Model saved as stroke_model.pkl")


# In[ ]:




