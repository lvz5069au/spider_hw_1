import re,requests,os,openpyxl

def crawing():
	
	wb=openpyxl.Workbook()
	ws=wb.active
	title=["排名","图片链接","电影名称","主演","上映日期","评分"]
	ws.append(title)

	headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.9',
		'Connection':'keep-alive',
		'Cookie':'uuid=1A6E888B4A4B29B16FBA1299108DBE9C620C75CB89EFC0262CC41D0A44F71066; _lxsdk_cuid=163f4de3438c8-0bc92fc3bb72af-335e4e76-1fa400-163f4de3438c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9C620C75CB89EFC0262CC41D0A44F71066; _csrf=da3b4197444d614b9b62454662df7dce4ed9e924e9ee3f47c0b60efcb15a991a; __mta=87922087.1528821593304.1528900443214.1528900445253.35; _lxsdk_s=163f97da1f7-bbf-464-35d%7C%7C37'	,
		'Host':'maoyan.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5478.400 QQBrowser/10.1.1550.400',
	}

	for i in range(0, 91, 10):
		page=int(i/10+1)
		try:
			url="http://maoyan.com/board/4?offset="+str(i)
			res=requests.get(url,headers=headers)

			print("正在爬取猫眼电影中榜单栏目中TOP100榜的所有电影信息（当前第"+str(page)+"页）...")	

			html=res.content.decode('utf-8')

		except Exception as err:
			print("爬取失败，原因是："+str(err))

		pic_pat='<img data-src="(.*?)" alt=".*?" class="board-img" />'
		name_pat='<p class="name"><a href=".*?" title="(.*?)" data-act="boarditem-click" data-val=".*?">'
		actors_pat='主演：(.*?)</p>'
		time_pat='<p class="releasetime">上映时间：(.*?)</p>'
		score_pat='<i class="integer">(.*?).</i><i class="fraction">(.*?)</i>'
		
		print("获取图片链接信息...")
		pic_list=re.compile(pic_pat,re.S).findall(html)
		print("获取电影名信息...")
		name_list=re.compile(name_pat,re.S).findall(html)
		print("获取主演信息...")
		actors_list=re.compile(actors_pat,re.S).findall(html)
		print("获取上映时间信息...")
		time_list=re.compile(time_pat,re.S).findall(html)
		print("获取分数信息...")
		score_list=re.compile(score_pat,re.S).findall(html)

		data_list=[]
		for j in range(10):
			j_list = no,pic,name,actors,time,score = str(i+j+1),pic_list[j],name_list[j],actors_list[j].strip(),time_list[j],score_list[j][0]+'.'+score_list[j][1]
			data_list.append(j_list)

		save_pic(data_list,i)
	
		save_file(data_list,wb,i)
		wb.save('./猫眼电影TOP100榜.xlsx')

	print("爬取完毕，所有信息及图片已成功保存")

def save_pic(list,page):
	'''保存图片'''
	target = ['|',':','*','?','/','\\','<','>','"']
	#创建文件夹
	if not os.path.exists('./猫眼电影TOP100榜图片'):
		os.makedirs('./猫眼电影TOP100榜图片')
	#循环取出图片地址保存
	for i in range(len(list)):
		try:
			res = requests.get(list[i][1])
			#判断文件名内是否有非法字符,并替换
			title = list[i][2]
			no=list[i][0]
			for j in target:
				if j in title:
					title = title.replace(j,'')
			with open('./猫眼电影TOP100榜图片'+"/"+no+' - '+title+".png","wb") as file:
				print("正在保存第"+str(page+i+1)+"张图片...")
				file.write(res.content)			

		except Exception as err:
			print("保存失败，原因是："+str(err))

def save_file(list,wb,page):
	'''保存信息表格'''
	try:
		ws = wb.active
		for i in range(len(list)):
			print('正在保存第'+str(page+i+1)+'条信息...')
			ws.append(list[i])

	except Exception as err:
			print("保存失败，原因是："+str(err))
	
if __name__ == '__main__':
	print("猫眼电影TOP100榜信息爬取")
	crawing()