import socket
import struct
import sys
import io
#import _thread
import classifyClass
import threading
from PIL import Image
from time import sleep
#from shutil import copy2
import os

class SocketCon:

    def __init__(self, arg, portSocket=5000):
        self.classImagem = arg
        self.portSocket = portSocket
        self.address = ("0.0.0.0", self.portSocket)


    def data_out(self,con,cliente):
        print ('Conectado por', cliente)
        con.settimeout(5.0)

#    for i in range(1,10):
#        con.send(str(i).encode())
#        sleep(1)

        while True:
            buf = b''
            while len(buf)<4:
                try:
                    buf += con.recv(4-len(buf))
        #            buf = con.recv(4)
                except socket.timeout:
                    print('Finalizando conexao do cliente', cliente)
                    con.close()
                    return

            size = struct.unpack('!i', buf)

            print ("receiving %d bytes" % int(size[0]))

            if (int(size[0]) < 0):
                con.close()

            imageSize = 0
#            img = io.BytesIO()

         
            with open('static/tmp.jpg', 'wb') as img:
                while imageSize < int(size[0]):
                    try:
                        data = con.recv(1024)
                    except socket.timeout:
                        print('Finalizando conexao do cliente', cliente)
                        con.close()
                        return
 
                    imageSize += len(data)
  
                    img.write(data)
                    img.flush()      
    
                os.rename('static/tmp.jpg','static/img0.jpg')
#                imageReceived = Image.open(img)

#                print(imageReceived.verify())

        print('Finalizando conexao do cliente', cliente)
        con.close()
        return
#############################################################
    def data_in(self,con,cliente):

        last_msg = " "        
        counter = 0
        while True:
            counter = counter + 1
            classificacao = self.classImagem.readPoints()
            winner = "sem vencedores"
#            print(classificacao)

            if classificacao:               
                maxValue = 0;
                j = 0;
                for i in classificacao:                    
                    if(i > maxValue):
                        maxValue = i
                        winner = str(j) + "\n"
                    j = j+1;

            if counter > 10000:
#                print(classificacao)
                counter = 0
     #           last_msg = winner
                con.send(winner.encode('utf-8')) 

#############################################################

    def run(self):

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except (socket.error, msg):
            print ('Failed to create socket.Error code:' + str(msg[0]) + ', Error    message')
            sys.exit()

        print ('Socket Created')

        s.bind(self.address)
        s.listen(5)

        while True:
            try:
                (con, cliente) = s.accept()
                print ('got connected from', con,cliente)
                t1 = threading.Thread(target=self.data_in, args=(con,cliente))
                t2 = threading.Thread(target=self.data_out, args=(con,cliente))
                t1.start()
                t2.start()

            except KeyboardInterrupt:
                break
#        _thread.start_new_thread(conectado, tuple([con, cliente]))

        print ('received, yay!')
        con.close()



