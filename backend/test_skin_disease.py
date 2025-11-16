from fastapi.testclient import TestClient 
from main import app 
import json, os 
import torch 
client = TestClient(app) 
'print("? Test client ready")' 
'print("Test the API with: py test_skin_disease.py")' 
