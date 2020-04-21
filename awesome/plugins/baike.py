import requests
import random
from lxml import etree
from nonebot import on_command, CommandSession


DIFFICULTY_RANK = {'简单':[1,100],'稍难':[101,200],'魔鬼':[201,500],'做出来叫你爸爸':[501,702]}

# 获取欧拉计划题目
def get_euler_url(words_list):
	ran = random.randint(words_list[0],words_list[1])
	url = "https://projecteuler.net/problem=%d"%(ran)
	return url


# 从百度百科爬取内容简介
def get_bdbk(key_words):
	url = "https://baike.baidu.com/item/%s"%(key_words)
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
	}
	r = requests.get(url,timeout=5,headers=headers)
	cnt = 0
	while r.status_code!=200:
		cnt += 1
		if cnt >= 3:
			return ["爬取失败！"]
		r = requests.get(url,timeout=5,headers=headers)

	r.encoding = 'utf-8'
	html = etree.HTML(r.text)
	html_content = html.xpath("//meta[@name='description']//@content")
	
	res = html_content
	if res == []:
		res.append("没有这条内容呢")
	else:
		res.append("\n\n更多内容可进入词条查看：\n%s"%url)
	# print(res)
	return res



# 从维基百科爬取内容简介
def get_wkbk(key_words):
	url = 'https://zh.wikipedia.org/wiki/%s'%(key_words)
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
	}
	try:
		r = requests.get(url,timeout=5,headers=headers)
	except:
		return ['爬取失败']

	cnt = 0
	while r.status_code!=200:
		cnt += 1
		if cnt >= 3:
			return ["爬取失败！"]
		r = requests.get(url,timeout=5,headers=headers)

	r.encoding = 'utf-8'
	html = etree.HTML(r.text)
	html_content = html.xpath("//p//text()")
	
	res = html_content
	if res == []:
		res.append("没有这条内容呢")
	else:
		res.append("\n\n更多内容可进入词条查看：（需要科学上网哦~）\n%s"%url)
	# print(res)
	return res



# 将百度百科列表内容格式化列表为string
def get_text(msg):
	text = ""

	for i in msg:
		text += i
	return text


# 将维基百科列表内容格式化为string
def get_text_wiki(msg):
	text = ""

	for ele in msg[:-1]:
		if ele[0] == '[' and ele[-1] == ']' and len(ele) == 3:
			continue
		if ele[:10] == '.mw-parser':
			continue
		text += ele.strip()

	return text[:200] + "……" + msg[-1]



@on_command('编程题',aliases=('出题','编程数学题'))
async def euler(session: CommandSession):
	message_type = session.ctx['message_type']
	key_words = session.get('key_words', prompt='（PS：题目都是英文题面）\n请选择难度:\n- 简单（其实不简单）\n- 稍难（其实很难）\n- 魔鬼\n- 做出来叫你爸爸')

	text = ""
	dif = DIFFICULTY_RANK.get(key_words,-1)
	if  dif == -1:
		text += "没有这种难度哦~" 
	else:
		text += "[%s]难度 题目链接：\n"%(key_words)
		text += get_euler_url(dif)

	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=%s]\n\n'%(session.ctx['user_id'])+text)
		# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



# 从用户获取关键字，并查询百度百科+维基百科
@on_command('百科')
async def baike(session: CommandSession):
	message_type = session.ctx['message_type']
	key_words = session.get('key_words', prompt='请输入关键字')
	
	text = "请稍等……"
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)
	
	bdbk_msg = get_bdbk(key_words)
	wkbk_msg = get_wkbk(key_words)

	msg = ""
	msg += "\n百度百科：\r\n" + get_text(bdbk_msg) +"\r\n\n"
	msg += "-"*40
	msg += "\n维基百科中文站：\r\n" + get_text_wiki(wkbk_msg) +"\r\nPS:出现乱码请自动无视\r\n\n"
	msg += "-"*40

	text = msg
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=%s]\n\n'%(session.ctx['user_id'])+text)
		# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



# 手写参数解析器
@baike.args_parser
@euler.args_parser
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

	msg = get_wkbk("pink")
	print(get_text_wiki(msg))