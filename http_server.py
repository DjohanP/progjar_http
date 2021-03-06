import datetime
import codecs
import socket
import sys
import threading
import os
import shutil
import cgi, cgitb

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
if len(sys.argv) == 1:
	port = 10000
else:
	port = int(sys.argv[1])
server_address = ('localhost', port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)


def response_teks():
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 7\r\n" \
		"\r\n" \
		"PROGJAR"
	return hasil

def response_no1(url):
	url = url.split('?dir=')
	if len(url) == 1:
		directory = os.curdir
	else:
		if url[1] == '':
			directory = os.curdir
		else:
			directory = url[1]
	
	files = os.listdir(directory)
	if directory == '.':
		current = ''
	else:
		current = directory
		current += '/'
	isi = ''

	for f in files:
		isi += '<p><a href="/1?dir='+current+f+'">'+f+'</a></p>'

	panjang = len(isi)

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(panjang, isi)

	return hasil

def response_no2():
	isi = "<form action=\"input\" method=\"post\" enctype=\"multipart/form-data\"><input type=\"file\" name=\"fileToUpload\" id=\"fileToUpload\"><input type=\"hidden\" name=\"countryxsz\" value=\"Norway\"><input type=\"submit\" value=\"Submit\"></form>"

	#isi = "<input type=\"text\" name=\"input\" placeholder=\"File\" />"

	panjang = len(isi)
	
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(panjang, isi)

	return hasil

def response_input_no2(req):
	#formData = cgi.FieldStorage()
	#print formData
	a,req=req.split("name=\"fileToUpload\"; ")
	#req,a,c=req.split(" -----------------------------")
	req=req.split("-----------------------------")	
	b=req[0].split("Content-Type: ")
	#get isi
	x=b[1].split("\n\r")
	print len(x)
	print "menghilangkan content type"
	print x
	#menciptakan judul
	now = datetime.datetime.now()
	now = str(now)
	now = now.replace(".","")
	now = now.replace(" ","")
	a=b[0].split("Content-Type: ")
	flnm=a[0].split("filename=\"")
	flnm=flnm=flnm[1].split("\"")
	flnm=now+flnm[0]
	print flnm
	file = open(flnm,"w")
	for xy in range(len(x)):
		if xy!=0:
			print "print"
			file.write(x[xy])
	file.close()
	#b[1]isi file
	msg="Sukses"
	panjang = len(msg)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}".format(panjang, msg)
	return hasil

def response_no6():

	mydir= ("<input type=\"text\" name=\"input\" id=\"folder\" placeholder=\"Masukkan Folder yang akan dihapus\" /> <input type=\"submit\" value=\"submit\"/> ")
	panjang = len(mydir)

	try:
		shutil.rmtree(mydir)
	except OSError, e:
		print ("Error: %s - %s." % (e.filename,e.strerror))

	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/html\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, mydir)
	return hasil



def response_gambar():
	filegambar = open('gambar.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_icon():
	filegambar = open('myicon.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_dokumen():
	filedokumen = open('dok.pdf','r').read()
	panjang = len(filedokumen)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: application/pdf\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filedokumen)
	return hasil

def response_redirect():
	hasil = "HTTP/1.1 301 Moved Permanently\r\n" \
		"Location: {}\r\n" \
		"\r\n"  . format('http://www.its.ac.id')
	return hasil




#fungsi melayani client
def layani_client(koneksi_client,alamat_client):
	try:
		print >>sys.stderr, 'ada koneksi dari ', alamat_client
		request_message = ''
		data = koneksi_client.recv(32)
		data = bytes.decode(data)
		print data
		request_message = request_message+data
		
		if("GET" in data):
			print "Method Get"
			while True:
				data = koneksi_client.recv(32)
				data = bytes.decode(data)
				print data
				request_message = request_message+data
				if (request_message[-4:]=="\r\n\r\n"):
					break
		elif("POST" in data):
			print "Method Post"
			while True:
				data = koneksi_client.recv(4096)
				request_message = request_message+data
				if ("countryxsz" in data):
					break
		
		print request_message
		baris = request_message.split("\r\n")
		baris_request = baris[0]
		print baris_request		
		a,url,c = baris_request.split(" ")
		#print url[:2]
		if (url=='/favicon.ico'):
			respon = response_icon()
		elif (url=='/doc'):
			respon = response_dokumen()
		elif (url=='/teks'):
			respon = response_teks()
		elif (url[:2]=='/1'):
			respon = response_no1(url)
		elif (url=='/2'):
			respon = response_no2()
		elif ("POST" in a and url=='/input'):
			#formData = cgi.FieldStorage()
			#name=formData.getvalue('name_field')
			#print "xxxx"
			#print name
			#print formData
			#print "xxxx"
			respon = response_input_no2(request_message)
		elif (url=='/6'):
			respon = response_no6()
		else:
			respon = response_gambar()

		koneksi_client.send(respon)
	finally:
		# Clean up the connection
		koneksi_client.close()


while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	koneksi_client, alamat_client = sock.accept()
	s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
	s.start()


