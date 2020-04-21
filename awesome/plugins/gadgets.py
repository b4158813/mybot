import requests
from lxml import etree
from nonebot import on_command, CommandSession

@on_command('vpn',aliases=('校园网','上理vpn','VPN'))
async def vpn(session: CommandSession):
	text = "http://www.usst.edu.cn/xywww/list.htm"
	message_type = session.ctx['message_type']
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



@on_command('菜单',aliases=('功能','list','列表'))
async def vpn(session: CommandSession):
	text = '''欢迎使用儿子机器人

目前支持的功能有：

- 点歌 xxx
（自动从QQ音乐获取该歌曲）

- 百科 xxx
（获得xxx的百度百科词条内容）

- 儿子 教务处
（获取上理教务处新闻）

- 儿子 上理新闻
（获取上理官网校务新闻）

- 儿子 vpn
（获取上理vpn链接网址）

- 儿子 b xxx
（查询b站关键字为xxx的视频内容）

- 儿子 bday xxx
（查询b站关键字为xxx的日榜内容）


更多垃圾功能敬请期待……
	'''
	message_type = session.ctx['message_type']
	if (message_type == 'group'):
		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
	elif (message_type == 'private'):
		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)



if __name__ == '__main__':
	
	pass