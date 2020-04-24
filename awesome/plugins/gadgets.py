'''
	机器人名字

	校园vpn获取

	健康打卡通知

	菜单功能显示
'''

from datetime import datetime
import nonebot
import requests
from lxml import etree
from nonebot import on_command, on_request, CommandSession
from aiocqhttp.exceptions import Error as CQHttpError
import json

from group_ctr import * # 群组控制


# 机器人名字
nn = '人民公仆'

# 获取当前时间 的 时分秒
# def GetTime(time=datetime.now())->list:
# 	Format = str(time)[11:19].split(':')
# 	return Format



# 返回校园vpn
@on_command('vpn',aliases=('校园网','上理vpn','VPN'))
async def vpn(session: CommandSession):
	text = "http://www.usst.edu.cn/xywww/list.htm"
	message_type = session.ctx['message_type']
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



# 健康打卡通知
@on_command('通知我',aliases=('提醒我'))
async def notice_me(session: CommandSession):
	message_type = session.ctx['message_type']
	if message_type == 'private':
		self_id = session.ctx['user_id']
		file = open('id.json','r',encoding='utf-8')
		js = file.read()
		id = json.loads(js)
		Id = id['user']
		ID = []
		for it in Id:
			if it == self_id:
				await session.bot.send_private_msg(user_id=self_id, message="您已经被通知无需操作！")
				return
			ID.append(it)
		ID.append(self_id)
		id['user'] = ID
		fp = open('id.json', 'w', encoding='utf-8')
		item_json = json.dumps(id, ensure_ascii=False)
		fp.write(item_json)
		fp.close()
		file.close()
		await session.bot.send_private_msg(user_id=self_id, message="将在每日9:50提醒您打卡！")
	else:
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message="来来来这位童鞋看过来\n\n输入：通知我\n（每天9：50提醒你打卡）\n\n输入：取消通知我\n（取消每天通知你）")



# 取消通知
@on_command('取消通知我',aliases=('取消提醒我'))
async def notice_me(session: CommandSession):
	message_type = session.ctx['message_type']
	if message_type == 'private':
		self_id = session.ctx['user_id']
		file = open('id.json','r',encoding='utf-8')
		js = file.read()
		id = json.loads(js)
		Id = id['user']
		ID = []
		for it in Id:
			if it == self_id:
				continue
			ID.append(it)
		id['user'] = ID
		fp = open('id.json', 'w', encoding='utf-8')
		item_json = json.dumps(id, ensure_ascii=False)
		fp.write(item_json)
		fp.close()
		file.close()
		await session.bot.send_private_msg(user_id=self_id, message="已经取消！")
	

# 导入要通知的好友
def LoadId() -> list:
	file = open('id.json','r',encoding='utf-8')
	js = file.read()
	id = json.loads(js)
	ID = id['user']
	print(ID)
	return ID



# 'interval', minutes=1
# 'cron', hour='12', minute='30'
@nonebot.scheduler.scheduled_job('cron', hour='9', minute='50')
async def _():
	bot = nonebot.get_bot()
	text = "同学打卡啦打卡啦~"
	try:
		ID = LoadId()
		for it in ID:
			await bot.send_private_msg(user_id=it, message=text)
	except CQHttpError:
		pass



# @on_command('色图',aliases=('涩图','ghs','pornhub'))
# async def vpn(session: CommandSession):
# 	message_type = session.ctx['message_type']
# 	text = '[CQ:image,file=打住.jpg]'
# 	if (message_type == 'group'):
# 		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
# 	elif (message_type == 'private'):
# 		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)




# 菜单功能
@on_command('菜单',aliases=('功能','list','列表'))
async def vpn(session: CommandSession):
	message_type = session.ctx['message_type']
	if message_type == 'group' and session.ctx['group_id'] == NJQ:
		text = '''欢迎使用{0}机器人

目前该群支持的功能有：
----------------------------------------
- {0} vpn
（获取上理vpn链接网址）

- {0} 通知我
（打卡提醒！加我为好友才能使用）
----------------------------------------
更多功能请加我为好友输入“功能”获取
'''.format(nn)
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
		return


	text = '''欢迎使用{0}机器人

目前支持的功能有：
----------------------------------------
- 点歌 xxx
（自动从QQ音乐获取该歌曲）

- {0} 教务处
（获取上理教务处新闻）

- {0} 上理新闻
（获取上理官网校务新闻）

- {0} vpn
（获取上理vpn链接网址）

- {0} b xxx
（查询b站关键字为xxx的视频内容）

- {0} bday xxx
（查询b站关键字为xxx的日榜内容）

- {0} 百科 xxx
（查询百度百科和维基百科）

- {0} 出题
（隐藏功能，只有主人可以用）

- {0} 通知我
（打卡提醒！加我为好友才能使用）
PS:此功能尚未完善
----------------------------------------
如果有bug请反馈给我的主人
QQ:814295903
更多垃圾功能敬请期待……
	'''.format(nn)

	
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)





if __name__ == '__main__':
	
	# print(GetTime()[0],GetTime()[1])

	# print(LoadId())

	pass