#coding:utf-8
'''
本工具调用了有道文本翻译的接口，劫持了输入和输出端，并添加了一些人性化小工具
'''
__author__ = {
				'name':'Mos', 
				'mail':'acwzy@qq.com',
				'version':'beta7',
				'date':'2016-03-29'}



import urllib.request
import urllib.parse
from urllib.error import URLError
import json
# import iplist
# import random
from tkinter import *
import os
import dictionary
#TODO:1. add a username √; 2. add a text version √ ;3. add a local dictionary √; 4. add the translating history; 5. if words in history, return a joke； 6. add a huge dict

#判断文件是否存在
user = ''
userlang = ''
version1 = ['本地词典没有查询结果！', 'Please input some contents which are needed to translated', '没网啦！', '输入不能为空！', '请输入你的名字~', '好了~', '暂时不想使用~', '单词翻译', '将单词', '翻译为', '欢迎使用', '翻译', '段落', '退出', '段落翻译', '开始翻译', '返回单词', '退出程序', '好了！']
version2 = ['There\'s no local translation!', '请输入需要翻译的内容！', 'Please connect the Internet!', 'Please input something!', 'What\'s your name?', 'OK~', 'Not now', 'Words Translator', 'Translate', 'To', 'Welcome', 'Go!', 'More', 'Exit', 'Text Translator', 'Let\'s Begin', 'Back to Words', 'Exit', 'OK~']
version = []
file = 'user.txt'
read = ''

if os.path.exists(file):
	with open(file, 'r', encoding='gbk') as r:
		read = r.read().split(' ') #user文件含有两个属性，分别为用户名和用户使用的语言
		if read != ['']:
			user = read[0] 
			userlang = read[1]
		r.close()
else:
	with open(file, 'w') as w:
		w.close()
	user = '' # 不存在则令用户名为空

# with open('dictionary.txt','r', encoding='utf8') as d:
	# lines = d.read().split('\n')
	# d.close()
dict0 = {}
# for x in range(0, len(lines)):
	# a = lines[x].split('   ')[0]
	# b = lines[x].split('   ')[1]
	# if a in dict0.keys():
		# dict0[a] = dict0[a] + ' ' + b
	# else:
		# dict0[a] = b
dict1 = dictionary.dictionary
for i in dict1:
	if i[0] in dict0.keys():
		dict0[i[0]] = dict0[i[0]] + ' [计]' + i[1]
	else:
		dict0[i[0]] = i[1]
		
		
p = 0
def langseletion():	#语言选择窗口
	lang.destroy()
	global version, userlang
	if langs.get() == 1:
		version = version1
		userlang = '中文'
		# Button(lang, text='好了！', command=lang.destroy).pack()
	if langs.get() == 2:
		version = version2
		userlang = 'English'
		# Button(lang, text='OK~', command=lang.destroy).pack()

def local(word):	#本地查询功能
	if word in dict0.keys():
		return dict0[word]
	else:
		return '%s' % version[0]

def getname(event=None):
	name.destroy()
	global p, user
	user = name1.get() #写入用户名， 后期加入用户名列表
	with open(file, 'w') as n:
		n.write('%s %s'%(user,userlang))
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
		content = '%s' % version[1]
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
		target = ''.join(target['smartResult']['entries'])

		text2.set(target)
	
def paras():	#段落翻译
	content = text3.get(1.0, END)
	text4.delete(0.0, END)
	if content == '':
		content = '%s' % version[3]
	req = translate(content)
	try:	#判断网络连通性
		response = urllib.request.urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			text4.insert(INSERT, '%s, %s\(^o^)/~' % (user, version[2]))
	else:
		html = response.read().decode('utf8')

		target = json.loads(html)
		# target = target['translateResult'][0][0]['tgt']
		if target.__contains__('translateResult'):
			for i in target['translateResult']:
				for j in i:
					text4.insert(INSERT,j['tgt'] + '\n')
		else:
			text4.insert(INSERT, '%s' % version[3])
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



if 	userlang == '':
	lang = Tk()
	lang.title('Hi~')
	langs = IntVar()
	Radiobutton(lang, text='中文', variable=langs, value=1).grid(row=0, column=0)
	Radiobutton(lang, text='English', variable=langs, value=2).grid(row=0, column=1)
	
	Button(lang, text='OK', command=langseletion).grid(row=0, column=2)
	lang.mainloop()
	
elif userlang == '中文':
	version = version1

elif userlang == 'English':
	version = version2

if user == '' and userlang != '':
	name = Tk()
	name.title('%s' % version[4])

	name1 = StringVar()

	entry = Entry(name, textvariable=name1, width=40)	
	entry.pack()

	Button(name, text='%s' % version[5], command=getname).pack(side=LEFT)
	Button(name, text='%s' % version[6], command=name.destroy).pack()

	entry.bind('<Return>', getname)

	name.mainloop()
	
while p in range(0,3) and userlang != '':		

	if user != '':	#如果用户名不为空，则开始进行翻译
		
		root = Tk()	

		root.title('%s for %s  by Mos'  % (version[7],user))

		Label(root, text='%s' % version[8], justify=LEFT).grid(row=0, column=0)
		Label(root, text='%s' % version[9], justify=LEFT).grid(row=1, column=0)

		text1 = StringVar()
		text2 = StringVar()

		entry1 = Entry(root, textvariable=text1, width=40)
		entry2 = Entry(root, textvariable=text2, state='readonly', width=40).grid(row=1, column=1)

		entry1.grid(row=0, column=1)

		text2.set('%s, %sO(∩_∩)O~~'  % (user,version[10]))

		entry1.bind('<Key-Return>', words)


		Button(root, text='%s'%version[11], command=words, justify=RIGHT).grid(row=0, column=2)
		Button(root, text='%s'%version[12], command=parav, justify=RIGHT).grid(row=0, rowspan=2, column=3)
		Button(root, text='%s'%version[13], command=quitwords, fg='red', justify=RIGHT).grid(row=1, column=2)
		root.mainloop()

	if p == 1:
		para = Tk()
		para.title('%s for %s by Mos'  % (version[14], user))

		text3=Text(para,width=80,height=10,padx=10,pady=10,fg='black',font=('Comic Sans MS', 10))
		text4=Text(para,width=80,height=10,padx=10,pady=10,fg='blue',font=('Comic Sans MS', 10))

		text3.pack()
		framep = Frame(para)
		Button(framep, text='%s'%version[15], command=paras).pack(side=LEFT)
		Button(framep, text='%s'%version[16], command=return2words).pack(side=LEFT)
		Button(framep, text='%s'%version[17], command=quitparas).pack(side=RIGHT)
		framep.pack()
		text4.pack()

		
		para.mainloop()
	
	if p == 2 or user == '': #如果不判断用户名为空的情况，则会陷入死循环
		break
