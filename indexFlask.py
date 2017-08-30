import threading
import flaskServer
import classifyClass
from flask import Flask, render_template, request

app = Flask(__name__)
classImg = classifyClass.Classify()
server = flaskServer.SocketCon(arg=classImg)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/print', methods=['POST'])
def print_screen():    
    number = request.form['numero']
    classImg.addImage(int(number))
    return render_template('index.html')

if __name__ == '__main__':

   threadServer = threading.Thread(target=server.run)
   threadServer.start()
   threadClassify = threading.Thread(target=classImg.classifyImage)
   threadClassify.start()
   app.run(host = '0.0.0.0', port=8080)

