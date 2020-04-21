# from nonebot import on_command, CommandSession

# @on_command('weather', aliases=('天气','天气预报','查天气'))
# async def weather(session: CommandSession):
# 	city = session.get('city', prompt='你想查询哪个城市的天气呢？')
# 	text = await get_weather_of_city(city)

# 	message_type = session.ctx['message_type']
# 	if (message_type == 'group'):
# 		await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
# 	elif (message_type == 'private'):
# 		await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)

# # 手写参数解析器
# @weather.args_parser
# async def _(session:CommandSession):
# 	stripped_arg = session.current_arg_text.strip()

# 	if session.is_first_run:
# 		if stripped_arg:
# 			session.state['city'] = stripped_arg
# 		return

# 	if not stripped_arg:
# 		session.pause('要查询的城市名称不能为空呢，请重新输入')

# 	session.state[session.current_key] = stripped_arg

# async def get_weather_of_city(city: str) -> str:
# 	return f'{city}的天气是……'