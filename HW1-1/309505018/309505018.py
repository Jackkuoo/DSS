import sys
import requests
import re
import time
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from operator import itemgetter, attrgetter



def main():

	a=sys.argv[1]
	if a == "":
		print("InputError")
		exit (0)
	if a == 'crawl':
		crawl_all_year(url=None)
	elif a == 'push':
		b=int(sys.argv[2])
		c=int(sys.argv[3])
		push_list = []
		pop_list = []
		push(b,c)
	elif a == 'popular':
		b=int(sys.argv[2])
		c=int(sys.argv[3])
		Get_all_img(b,c)
	elif a == 'keyword':
		b=str(sys.argv[2])
		c=int(sys.argv[3])
		d=int(sys.argv[4])
		keyword(b,c,d)
	else:
		print("InputError")
		exit (0)

root = "https://www.ptt.cc/bbs/"
payload = {
	'from':'/bbs/Beauty/index2748.html',
	'yes': 'yes'
}
rs = requests.session()
res = rs.post("https://www.ptt.cc/ask/over18", data=payload)

push_list = []
pop_list = []


def crawl_all_year(url):
	#url = "https://www.ptt.cc/bbs/Beauty/index2749.html"
	f = open("all_articles.txt","w+")
	p = open("all_popular.txt","w+")
	t = 0
	for index in range(2747,3144):# 2748 3144
		url = "https://www.ptt.cc/bbs/Beauty/index" + str(index) + ".html"
		#print(index, "/ 3144")
		res = rs.get(url)
		soup = BeautifulSoup(res.text, "lxml")
		r_ent_div = soup.find_all('div', class_ = 'r-ent', limit = 20)
		for item in r_ent_div:
			title = item.find( class_ = 'title')
			if item.find('a'):
				s = item.find('a')
				title_text = s.string
				pop = item.find( class_ = 'nrec')
				popular = pop.string
				date = item.find('div', class_ = 'date')
				x1 = date.string.split('/')[0]
				x2 = date.string.split('/')[1]
				if s.get('href') == '/bbs/Beauty/M.1546272669.A.765.html':
					t = 1
				elif s.get('href') == '/bbs/Beauty/M.1546272980.A.AAA.html':
					t = 1
				elif s.get('href') == '/bbs/Beauty/M.1577801740.A.E41.html':
					t = 2

				if '[公告]' in title_text:
					continue
				else:
					if t == 1:
						f.writelines(x1+x2+","+title_text+","+'https://www.ptt.cc'+s.get('href')+"\n")
						#print(x1+x2+","+title_text+","+'https://www.ptt.cc'+s.get('href')+"\n")
						if popular == "爆":
							p.writelines(x1+x2+","+title_text+","+'https://www.ptt.cc'+s.get('href')+"\n")
					elif t == 2:
						f.writelines(x1+x2+","+title_text+","+'https://www.ptt.cc'+s.get('href')+"\n")
						#print(x1+x2+","+title_text+","+'https://www.ptt.cc'+s.get('href')+"\n")
						if popular == "爆":
							p.writelines(x1+x2+","+title_text+","+'https://www.ptt.cc'+s.get('href')+"\n")
						t = 0
	
	f.close()
	p.close()



def push(start,end):
	all=[]
	filename = "push"+"["+str(start)+"-"+str(end)+"]"+".txt"
	r = open("all_articles.txt", 'r')
	t = 0
	totalupvote = 0
	totaldownvote = 0
	for line in r:
		line = line.strip('\n')
		date = int(line.split(",")[0])
		if date >= end:
			t=2
		elif date >= start:
			t=1

		if t == 1:
			na = line.split(",")[1]
			ul = line.split(",")[-1]
			#print("date:",date,"name:",na,"url:",ul)
			ans = push_down_vote(url=ul)
			totalupvote +=ans[0]
			totaldownvote +=ans[1]
		elif t == 2:
			if date == end:
				na = line.split(",")[1]
				ul = line.split(",")[-1]
				#print("date:",date,"name:",na,"url:",ul)
				ans = push_down_vote(url=ul)
				totalupvote +=ans[0]
				totaldownvote +=ans[1]
			elif date != end:
				break

	#push_list.sort(key=takeSecond, reverse=True)
	#pop_list.sort(key=takeSecond, reverse=True)
	push_list.sort(key=lambda r: r[0])
	push_list.sort(key=lambda r: r[1], reverse=True) 
	pop_list.sort(key=lambda r: r[0])
	pop_list.sort(key=lambda r: r[1], reverse=True) 
	#print("push: ",totalupvote,"pop: ",totaldownvote)
	pu = open(filename, 'w+')
	pu.writelines("all like: "+str(totalupvote)+"\n")
	pu.writelines("all boo: "+str(totaldownvote)+"\n")
	for i in range(0,10):
		pu.writelines("like #"+str(i+1)+": "+push_list[i][0]+" "+str(push_list[i][1])+"\n")
			#print(push_list[i])

	for i in range(0,10):
		pu.writelines("boo #"+str(i+1)+": "+pop_list[i][0]+" "+str(pop_list[i][1])+"\n")

	r.close()
	pu.close()

