from cryptography.fernet import Fernet
import hashlib
import requests
from flask import Flask, request
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def recibir():
	if(request.method == 'GET'):
		return 'GET xd'
	else:
		texto = request.data
		llave = leerLlave()
		decrypt = decriptar(texto, llave)
		x = decrypt.split()
		if x[1] != hash(x[0]):
			return 'NO HUBO INTEGRIDAD DE LOS DATOS'
		with open("recibido.txt", "a") as f:
			f.write(str(texto)+' DECRIPTADO: '+str(x[0])+" digest: "+str(x[1])+' \n')
		return str(x[0])+" digest: "+str(x[1])

def leerLlave():
	file = open('key.key', 'r')
	key = file.read()  # The key will be type bytes
	file.close()
	return key

@app.route("/encriptar", methods=['GET', 'POST'])
@cross_origin()
def encriptar():
	if(request.method == 'GET'):
		return "GET XD"
	else:
		llave = leerLlave()
		mens = request.data
		hs = hash(mens)
		print(mens)
		f = Fernet(llave)
		cifrado = f.encrypt(mens+" "+hs)
		return str(cifrado)

def decriptar(mensajeCifrado, llave):
	f = Fernet(llave)
	decriptado = f.decrypt(mensajeCifrado)
	return decriptado.decode()

def hash(mensaje):
	mes = mensaje.encode()
	return hashlib.md5(mes).hexdigest()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
