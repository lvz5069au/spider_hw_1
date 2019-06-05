import requests,re,openpyxl,os

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
	}

def crawing(page):
	'''爬取指定页数的信息'''
	try:
		print('正在爬取第'+page+'页信息...')

		url = 'http://bj.58.com/dashanzi/chuzu/pn'+str(page)+'/?ClickID=1'
		res = requests.get(url,headers=headers)
		html = res.content.decode('utf-8')

	except Exception as err:
		print("爬取失败，原因是："+str(err))

	#定义查找标题、图片、户型、价格的正则表达式
	title_pat='<h2>.*?<a.*?tongji_label="listclick".*?>(.*?)                    </a>'
	pic_pat = 'lazy_src="(.*?)"'
	room_pat = '<p class="room">(.*?)                    &nbsp;&nbsp;&nbsp;&nbsp;(.*?)</p>'
	# room_pat = '<p class="room">(.*?).*?</p>'
	room_pat_str = '<p class="room strongbox">(.*?)                    &nbsp;&nbsp;&nbsp;&nbsp;(.*?)</p>'
	# price_pat = '<div class="money">.*?<b>(.*?)</b>'
	price_pat = '<div class="money">.*?<b class="strongbox">(.*?)</b>'

	print("获取标题信息...")
	title_list=re.compile(title_pat,re.S).findall(html)

	print("获取图片信息...")
	pic_list=re.compile(pic_pat,re.S).findall(html)

	print("获取户型信息...")
	room_list_1=re.compile(room_pat,re.S).findall(html)
	room_str_list =  re.compile(room_pat_str,re.S).findall(html)
	room_list  = room_list_1 + room_str_list

	print("获取价格信息...")
	price_list=re.compile(price_pat,re.S).findall(html)


	data_list = []
	for i in range(len(title_list)):
		i_list = title,pic,room,price = title_list[i].strip(),"http:"+pic_list[i],room_list[i][0] +' - ' + room_list[i][1],price_list[i]+'元/月'
		data_list.append(i_list)

	print("开始保存图片...")
	save_pic(data_list,page)
	print("所有图片已保存在当前目录下的58同城租房信息图片文件夹内")

	print("开始保存信息表格文件...")
	save_file(data_list,page)
	print("当前页租房信息已保存在当前目录下的表格文件内")

	print("爬取完毕，所有信息及图片已成功保存")

def save_pic(data_list,page):
	'''保存图片'''
	target = ['|',':','*','?','/','\\','<','>','"']
	#创建文件夹
	if not os.path.exists('./58同城租房信息图片 - 第'+page+'页'):
		os.makedirs('./58同城租房信息图片 - 第'+page+'页')
	#循环取出图片地址保存
	for i in range(len(data_list)):
		try:
			res = requests.get(data_list[i][1])
			#判断文件名内是否有非法字符,并替换
			title = data_list[i][0]
			for j in target:
				if j in title:
					title = title.replace(j,'')
			with open('./58同城租房信息图片 - 第'+page+'页'+"/"+title+".png","wb") as file:
				print("正在保存第"+str(i+1)+"张图片...")
				file.write(res.content)			

		except Exception as err:
			print("保存失败，原因是："+str(err))

def save_file(data_list,page):
	'''保存信息表格'''
	try:
		wb = openpyxl.Workbook()
		ws = wb.active
		title = ['标题','图片链接','户型','价格']
		ws.append(title)
		for i in range(len(data_list)):
			print('正在保存第'+str(i+1)+'条信息...')
			ws.append(data_list[i])
		wb.save('./58同城房屋出租信息 - 第'+page+'页.xlsx')

	except Exception as err:
			print("保存失败，原因是："+str(err))

if __name__ == '__main__':

	while True:
		page=input("请输入要爬取的信息页数(1~70)，输入q退出：")
		if page=='q':
			break
		else:
			crawing(page)
