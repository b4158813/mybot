import requests
import random
from lxml import etree
from nonebot import on_command, CommandSession
from group_ctr import *

DIFFICULTY_RANK = {'简单':[1,100],'稍难':[101,200],'魔鬼':[201,500],'做出来叫你爸爸':[501,616]}

I_SOLVED = {
	10:"答案：142913828922\n算法：可以直接暴力枚举，各种筛法（埃拉托斯特尼筛法、欧拉筛 等）会更快",
	14:"答案：837799\n算法：直接暴力即可"
}

# 获取欧拉计划题目
def get_euler_url(words_list):
	ran = random.randint(words_list[0],words_list[1])
	# url = "https://projecteuler.net/problem=%d"%(ran)
	url = "https://pe-cn.github.io/%d/"%(ran)
	return url,ran

# 获取答案解析
def get_euler_sovlved(ind):
	try:
		return I_SOLVED.get(int(ind),-1)
	except:
		return -1

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




# 查询此题答案
@on_command('答案',aliases=('题目答案','answer'))
async def euler_ans(session: CommandSession):
	message_type = session.ctx['message_type']
	if message_type == 'group' and session.ctx['group_id'] == NJQ:
		return

	# 如果不是主人发的消息
	if session.ctx['user_id'] != 814295903:
		text = '你不是主人QAQ'
		if (message_type == 'group'):
			await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
			# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
		elif (message_type == 'private'):
			await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)
		return

	ind = session.get('key_words', prompt='请输入题号')
	ans = get_euler_sovlved(ind)
	text = ""
	if ans == -1:
		text = "没有这题的的答案呢"
	else:
		text = "第%s题\n"%(ind)+ans

	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=%s]\n\n'%(session.ctx['user_id'])+text)
		# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)




# 欧拉计划出题
@on_command('编程题',aliases=('出题','编程数学题'))
async def euler(session: CommandSession):
	message_type = session.ctx['message_type']
	if message_type == 'group' and session.ctx['group_id'] == NJQ:
		return
	if session.ctx['user_id'] != 814295903:
		text = '你不是主人QAQ'
		if (message_type == 'group'):
			await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
			# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
		elif (message_type == 'private'):
			await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)
		return

	key_words = session.get('key_words', prompt='\n请选择难度:\n- 简单（其实不简单）\n- 稍难（其实很难）\n- 魔鬼\n- 做出来叫你爸爸\n\n或者直接输入题号')
	text = ""

	if key_words.isdigit():
		if int(key_words) > 616 or int(key_words) < 1:
			text += "超出题目范围QAQ"
		else:
			q = get_euler_url([int(key_words),int(key_words)])
			text += "[CQ:emoji,id=128161]第%d题\n题目链接：\n%s"%(q[1],q[0])
	else:
		dif = DIFFICULTY_RANK.get(key_words,-1)
		if  dif == -1:
			text += "没有这种难度哦~"
		else:
			q = get_euler_url(dif)
			text += "[%s]难度\n[CQ:emoji,id=128161]本题选自Project Euler第%d题\n题目链接：\n%s"%(key_words,q[1],q[0])


	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=%s]\n\n'%(session.ctx['user_id'])+text)
		# await session.bot.send_group_msg(group_id=session.ctx['group_id'], message='[CQ:at,qq=all]'+text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



# 从用户获取关键字，并查询百度百科+维基百科
@on_command('百科')
async def baike(session: CommandSession):
	message_type = session.ctx['message_type']
	if message_type == 'group' and session.ctx['group_id'] == NJQ:
		return
	key_words = session.get('key_words', prompt='请输入关键字')
	
	text = "请稍等……"
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)
	
	bdbk_msg = get_bdbk(key_words)
	wkbk_msg = get_wkbk(key_words)

	msg = ""
	msg += "\n[CQ:emoji,id=128161]百度百科：\r\n" + get_text(bdbk_msg) +"\r\n\n"
	msg += "-"*40
	msg += "\n[CQ:emoji,id=128161]维基百科中文站：\r\n" + get_text_wiki(wkbk_msg) +"\r\n\nPS:出现乱码请自动无视\r\n\n"
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
@euler_ans.args_parser
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

	# msg = get_wkbk("pink")
	# print(get_text_wiki(msg))

	print(get_euler_url(DIFFICULTY_RANK.get("简单")))