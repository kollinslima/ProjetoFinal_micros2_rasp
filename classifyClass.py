import socket
import struct
import sys
import io
import threading
from PIL import Image
from time import sleep
import math
import imagehash
import mongoengine as me

database_name = 'librasDB'
me.connect(database_name)

class Symbols(me.Document):
    number = me.IntField()
    hashValue = me.StringField()

class Classify:

    def __init__(self):
        self.hashSize = 256
        self.neighbor = 3
        self.totalElement = 2
        self.lock = threading.Lock()
        self.mainList=[]
        self.pointList=[]
        self.classList=[]
        self.auxClassList=[]

        for i in range(0,self.totalElement):
#            self.classList.append(0)
            self.pointList.append([])
            self.mainList.append([])            

        database = Symbols.objects.all()
        if(database != None):
            for db_input in database:
                self.mainList[db_input.number].append(hex_to_hash(db_input.hashValue))
       

    def addImage(self,number):
        with (self.lock):
            image = Image.open('static/img0.jpg')
            imgHash = imagehash.average_hash(image,self.hashSize)
            self.mainList[number].append(imgHash)
            
            new_symbol = Symbol(number=number,hashValue=str(imgHash))
            new_symbol.save()

    def readPoints(self):
        return self.auxClassList

    def classifyImage(self):
        while True:
            try:
                self.classList = [0] * self.totalElement

                img = Image.open('static/img0.jpg')
                imgHash = imagehash.average_hash(img,self.hashSize)

                i = 0
                with (self.lock):
                    for bankList in self.mainList:
                        for hashElement in bankList:
                            self.pointList[i].append(math.sqrt((imgHash - hashElement)**2))

                        i = i+1
 
                for pointElement in self.pointList:
                    pointElement.sort()
                    #print(pointElement)        

                for i in range(0,self.neighbor):

                    try:
                        minValue = self.pointList[0][0]

                        index = 0
                        for j in range(1,self.totalElement):
                            if self.pointList[j][0] < minValue:
                                minValue = self.pointList[j][0]
                                index = j

                        if(minValue != 0):                  
                            self.classList[index] = self.classList[index] + (1/minValue)
                        else:
                            self.classList[index] = float("inf")

                        self.pointList[index].pop(0)                     

                    except IndexError:
                        pass

                self.auxClassList = self.classList
#                sleep(1)

            except FileNotFoundError:
                pass
