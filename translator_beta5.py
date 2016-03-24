#coding:utf-8
import urllib.request
import urllib.parse
from urllib.error import URLError
import json
# import iplist
# import random
from tkinter import *
import os

#TODO:1. add a username √; 2. add a text version √ ;3. add a local dictionary √; 4. add the translating history; 5. if words in history, return a joke； 6. add a huge dict

#判断文件是否存在
user = ''
file = 'username.txt'
if os.path.exists(file):
	with open('username.txt', 'r') as r:
		user = r.read()	#若文件存在则读取用户名
		r.close()
else:
	with open('username.txt', 'w') as w:
		w.close()
	user = '' # 不存在则令用户名为空

with open('dictionary.txt','r', encoding='utf8') as d:
	lines = d.read().split('\n')
	d.close()
dictionary = {}
for x in range(0, len(lines)):
	a = lines[x].split('   ')[0]
	b = lines[x].split('   ')[1]
	if a in dictionary.keys():
		dictionary[a] = dictionary[a] + ' ' + b
	else:
		dictionary[a] = b
		
		
p = 0
def local(word):
	if word in dictionary.keys():
		return dictionary[word]
	else:
		return '本地词典没有查询结果！'

def getname(event=None):
	name.destroy()
	global p, user
	user = name1.get() #写入用户名， 后期加入用户名列表
	with open('username.txt', 'w') as n:
		n.write(user)
		n.close()
	if user != '':
		p = 1

def quitwords():
	root.destroy()
	global p
	p = 2

def quitparas():
	para.destroy()
	global p
	p = 2
				
def parav():	#通过改变P值跳转到段落
	root.destroy()
	global p
	p = 1
	
def return2words():
	para.destroy()
	global p
	p = 0

def words(event=None):	#单词翻译
	content = text1.get()
	if content == '':
		content = 'Please input some contents which are needed to translated'
	req = translate(content)
	
	try:	#判断网络连通性
		response = urllib.request.urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			# text2.set('%s, 没网啦！\(^o^)/~' % user)
			text2.set(local(content))
			
	else:
		html = response.read().decode('utf8')

		target = json.loads(html)
		target = target['translateResult'][0][0]['tgt']

		text2.set(target)
	
def paras():	#段落翻译
	content = text3.get(1.0, END)
	text4.delete(0.0, END)
	if content == '':
		content = "Please input something!"
	req = translate(content)
	try:	#判断网络连通性
		response = urllib.request.urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			text4.insert(INSERT, '%s, 没网啦！\(^o^)/~' % user)
	else:
		html = response.read().decode('utf8')

		target = json.loads(html)
		# target = target['translateResult'][0][0]['tgt']
		cloum=1
		if target.__contains__('translateResult'):
			for i in target['translateResult']:
				for j in i:
					text4.insert(INSERT,j['tgt'] + '\n')
					cloum+=1
		else:
			text4.insert(INSERT, '输入不能为空！')
		# text4.insert(INSERT, target)
	
def translate(content): #翻译entry1的内容
	content = content
	# iplist = iplist.get_proxy() #导入代理

	url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=http://www.baidu.com/s'	

	# proxy_support = urllib.request.ProxyHandler({'http':random.choice(iplist)})
	# opener = urllib.request.build_opener(proxy_support)
	# opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')]
	# urllib.request.install_opener(opener)

	head = {}
	head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

	data = {}
	data['type'] = 'AUTO'
	data['i'] = content
	data['doctype'] = 'json'
	data['xmlVersion'] = '1.8'
	data['keyfrom'] = 'fanyi.web'
	data['ue'] = 'UTF-8'
	data['action'] = 'FY_BY_CLICKBUTTON'
	data['typoResult'] = 'true'
	data = urllib.parse.urlencode(data).encode('utf8')
	
	req = urllib.request.Request(url, data)
	
	return req

if user == '':
	name = Tk()
	name.title('请输入你的名字~')

	name1 = StringVar()

	entry = Entry(name, textvariable=name1, width=40)	
	entry.pack()

	Button(name, text='好了~', command=getname).pack(side=LEFT)
	Button(name, text='暂时不想使用~', command=name.destroy).pack()

	entry.bind('<Return>', getname)

	name.mainloop()
	
while p in range(0,3):		

	if user != '':	#如果用户名不为空，则开始进行翻译
		
		root = Tk()	

		root.title('单词翻译 for %s  by Mos'  % user)

		Label(root, text='将单词', justify=LEFT).grid(row=0, column=0)
		Label(root, text='翻译为', justify=LEFT).grid(row=1, column=0)

		text1 = StringVar()
		text2 = StringVar()

		entry1 = Entry(root, textvariable=text1, width=40)
		entry2 = Entry(root, textvariable=text2, state='readonly', width=40).grid(row=1, column=1)

		entry1.grid(row=0, column=1)

		text2.set('欢迎%s使用O(∩_∩)O~~'  % user)

		entry1.bind('<Key-Return>', words)


		Button(root, text='翻译', command=words, justify=RIGHT).grid(row=0, column=2)
		Button(root, text='段落', command=parav, justify=RIGHT).grid(row=0, rowspan=2, column=3)
		Button(root, text='退出', command=quitwords, fg='red', justify=RIGHT).grid(row=1, column=2)
		root.mainloop()

	if p == 1:
		para = Tk()
		para.title('段落翻译 for %s by Mos'  % user)

		text3=Text(para,width=80,height=10,padx=10,pady=10,fg='black',font=('Comic Sans MS', 10))
		text4=Text(para,width=80,height=10,padx=10,pady=10,fg='blue',font=('Comic Sans MS', 10))

		text3.pack()
		framep = Frame(para)
		Button(framep, text='开始翻译', command=paras).pack(side=LEFT)
		Button(framep, text='返回单词', command=return2words).pack(side=LEFT)
		Button(framep, text='退出程序', command=quitparas).pack(side=RIGHT)
		framep.pack()
		text4.pack()

		
		para.mainloop()
	
	if p == 2 or user == '': #如果不判断用户名为空的情况，则会陷入死循环
		break
