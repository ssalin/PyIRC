#!/usr/bin/python
# use twisted??
#SERVER CODE WRITTEN BY SAM SALIN FOR CS 494 5/4/17

#IMPORT
import socket
import sys
import threading
host = "localhost"
port = 7
rooms = []
#globals

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_adr = ('localhost', port)
s.bind(serv_adr)
                        
#user class
class user(object):
        def __init__(self, username, addr, con):
                #print("in user init")
                self.addr = addr
                self.name = username
                self.con = con
        def getaddr(self):
                #print ("in user get")
                return self.addr
        def getcon(self):
                return self.con
        def getname(self):
                #print("in user getname")
                return self.name
#room class
class room(object):
        global sk
        def __init__(self, name, creator, addr,con):
                #print("room init")
                self.name = name # stor the room name
                self.users = []
                self.users.append(user(creator, addr,con))
        def add(self, usr,addr,con):
                #print ("in add")
                tmp = user(usr, addr, con)
                self.users.append(tmp)
        def leave(self, addr,usr):
                #print ("in leave_room") #usr "leaving" room_name
                j = 0
                for i in self.users:
                 #       print (i.getname())
                 #       print (usr)
                        if usr == i.getname():
                 #               print ("Popping")
                                self.users.pop(j)
                 #               print ("Popped")
                        j+=1 #
                return
        def getname(self):
                return self.name
        def send(self, name, usr, msg): #roomname, sending user, message body
                #print("in room.send")
                snd = usr + '@' + name + ':'+ msg # get message packet ready
                snd=snd.encode('utf-8')
                for i in self.users: #iterate though user list
                        c = i.getcon()
                        c.send(snd)
        def listusers(self,con):
               # print ("in room listusers")
                for i in self.users:
                        name = i.getname()
                #        print(name)
                        con.send(name.encode('utf-8'))
                

#HELPER FUNCTIONS
#function for listing users in a room
def listrooms(con):
        #show all avalible chatrooms
        for i in rooms:
                con.send(i.getname().encode('utf-8'))
        return

def createroom(roomname,addr,usr,con):
        #make a new chatroom
        #should make sure no room already exists
        tmp = room(roomname,usr,addr,con)
        rooms.append(tmp)
        return

def joinroom(roomname,addr,usr,con):
        #iterate though room list
        #should check and make sure the user isnt already in the room
        for i in rooms:
                print (i.getname())
                if i.getname() == roomname:
                        i.add(usr,addr,con)
                        return 0
        return 1 # means room does not exist

def leaveroom(roomname,addr,usr):
        #should make sure room exists
        #should make sure user is actually in the room
        for i in rooms:
                print(i.getname())
                if i.getname() == roomname:
                        i.leave(addr,usr)
        return

def parse(data, addr, con):
        strdata = data.decode('utf-8')
        usr,flag, name, msg = strdata.split(',') # break incoming packets into subfeilds
        flag = int(flag)
        #print(usr)
        if flag == 1: # list rooms
                return listrooms(con)
        elif flag == 2: # join room
                return joinroom(name, addr, usr, con)
        elif flag == 3: # create room
                return createroom(name, addr, usr, con)
        elif flag == 4: #leave room
                return leaveroom(name, addr, usr)
        elif flag == 5: #message
                #find the right room/ make sure it exists
                for room in rooms:
                        if name == room.getname(): #found the right room!
                                room.send(name,usr,msg) #send message to everybody?
                return
        elif flag == 6: #list room members
                print ("in list room members call")
                for room in rooms:
                       if name == room.getname():
                               room.listusers(con)
                return

def client(con,addr): # function run by each client thread
        print("Client Sucessfully Connected!")
        while 1:
                try:
                        data = con.recv(10000)
                        parse(data, addr, con)
                        ctr = 0
                except:
                        if (con._closed):
                                print("connection closed!")
                                con.close()
                                return
                        pass
        print ("gonna close the sockets!")
        

def main():
        s.listen(5) #potentially 5 queued connections. arbitrary number choice.
        while 1:
                try:
                        conn, addr = s.accept()
                        conn.setblocking(0)#so the sockets dont interfere with one another
                        threading.Thread(target=client, args=(conn,addr)).start()
                except:
                        pass
        

        s.close()
        sk.close()
                
if __name__=="__main__":
    main()
