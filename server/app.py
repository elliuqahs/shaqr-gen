from flask import Flask, request, jsonify
from scripts.shaqr import ShaQR

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from ShaQR"

@app.route("/generate", methods=['POST'])
def createNewQr():
    data = request.get_json()
    text = data['text']
    
    shaq_qr = ShaQR()
    newShaQr = shaq_qr.create_sha_qr(text)
    
    response = {
        "qr_code": newShaQr.decode()
    }
    
    return response, 201
    