# diabetes.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Load and preprocess dataset
df = pd.read_csv('diabetes.csv')
X = df.drop(columns=['Outcome'])
y = df['Outcome']

# Scaling the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = SVC(probability=True)
model.fit(X_train, y_train)

# Predict function
def check_input(input_data: dict) -> str:
    # Convert input dict to DataFrame
    input_df = pd.DataFrame([input_data])
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]
    
    if prediction == 1:
        return f"⚠️ The patient is likely to have diabetes.\nProbability: {probability:.2%}"
    else:
        return f"✅ The patient is unlikely to have diabetes.\nProbability: {probability:.2%}"