def takeSecond(elem):
    return elem[1]

def push_down_vote(url):
    
	res = rs.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	try:
		article = {}
		upvote = 0
		downvote = 0
		novote = 0

		for response_struct in soup.select(".push"):
			if "warning-box" not in response_struct['class']:
				if response_struct.select(".push-tag")[0].contents[0][0] == u"推":
					user = response_struct.select(".push-userid")[0].contents[0]
					t = 0
					#print("user: ",user)
					for i in range(len(push_list)):
						if push_list[i][0] == user:
							push_list[i][1] += 1
							upvote += 1
							t=1;
							break;
					if t == 0:
						pp = [[],[]]
						pp[0] = user
						pp[1] = int(1)
						#print(pp)
						push_list.append(pp)
						upvote += 1

				elif response_struct.select(".push-tag")[0].contents[0][0] == u"噓":
					user = response_struct.select(".push-userid")[0].contents[0]
					t = 0
					#print("user: ",user)
					for i in range(len(pop_list)):
						if pop_list[i][0] == user:
							pop_list[i][1] += 1
							downvote += 1
							t=1;
							break;
					if t == 0:
						pp = [[],[]]
						pp[0] = user
						pp[1] = int(1)
						#print(pp)
						pop_list.append(pp)
						downvote += 1
				else:
					novote += 1

	except Exception as e:
		print(e)
		print(u"在分析 %s 時出現錯誤" % url)

	ans = []
	ans.append(upvote)
	ans.append(downvote)
	#print(ans)
	return ans

def Get_all_img(start,end):
	pre = open("all_popular.txt", 'r')
	count = 0
	p = 0
	for line in pre:
		line = line.strip('\n')
		date = int(line.split(",")[0])
		if date >= end:
			p=2
		elif date >= start:
			p=1

		#print("date:",date,"p:",p,"start:",start,"end:",end)
		if p == 1:
			count+=1
		elif p == 2:
			if date == end:
				count+=1
			elif date != end:
				p = 0
				break
	pre.close()
	r = open("all_popular.txt", 'r')
	filename = "popular"+"["+str(start)+"-"+str(end)+"]"+".txt"
	allimg = open(filename, 'w+')
	allimg.writelines("number of popular articles: "+str(count)+"\n")
	t = 0
	for line in r:
		line = line.strip('\n')
		date = int(line.split(",")[0])
		if date >= end:
			t=2
		elif date >= start:
			t=1

		if t == 1:
			url = line.split(",")[-1]
			img_per_page(url=url,allimg=allimg)
		elif t == 2:
			if date == end:
				url = line.split(",")[-1]
				img_per_page(url=url,allimg=allimg)
			elif date != end:
				t = 0
				break

	allimg.close()
	r.close()

def img_per_page(url,allimg):

	res = rs.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	imgs = soup.find_all('a')
	for img in imgs:
		if '.jpg' in img['href']:
			#print(img['href'])
			allimg.writelines(img['href']+"\n")
		elif '.jpeg' in img['href']:
			#print(img['href'])
			allimg.writelines(img['href']+"\n")
		elif '.png' in img['href']:
			#print(img['href'])
			allimg.writelines(img['href']+"\n")
		elif '.gif' in img['href']:
			#print(img['href'])
			allimg.writelines(img['href']+"\n")

def keyword(keyword,start,end):
	r = open("all_articles.txt", 'r')
	filename = "keyword("+keyword+")["+str(start)+"-"+str(end)+"]"+".txt"
	key = open(filename, 'w+')
	t = 0
	for line in r:
		line = line.strip('\n')
		date = int(line.split(",")[0])
		if date >= end:
			t=2
		elif date >= start:
			t=1

		if t == 1:
			url = line.split(",")[-1]
			if find_keyword(url=url,keyword=keyword) == "yes":
				#print(line)
				img_per_page(url=url,allimg=key)
		elif t == 2:
			if date == end:
				url = line.split(",")[-1]
				if find_keyword(url=url,keyword=keyword) == "yes":
					#print(line)
					img_per_page(url=url,allimg=key)
			elif date != end:
				t = 0
				break

	key.close()
	r.close()

def find_keyword(url,keyword):
	res = rs.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	if soup.find(id="main-content"):
		content = soup.find(id="main-content").text
		target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'
		content = content.split(target_content)
		#print(type(content[0]))
		if keyword in content[0]:
			return "yes"
		else:
			return "no"


if __name__ == '__main__':
	main()