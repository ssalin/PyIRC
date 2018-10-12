#!/usr/bin/python
#CURRENT BUGS AND COMING REVISIONS
#multithreaded version where
        #one thread handles user actions
        #one thread listens for messages
#import
import socket
import sys
import threading
import time

#definintions / globals
USERNAME = ""
host = "localhost"
port = 7
s_pkt = ""
r_pkt = ""
running = 1
#make global socket for the threads to use
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#OPEN A SOCK STREAM BOIIII
s.connect((host,port)) #CONNECT THE SOCKS
        
def pkt_snd():
        global s
        global s_pkt
        s_pkt = s_pkt.encode('utf-8')
        s.send(s_pkt)   #SEND 
        #print ("sent packet: ")
        #print (s_pkt)
        return

def menu(tmp, m):
    flag = 1
    t= 0
    while (flag):
        if m|t:
            print ("Command Menu")
            print ("1: List Rooms")
            print ("2: Join Room")
            print ("3: Create room")
            print ("4: Leave Room")
            print ("5: Send Message")
            print ("6: list room members")
            tmp = input ("What are you doing: ")
            tmp = int(tmp)
            if (tmp <= 6) & (tmp >= 1): #make sure user gave valid choice
                return tmp
            print ("invalid choice!")
            t = 1 # show choices if they give bad input

def pkt_mk(choice):
        global s_pkt
        # get room name
        name = ""
        msg = ""
        if choice != 1:
                name = input ("enter room name: ")
        if choice == 5:
                msg = input ("enter message: ")
        choice = str(choice)
        s_pkt = [USERNAME,choice,name,msg]
        s_pkt = ",".join(s_pkt)
        #print (s_pkt)
        return

def send():
        choice = 0
        m = 1
        global running
        while running:
                choice = menu(choice, m)
                pkt_mk(choice)
                pkt_snd()

def listen(): #HEY. LISTEN. HEY. LISTEN. 
        global s
        global running
        while running:
                try:
                        time.sleep(2) # need to figure out a better way to make the print happen at a more convenient time
                        r_pkt = s.recv(10000)
                        r_pkt = r_pkt.decode('utf-8')
                        #print ("received: ")
                        print(r_pkt)
                except:
                        running = 0
                        print ("connection closed")
                        s.close()
                
def main():
        global USERNAME
        m = 1 # show menu choice variable
        #m = input ("enter 0 for no men anything else for menu") # get option to show menu all the time or nah
        USERNAME = input ("Enter your username: ")
        threading.Thread(target=send, args =()).start() #pkt_snd(r_pkt)
        threading.Thread(target=listen, args=()).start()
if __name__=="__main__":
    main()


