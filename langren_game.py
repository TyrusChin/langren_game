#!/usr/bin/env python3

__author__ = 'bjong'

from pprint import pprint

def thief():
	print('盗贼请选择你要的牌')
	print('盗贼请闭眼')


def cupid():
	print('丘比特请选择情侣')
	lovers = [ int(i) for i in input('情侣是：').split() ]
	peoples[lovers[0]]['love'] = lovers[1]
	peoples[lovers[1]]['love'] = lovers[0]
	print('丘比特请闭眼')


def guard():
	# print('守卫请选择要保护的人')
	safe_people = int(input('守卫请选择要保护的人：'))
	peoples[safe_people]['safe'] = True


def langren():
	print('浪人选择你要杀的人')
	tonight_dead_list.append(int(input('狼人要杀的人是：')))
	print(tonight_dead_list)


def witch():
	print('这个人死了：', tonight_dead_list[0])
	is_safe = input('你要救他么[y/n]：')
	if is_safe == 'y':
		peoples[tonight_dead_list[0]]['safe'] = True
	else:
		pass
	dead_people = input('有一瓶毒药要用么：')
	if dead_people:
		tonight_dead_list.append( int(dead_people) )
	else:
		pass
	# tonight_dead = 


def diviner():
	check_people = int(input('选择你要验的人：'))
	if peoples[check_people]['langren']:
		print('他是坏人')
	else:
		print('他是好人')


def god_active_(god_name):
	if god_name == 'thief':
		thief()
	elif god_name == 'guard':
		guard()
	elif god_name == 'cupid':
		cupid()
	elif god_name == 'langren':
		langren()
	elif god_name == 'witch':
		witch()
	elif god_name == 'diviner':
		diviner()


def god_active(god_name, init=False):
	print(god_name, '请睁眼')
	if init:
		god_sn_list = input(god_name +'是：').split()
		if god_sn_list:
			for god in god_sn_list:
				god_sn = int(god)
				peoples[god_sn][god_name] = True
			god_list.append(god_name)
		else:
			return
	else:
		pass
	return god_active_(god_name)
	print(god_name, '请闭眼')
		


# def god_init(god_name):


def first():
	god_active('thief', init=True)
	god_active('cupid', init=True)
	god_active('guard', init=True)
	god_active('langren', init=True)
	god_active('witch', init=True)
	god_active('diviner', init=True)
	print(god_list)


def kill_people(people):
	peoples[people]['dead'] = True
	return people

def try_kill_people():
	dead_people = [ kill_people(people)
					for people in tonight_dead_list
					if not peoples[people].get('safe') ]
	return dead_people
		# if peoples[dead_people]['safe']:
		# 	pass
		# else:
		# 	peoples[dead_people]['dead'] = True


def close_safe(people):
	peoples[people]['safe'] = False


def del_god():
	# del_god_list = ['thief', cupid, 
	if 'thief' in god_list:
		del god_list[god_list.index('thief')]
	if 'cupid' in god_list:
		del god_list[god_list.index('cupid')]
		# del god_list['cupid']


def new_game():
	global peoples, tonight_dead_list, god_list
	people_num = int(input('人数：'))
	peoples = { i:{} for i in range(1, people_num+1) }
	tonight_dead_list = []
	god_list = []
	is_first = True
	while True:
		print('天黑请闭眼')
		if is_first:
			first()
			del_god()
			is_first = False
			print('警长竞选')
		else:
			# god_list = ['langren', 'witch', 'diviner']
			# god_list =
			[ god_active(god) for god in god_list ]
		print('天亮了')
		dead_people = try_kill_people()
		if dead_people:
			print(dead_people, '死了')
		else:
			print('平安夜')
		[ print(i, peoples[i]) for i in peoples.keys() ]
		tonight_dead_list = []
		[ close_safe(people) for people in peoples if peoples[people].get('safe') ]


def main():
	while True:
		new_game()

if __name__ == '__main__':
	main()
