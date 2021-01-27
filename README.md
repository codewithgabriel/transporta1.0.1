Project Description
===================
name : transporta
version : 1.0.1
status : stable
program language : python
program language version : 3.7+


Author Information
==================
developer: O. Olaide Gabriel
email: olatoyeolaide@gmail.com
phone: 07083517016

Usage
==================
Installation (quick and easy)
==========================================
	git clone https://github.com/codewithgabriel/transporta1.0.1.git
	sudo chmod +x install.sh
	./install.sh

step 1: Get started
===============================================
	download transporta using git clone.
	example:
		cd /opt
		git clone https://
step 2: Install modules in requirements.txt with pip3
=======================================================
	example:
		pip3 install -r requirements.txt

step 3: Make transporta.py executable using chmod
===================================================
	example:
		chmod +x transporta.py
step 4: Start transporta as host
=========================================================
	example:
		./transporta -H 192.168.43.1 5050 -st MAX
	where:
		-H : start transporta as HOST machine.
		192.168.43.1 : is the ipv4 address of the HOST machine.
		5050 :  is the port to listen to.
		-st : -st is used to set the amount of bytes to send and recv from client per connection.
			MAX : 100 000 000 bytes
			MIN : 100 000 bytes
			DEF : 1000 bytes
step 5: Start CLIENT from remote machine.
==============================================
	example:
		./transporta -C 192.168.43.1 5050 -s "hello"
	where:
		-C : start transporta as CLIENT machine.
		192.168.43.1 :  is the ipv4 address of the HOST machine.
		5050 :  is the port HOST machine is listenning to.
		-s : tells transporta to send a bytes to the HOST.
		hello : is the bytes sent to HOST.

How to send file over transporta network
========================================
	example 1: -t or --transport:
		./transporta -C 192.168.43.1 5050 -t "/root/Desktop/sample.mp4 , /root/Videos"
	description:
		"where to save the sent file on local machine ,  file to transport on remote machine"
	
	example 2: -d or --drag:
		./transporta -C 192.168.43.1 5050 -t "/root/Desktop/sample.mp4 , /root/Videos"
	description:
		"local file to send location , where to save the sent file ons remote machine"


Report bugs or issue
=====================
olatoyeolaide@gmail.com

	
		
	
	
			
		 


