from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("MODEL_KEY").encode()
fernet = Fernet(KEY)

with open("model/diabetes_model.pkl", "rb") as f:
    model_data = f.read()

encrypted_data = fernet.encrypt(model_data)

with open("model/diabetes_model_encrypted.pkl", "wb") as f:
    f.write(encrypted_data)

print("Model encrypted successfully.")
