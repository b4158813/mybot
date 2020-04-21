import requests
from lxml import etree
from nonebot import on_command, CommandSession

BILI_RANK = {
	"全站":0,
	"动画":1,
	"国创":168,
	"音乐":3,
	"舞蹈":129,
	"游戏":4,
	"科技":36,
	"数码":188,
	"生活":160,
	"鬼畜":119,
	"时尚":155,
	"娱乐":5,
	"影视":181
}

# 爬取b站视频
def get_bv(key_words):
	url = 'https://search.bilibili.com/all?keyword=%s'%(key_words)
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

	r.encoding = 'utf-8'
	html = etree.HTML(r.text)
	html_url = html.xpath("//li[@class='video-item matrix']/a/@href")
	html_url = [i[2:] for i in html_url]
	# print(html_url)
	html_content = html.xpath("//li[@class='video-item matrix']/a/@title")
	# print(html_content)
	html_upname = html.xpath("//li[@class='video-item matrix']//a[@class='up-name']/text()")
	html_playt = html.xpath("//span[@title='观看']//text()")
	html_playt = [i.strip() for i in html_playt]
	html_uptime = html.xpath("//span[@title='上传时间']//text()")
	html_uptime = [i.strip() for i in html_uptime]
	# print(html_uptime)
	# print(html_playt)
	# print(len(html_playt),len(html_url),len(html_content))
	# print(html_upname)

	res = []
	for i in range(len(html_content)):
		# 内容，链接，播放量，上传时间，up主
		res.append([html_content[i], html_url[i], html_playt[i], html_uptime[i], html_upname[i]])

	return res


# 爬取日榜信息
def get_rank(key_words):
	url = 'https://www.bilibili.com/ranking/all/%d/0/1'%(key_words)
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

	r.encoding = 'utf-8'
	html = etree.HTML(r.text)
	html_content = html.xpath("//div[@class='info']/a/text()")
	# print(len(html_content))
	html_url_o = html.xpath("//div[@class='info']//a//@href")
	html_url = []
	# 奇数下标的链接为up主主页url，去掉它
	for i in range(0,len(html_url_o),2):
		html_url.append(html_url_o[i])
	# print(html_url)
	html_details = html.xpath("//div[@class='detail']//text()")
	html_upname = []
	html_playt = []
	# print(len(html_details))
	# up主名字和播放量分别是list中第三个和第一个元素
	# 第二个元素为弹幕数量
	for i in range(0,len(html_details),3):
		html_upname.append(html_details[i+2])
		html_playt.append(html_details[i])
	# print(html_upname)
	# print(html_playt)

	res = []
	for i in range(len(html_content)):
		res.append([html_content[i],html_url[i],html_playt[i],html_upname[i]])
	# print(res)
	return res


# 将日榜信息格式化成string
def get_rank_text(msg,num):
	text = ""

	for i in range(min(num,len(msg))):
		text += "标题："+msg[i][0]+"\n"
		text += "链接："+msg[i][1]+"\n"
		text += "播放量："+msg[i][2]+"\n"
		text += "UP主："+msg[i][3]+"\r\n\r\n"

	return text



# 将b站搜索得到的内容格式化成string
def get_text(msg, num):
	text = ""

	for i in range(min(num,len(msg))):
		text += "标题："+msg[i][0]+"\n"
		text += "链接："+msg[i][1]+"\n"
		text += "播放量："+msg[i][2]+"\n"
		text += "上传时间："+msg[i][3]+"\n"
		text += "UP主："+msg[i][4]+"\r\n\r\n"

	return text



# 从用户获取日榜关键字，并查询
@on_command('bday', aliases=('b站日榜','b日榜','B站日榜','B日榜'))
async def blbl_rank(session: CommandSession):
	message_type = session.ctx['message_type']
	key_words = session.get('key_words', prompt='请输入B站日榜关键字\n目前支持关键字：全站/动画/国创/音乐/舞蹈/游戏/科技/数码/生活/鬼畜/时尚/娱乐/影视')
	text = "请稍等……"
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)
	
	ind = BILI_RANK.get(key_words,-1)
	msg = ""
	if ind == -1:
		msg = "没有这一栏哦~"
	else:
		msg = get_rank(ind)

	text = msg

	if text!="爬取失败！" and text!="没有这一栏哦~":
		if len(text)!=0:
			text = "获取成功！\n（获取排行榜前5名）：\r\n\n".format(key_words)
			text += get_rank_text(msg,5)
		else:
			text = "你不要搞我"

	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=%s]'%(session.ctx['user_id'])+text)
		# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)




# 从qq客户端获取用户输入的关键字，并进行查询
@on_command('b', aliases=('blbl','bilibili','b站','B站','bili'))
async def blbl(session: CommandSession):
	message_type = session.ctx['message_type']
	key_words = session.get('key_words', prompt='请输入B站视频搜索关键字')
	
	text = "请稍等……"
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)
	
	msg = get_bv(key_words)
	text = msg
	if text!="爬取失败！":
		if len(text)!=0:
			text = "有关“{0}”的视频（获取搜索结果前8条）：\r\n\n".format(key_words)
			text += get_text(msg,8)
		else:
			text = "你不要搞我"

	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=%s]'%(session.ctx['user_id'])+text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



# 手写参数解析器
@blbl.args_parser
@blbl_rank.args_parser
async def _(session:CommandSession):
	stripped_arg = session.current_arg_text.strip()

	if session.is_first_run:
		if stripped_arg:
			session.state['key_words'] = stripped_arg
		return

	if not stripped_arg:
		session.pause('关键字不能为空呢，请重新输入')

	session.state[session.current_key] = stripped_arg



if __name__ == '__main__':

	msg = get_rank(BILI_RANK.get("影视"))
	# print(get_text(msg,8))