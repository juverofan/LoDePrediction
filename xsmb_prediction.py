import numpy as np
import pandas as pd
import numpy as np
import time
import requests
from bs4 import BeautifulSoup as BS
import progressbar
from time import sleep
import random
import os
import json
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("LoDeV1 by topVL.net")
from colored import fg

red = fg('red_1')
bloodred = fg('dark_red_2')
purple = fg('purple_1a')
white = fg('white')
green = fg('light_green')
blue = fg('blue')
grey = fg('grey_54')
yellow = fg('yellow')

print(yellow + "\t\t\tCÔNG CỤ DỰ ĐOÁN XSMB - HOÀN TOÀN MIỄN PHÍ NHÁ\n \t\t\t\tBẠN NÀO THƯƠNG THÌ ỦNG HỘ")
print("\t\t\tWebsite: https://topvl.net")
print(yellow+"\t\t\t\tDonate us\n\t\tBTC: "+green+"1Dbu7Hwrmd2iT6xSxKf4rYrYiufukQLAjt")
print(yellow+"\t\tETH: "+green+"0xb6f5ed1e3b05f8837c444c22839e47c468dab818")
print(yellow+"\t\tDOGE: "+green+"DP9KxGRiA4gYGnn8FdF6mBva6NxtQmPhEC")
print(yellow+"\t\tPaypal: "+green+"https://paypal.me/topvl")
print(white)
#z = input('Có cần tổng hợp dữ liệu không? '+green+'1 - có, 2 - không\n'+green+'\tKhông cần tổng hợp lại nếu vừa thực hiện dự đoán\n')
kt = input(white + "Thích lô hay đề? "+green+" 1 - đề; 2 - lô\n")
path = os.getcwd()
#kt = "1"
z = "1"
if z == "1":
	print(white + "Quá trình tổng hợp dữ liệu ...")
	rolldate = []
	results = []
	maxdate = ""
	maxid = ""
	lastresult = []
	baseurl = "https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/main/results/xsmb_1_year.csv"
	url = baseurl
	i = 1
	FILE_TO_SAVE_AS = path+"\\xsmb.txt" # the name you want to save file as
	resp = requests.get(url) # making requests to server
	with open(FILE_TO_SAVE_AS, "wb") as f:
		f.write(resp.content) # writing content to file

	fo = open(FILE_TO_SAVE_AS)
	i = 1
	lines = fo.readlines()
	bar = progressbar.ProgressBar(maxval=len(lines), \
		widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	lx = 0 
	#results = []
	for l in lines:
		if lx > 0: 
			rss = l.split(",")
			maxdate = rss[0]
			lastresult = []
			for x in rss:
				if x != maxdate:
					lastresult.append(str(x.strip()))
			rolldate.append(maxdate)
			results.append(lastresult)
			bar.update(i+1)
		lx += 1
	fo.close()
	bar.finish()
	#print(str(len(rolldate)))
	#print(str(len(results)))
	print(white + "Kỳ quay cuối cùng ngày: "+maxdate+" - kết quả: "+str(lastresult))
	print(white + "Kết thúc tổng hợp dữ liệu\nBắt đầu quá trình dự đoán...")

	ws = open(path+"\\xsmb_db.txt","w+")
	if kt == "1":
		i = 0 
		ws.write("special\n")
		while i < len(rolldate):
			if len(results[i])==27:
				vdata = results[i][0]
				vdata = vdata.strip()+"\n"
				ws.write(vdata)
			i += 1
		ws.close()
	else:
		i = 0 
		ws.write("special\tprize1\tprize2_1\tprize2_2\tprize3_1\tprize3_2\tprize3_3\tprize3_4\tprize3_5\tprize3_6\tprize4_1\tprize4_2\tprize4_3\tprize4_4\tprize5_1\tprize5_2\tprize5_3\tprize5_4\tprize5_5\tprize5_6\tprize6_1\tprize6_2\tprize6_3\tprize7_1\tprize7_2\tprize7_3\tprize7_4\n")
		while i < len(rolldate):
			if len(results[i])==27:
				vdata = ""
				for rs in results[i]:
					vdata += "\t"+str(int(rs.strip()) % 100)
				vdata = vdata.strip()+"\n"
				ws.write(vdata)
			i += 1
		ws.close()


def getTop(plist):
	rt = []
	grt = 0
	#print(len(plist))
	while grt < 3:
		start = 0
		tmp = 0
		x = 0
		while x < len(plist):
			if plist[x] >= start:
				if x not in rt:
					start = plist[x]
					tmp = x
			x += 1
		#print(tmp)
		rt.append(tmp)
		grt += 1
	return rt

stop = 0

while stop == 0:

	data = np.loadtxt(path+"\\xsmb_db.txt",delimiter="\t",dtype="int",skiprows=1)
	#print(data)
	X = []
	#nếu là đề, chỉ lấy danh sách kết quả đề
	if kt == "1":
		rs1 = data.tolist()
		rs = []
		for rx in rs1:
			rs.append(int(rx)%100)
	else:
		#nếu là lô lấy tất tần tật
		X = data[1:, :] 
		str(X)
		rs = [i for z in X.tolist() for i in z]
	
	#print(rs)

	#tạo ds kết quả
	results = []
	#add sẵn mỗi số 1 lượt
	z1 = 0 
	while z1 < 100:
		results.append(z1)
		z1 += 1

	#add kết quả thực vào danh sách kết quả, nếu là đề mỗi kết quả bổ sung 10 lượt, và 1 lượt cho 2 vị trí liền kề, nếu là lô bổ sung mỗi kết quả 4 lượt
	#for r in rs:
	idx = 0
	h = 1
	lenrs = len(rs)-1
	while idx < len(rs):
		if kt == "1":
			if idx == (-1 + 7*h):
				results.append(int(rs[lenrs-idx])-1)
				results.append(int(rs[lenrs-idx])+1)
				ii = 0
				while ii < 25:
					results.append(int(rs[lenrs-idx]))
					ii += 1
				h += 1
			else:
				results.append(int(rs[lenrs-idx])-1)
				results.append(int(rs[lenrs-idx])+1)
				ii = 0
				while ii < 10:
					results.append(int(rs[lenrs-idx]))
					ii += 1
				#h += 1
		else:
			if idx >= (-1 + 7*h)*27 and idx < 7*h*27 + 1:
				ii = 0
				while ii < 7:
					results.append(int(rs[lenrs-idx]))
					ii += 1
				if idx == 7*h*27:
					h += 1
			else:
				ii = 0
				while ii < 3:
					results.append(int(rs[lenrs-idx]))
					ii += 1
		idx = idx + 1

	#chạy lấy danh sách ngẫu nhiên
	runiter = len(results)*10
	zz = 0
	bar = progressbar.ProgressBar(maxval=runiter, \
				widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	countTot = [] #danh sách đếm
	#results = []
	randList = [] #danh sách random số
	randCount = [] #danh sách random số và số lượt lấy ngẫu nhiên
	#print(len(results))
	while zz < runiter:
			
		rand = random.randint(0,len(results)-1) #lấy ngẫu nhiên 1 số thuộc vị trí ds kết quả
		if rand not in randList:
			randList.append(rand) #add vào ds random số nếu chưa có
			randCount.append([rand,1]) #add vào danh sách số và số lượt đếm bằng 1
		else:
			idx = randList.index(rand)
			randCount[idx][1] = randCount[idx][1]+1 # cộng thêm 1 lượt vào randCount
		
		#	print("\nKết quả dự đoán lần "+str(zz-27+1)+": ",green+str([z[0] for z in randCount]),yellow+str([z[1] for z in randCount])+white)
		bar.update(zz+1)
		zz += 1
	bar.finish()
	tmp = 0
	for z in randCount:
		tmp = int(z[1])
		countTot.append(tmp)
	getRS = getTop(countTot)
	
	#print(getRS)
	if kt == "1":
		print(green+"\nKẾT QUẢ DỰ ĐOÁN ĐỀ NGÀY HÔM NAY\n")
	else:
		print(green+"\nKẾT QUẢ DỰ ĐOÁN LÔ NGÀY HÔM NAY\n")
	for rs in getRS:
		#print(countTot[rs])
		print("\n"+white+"Kết quả dự đoán lần "+str(getRS.index(rs)+1)+": "+green+str(results[rs])+" - Xác suất: "+ yellow+str(round((countTot[rs])*1000/len(results),2))+"%"+white)

	repeat = input('\nBạn có muốn dự đoán lại không? '+green+'Y/N - có/không\n'+white)
	if repeat.strip().upper() != "Y":
		stop = 1

import readchar
print("Press Any Key To Exit")
k = readchar.readchar()
