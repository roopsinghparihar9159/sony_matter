from tkinter import *
from  tkinter import ttk
import requests
from sys import exit
import json

def ptiApiStatus():
	url="http://webhook.multitvsolution.com/status"
	try:
		r=requests.get(url)
		if(r.status_code == 200):
			status='True'
		else:
			status='False'
	except requests.exceptions.ConnectionError:
		status='False'
	except KeyboardInterrupt:
		exit()
	return(status)

def transcodingApi():
	url="http://webhook.multitvsolution.com:7005/status"
	try:
		r=requests.get(url)
		if(r.status_code == 200):
			status='True'
		else:
			status='False'
	except requests.exceptions.ConnectionError:
		status='False'
	except KeyboardInterrupt:
		exit()
	return(status)

def transcodingList():
	url="http://webhook.multitvsolution.com:7005/list"
	if(transcodingApi() == 'True'):
		r=requests.get(url)
		return(json.loads(r.text))
	
root = Tk()
#lab1 = Label(root)
#lab2 = Label(root)
root.title("Transcoding Monitoring")
root.geometry("300x300")
pendingFrame=Frame(root)
pendingFrame.pack()
"""frame=ttk.Treeview(pendingFrame)
frame['columns']=('app_id','content_id','qc','Transcoding','Uploaded','sprite')
frame.column("#0", width=0,  stretch=NO)
frame.column("app_id",anchor=CENTER, width=80)
frame.column("content_id",anchor=CENTER,width=80)
frame.column("qc",anchor=CENTER,width=80)
frame.column("Transcoding",anchor=CENTER,width=80)
frame.column("Uploaded",anchor=CENTER,width=80)
frame.column("sprite",anchor=CENTER,width=80)

frame.heading("#0",text="",anchor=CENTER)
frame.heading("app_id",text="Id",anchor=CENTER)
frame.heading("content_id",text="Name",anchor=CENTER)
frame.heading("qc",text="Rank",anchor=CENTER)
frame.heading("Transcoding",text="States",anchor=CENTER)
frame.heading("Uploaded",text="States",anchor=CENTER)
frame.heading("sprite",text="States",anchor=CENTER)"""
#lab1.pack()
#lab2.pack()

def update():
	label1 = Label(root, text="PTI Webhook API: %s" % (ptiApiStatus()))
	label1.grid(column=0,row=0)
	label2 = Label(root, text="Transcoding API: %s" % (transcodingApi()))
	label2.grid(column=20,row=0)
	for data in json.dumps(transcodingList()):
		print(data)
	root.after(10000, update)
 

update()
root.mainloop()