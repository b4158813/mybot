import requests
from lxml import etree
from nonebot import on_command, CommandSession



# 爬取上理校务新闻
def get_school_affairs():
	url = 'http://www.usst.edu.cn/qb/list.htm'
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
	}
	r = requests.get(url,timeout=30,headers=headers)

	cnt = 0
	while r.status_code!=200:
		cnt += 1
		if cnt >= 3:
			return "爬取失败！"
		r = requests.get(url,timeout=30,headers=headers)

	r.encoding = 'utf-8' # 编码成utf-8才能正常读取中文
	# r.encoding = 'utf-8'
	# print(r.encoding)
	html = etree.HTML(r.text)
	news_url = html.xpath("//div[@id='wp_news_w9']/li//a/@href")
	news_content = html.xpath("//div[@id='wp_news_w9']/li//a/text()")
	news_date = html.xpath("//div[@id='wp_news_w9']//span[@class='column-news-date news-date-hide']/text()")
	# print(news_url)
	# print(news_date)
	# print(news_content)
	res = []
	for i in range(len(news_date)):
		# 内容，日期，链接
		if news_url[i][0]=='/':
			news_url[i] = "http://jwc.usst.edu.cn"+news_url[i]
		res.append([news_content[i],news_date[i],news_url[i]])
	# print(res)
	return res


# 爬取教务处新闻
def get_jwcnews():
	url = 'http://jwc.usst.edu.cn/'
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
	}
	r = requests.get(url,timeout=30,headers=headers)

	cnt = 0
	while r.status_code!=200:
		cnt += 1
		if cnt >= 3:
			return "爬取失败！"
		r = requests.get(url,timeout=30,headers=headers)

	r.encoding = 'utf-8' # 编码成utf-8才能正常读取中文
	html = etree.HTML(r.text)
	news_url = html.xpath("//td[@align='left']/a/@href")[:15]
	news_content = html.xpath("//td[@align='left']/a/@title")[:15]
	news_date = html.xpath("//td[@align='left']/div/text()")
	# news_img = html.xpath("//td[@align='left']/div/img/@src")
	# print(news_img)
	# news_date = [ele[6:8]+"-"+ele[8:10] for ele in news_url]
	# print(news_url)
	# print(news_date)
	# print(len(news_date))
	# print(len(news_url))
	# print(news_content)
	# print(len(news_content))
	res = []
	for i in range(len(news_date)):
		# 内容，日期，链接
		if news_url[i][0]=='/':
			news_url[i] = "http://jwc.usst.edu.cn"+news_url[i]
		res.append([news_content[i],news_date[i],news_url[i]])
	
	# 按照日期降序排序，然后获取前八条信息
	res = sorted(res, key=lambda x: int(x[1][0]+x[1][1]+x[1][3]+x[1][4]), reverse=True)
	res = res[:8]
	return res



# 将爬取的字符串list转换成一整个string
def get_text(msg, num):
	res = ""
	for i in range(num):
		res += msg[i][1]+"\n"+msg[i][0]+"\n链接: "+msg[i][2]+"\r\n\r\n"

	return res


@on_command('校务新闻',aliases=('usst新闻','上理新闻','USST新闻','学校新闻','学校最新消息'))
async def school_affairs(session: CommandSession):
	msg = get_school_affairs()
	text = msg
	if text!="爬取失败！":
		text = "USST最新新闻（获取前5条）：\r\n"
		text += get_text(msg,5)
	message_type = session.ctx['message_type']
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


@on_command('教务处',aliases=('教务处新闻','上理教务处','教务处消息','jwc'))
async def jwc_affairs(session: CommandSession):
	msg = get_jwcnews()
	text = msg
	if text!="爬取失败！":
		text = "上理教务处最新消息（获取前8条）：\r\n"
		text += get_text(msg,8)
	message_type = session.ctx['message_type']
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


if __name__ == '__main__':

	# msg = get_school_affairs()
	# print(get_text(msg,5))

	msg = get_jwcnews()
	print(get_text(msg,8))