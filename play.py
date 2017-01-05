#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'tyruschin'

from config import *
import random

# 全局的一些量
# 还没开始
global my_roles             # 角色配置的编号列表
global players_count        # 玩家总人数
global killers_count        # 狼人人数
global commoners_count      # 平民人数
global kill_protect         # 首杀保护
global foresee_protect      # 首验保护
global compare_identity     # 身份列表(有序的),可以用来检查身份分发是否正确

# 开始之后
global identity_list        # 列表:每个玩家的位置号 => 身份号,如3号玩家是女巫且存活,identity_list[3] = ROLE_WITCH[1],如果玩家已经死亡,则身份号置为-1(ROLE_DEAD[1])
global is_confirm_identity  # 是否需要睁眼确认身份
global play_type            # 屠边1,屠城2
global day                  # 第几天
global guarded_list         # 保护的列表,由于不能连续两晚守同一个人,所以直接用列表存储
global lover                # 情侣
global killed               # 这一天被杀的人
global rescued              # 救的情况,(1, 0)表示还有解药,(0, 3)表示这一回合救了3号,(0, 0)表示解药已经用完
global poisoned             # 毒的情况,同上

# 开始前的配置
def pre_start():
    global my_roles
    global players_count
    global killers_count
    global commoners_count
    global identity_list
    global compare_identity
    global is_confirm_identity
    global play_type
    global kill_protect
    global foresee_protect
    flag = input("采用屠边规则吗?(y/n),y是屠边,n是屠城: ")
    if equals_y(flag):
        play_type = 1
    else:
        play_type = 2
    print("当前默认配置如下:")
    my_roles = set([i[1] for i in gaoshi_default_config['roles']])
    print_roles_config()
    # 角色
    flag = input("是否要修改角色配置?(y/n)")
    if equals_y(flag):
        my_roles = modify_roles_config()
    print_roles_config()
    print("-------------狼人和平民的数目-------------")
    # 狼和平民的数量
    killers_count = int(input("狼人数目: "))
    commoners_count = int(input("平民数目: "))
    players_count = killers_count + commoners_count + len(my_roles) - 2
    print("----------------人员分配----------------")
    print("总人数:", players_count)
    print("狼人:", killers_count)
    print("平民:", commoners_count)
    identity_list = []
    identity_list.extend([constant.ROLE_KILLER[1]] * killers_count)
    identity_list.extend([constant.ROLE_COMMONER[1]] * commoners_count)
    for i in my_roles:
        if i not in (1, 2):
            identity_list.append(constant.ROLE_ALLOCATE_LIST[i][1])
            print(constant.ROLE_ALLOCATE_LIST[i][0]+":", 1)
    # 保存一个副本到compare_identity,打乱,相当于分配身份
    random.shuffle(identity_list)
    identity_list.append(identity_list[0])
    identity_list[0] = constant.ROLE_COMMONER[1]    # 第0个位置不使用
    compare_identity = sorted(identity_list)
    flag = input("系统已经分配好了人员身份,是否手动分配(适用于发牌玩的情况)?(y/n)")

    # 这种分配方式好像不太好,用睁眼闭眼比较好
    # while equals_y(flag):
    #     print_roles_config(True)
    #     print("请根据上面的编号,分别为每位玩家设定身份:")
    #     temp_list = [0] # 临时保存,全部输入之后还要做个比对确认身份正确才赋值
    #     for i in range(1, players_count+1):
    #         temp_list.append(int(input("第"+str(i)+"位玩家的身份: ")))
    #     if sorted(identity_list) == sorted(temp_list):
    #         # 身份是不是全部都放入了
    #         identity_list = temp_list
    #         flag = 'n'
    #     else:
    #         print("身份设定异常,请重新试试")
    #         flag = 'y'

    if equals_y(flag):
        # 全部先定义成平民
        identity_list = [constant.ROLE_COMMONER[1]] * (players_count+1)
        is_confirm_identity = True
    else:
        is_confirm_identity = False

    # 首杀首验保护
    num = int(input("首杀保护: "))
    if is_exist_player(num):
        kill_protect = num
    num = int(input("首验保护: "))
    if is_exist_player(num):
        foresee_protect = num

    # print(identity_list)

# 当前角色配置
def print_roles_config(code = False):
    # code 是表示角色编号,默认是不打印的
    global my_roles
    print("角色:", end=' ')
    for role in my_roles:
        if code:
            print(
                constant.ROLE_ALLOCATE_LIST[role][0],
                "(编号:"+str(constant.ROLE_ALLOCATE_LIST[role][1])+")",
                end=', '
            )
        else:
            print(constant.ROLE_ALLOCATE_LIST[role][0], end=', ')

    print("一共{}种角色".format(len(my_roles)))

# 修改角色配置
def modify_roles_config():
    print("角色列表:")
    constant.R()
    my_roles = {}
    flag = True # 循环选择
    while flag:
        roles_string = input("根据列表的编号,选择相应的角色,用空格隔开,eg: 1 2 3。注意,狼人和平民必选\n")
        roles_list = roles_string.split(' ')
        # 去掉多余空格并去重
        roles_list = [int(s) for s in roles_list if s]
        roles_list = set(roles_list)
        print("你挑选了如下角色:")
        try:
            if constant.ROLE_KILLER[1] not in roles_list or constant.ROLE_COMMONER[1] not in roles_list:
                raise IndexError
            print_string = ""
            for i in roles_list:
                print_string = print_string + str(i) + " " + constant.ROLE_ALLOCATE_LIST[i][0] + "\n"
            print(print_string)
            confirm = input("是否确定使用此角色配置?(y/n)")
            if equals_y(confirm):
                for i in roles_list:
                    my_roles[i] = constant.ROLE_ALLOCATE_LIST[i]
                flag = False
        except IndexError:
            print("输入的角色号有误或不全,请重新输入")
            # print("log: ", roles_list)
    return my_roles

# 开始
def start():
    global is_confirm_identity
    global identity_list
    global compare_identity
    global players_count
    global day
    day = 1
    confirm = True
    print("----------------游戏开始----------------")
    if is_confirm_identity:
        # 需要睁眼确定身份并开始第一轮
        while confirm:
            try:
                night_hunter()
                night_sb()
                night_guard()
                night_cupid()
                night_killer()
                night_witch()
                night_prophet()

                # 检查是否记录正确!
                if sorted(compare_identity) != sorted(identity_list):
                    print("身份分发有误,请检查,并重新分发")
                    print(compare_identity)
                    print(identity_list)
                    raise ValueError

                confirm = False
            except ValueError:
                # 清空重来
                identity_list = [constant.ROLE_COMMONER[1]] * (players_count+1)

    else:
        night_guard()
        night_cupid()
        night_killer()
        night_witch()
        night_prophet()

###### 夜晚

def empty_func():
    pass

# 公共方法
def night_common(identity_array, first_night = True, callback = empty_func):
    global identity_list
    global players_count
    global killers_count
    global my_roles
    identity = identity_array[0]
    code = identity_array[1]
    if code not in my_roles:
        return False
    print(identity+"请睁眼")
    if first_night:
        cycle_times = 1
        if identity_array == constant.ROLE_KILLER:
            # 狼人的情况,要输入多个玩家的号码
            cycle_times = killers_count
            print("输入狼人,注意逐个玩家的号码输入!")
        for ct in range(cycle_times):
            flag = True
            while flag:
                num = int(input(identity+str(ct+1)+": "))
                if is_exist_player(num) and identity_list[num] == constant.ROLE_COMMONER[1]:
                    identity_list[num] = code
                    flag = False
                else:
                    print("输入号码错误或这个玩家已经被定义身份,请检查")
                    retry = input("y表示从头开始输入全部身份,n表示重新输入此身份: ")
                    if equals_y(retry):
                        raise ValueError
    callback()
    print(identity+"请闭眼")

# 猎人
def night_hunter():
    night_common(constant.ROLE_HUNTER)

# 白痴
def night_sb():
    night_common(constant.ROLE_SB)

# 守卫
def night_guard():
    global day
    global guarded_list

    # 守护的过程
    def guarding():
        global guarded_list
        flag = True
        while flag:
            num = int(input("守卫请选择要守护的人(空守输入0): "))
            if num == 0 or (is_exist_player(num) and is_alive_player(num) and num != guarded_list[len(guarded_list)-1]):
                guarded_list.append(num)
                flag = False
            else:
                print("角色号有误,或者连续两夜守护同一个人")

    if day == 1:
        guarded_list = [0]
        night_common(constant.ROLE_GUARD, True, guarding)
    else:
        night_common(constant.ROLE_GUARD, False, guarding)


# 丘比特
def night_cupid():
    global lover

    # 连成情侣
    def marring():
        global lover
        flag = True
        while flag:
            lover_string = input("丘比特请选择两个人成为情侣,用空格隔开(如: 3 5): ")
            lover_list = lover_string.split(' ')
            # 去掉多余空格并去重
            lover_list = [int(s) for s in lover_list if s]
            lover_list = list(set(lover_list))
            if len(lover_list) == 2 and is_exist_player(lover_list[0]) and is_exist_player(lover_list[1]):
                lover = lover_list
                flag = False
            else:
                print("角色号有误,或者输入了超过两个号码")

    if night_common(constant.ROLE_CUPID, True, marring):
        night_lover()


# 恋人
def night_lover():
    global lover
    print("下面我绕场一周,被我拍到的两个人就是情侣")
    print("丘比特选择的情侣是:", str(lover))
    print("情侣请睁眼,请相互示意对方")
    print("情侣请闭眼")

# 狼人
def night_killer():
    global day
    global killed

    def killing():
        global day
        global killed
        flag = True
        while flag:
            num = int(input("狼人请选择要杀的人(空刀输入0): "))
            if num == 0 or (is_exist_player(num) and is_alive_player(num)):
                if day == 1 and num == kill_protect:
                    print("首杀保护!请重新选择")
                else:
                    killed = num
                    flag = False
            else:
                print("角色号有误")

    if day == 1:
        night_common(constant.ROLE_KILLER, True, killing)
    else:
        night_common(constant.ROLE_KILLER, False, killing)

# 女巫
def night_witch():
    global day
    global rescued
    global poisoned
    global killed

    def res_and_poi():
        global day
        global rescued
        global poisoned
        global killed
        print("今晚ta死了,你有一瓶解药要不要救 ("+str(killed)+"号玩家死亡),你有一瓶毒药要不要毒死谁?")
        command = input("y表示救起,数字表示毒死指定号数,0表示不做任何事: ")
        flag = True
        while flag:
            if equals_y(command) and rescued == (1, 0):
                if day != 1 and killed == constant.ROLE_WITCH[1]:
                    print("女巫第二晚及之后不能自救")
                else:
                    rescued = (1, killed)
                    flag = False
            elif is_exist_player(int(command)) and is_alive_player(int(command)) and poisoned == (1, 0):
                poisoned = (1, int(command))
                flag = False
            elif int(command) == 0:
                flag = False
            else:
                print("玩家已经死亡,或者(解、毒)药已经用过")

    if day == 1:
        rescued = (1, 0)
        poisoned = (1, 0)
        night_common(constant.ROLE_WITCH, True, res_and_poi)
    else:
        night_common(constant.ROLE_WITCH, False, res_and_poi)

# 预言家
def night_prophet():
    global day
    global identity_list

    def foreseeing():
        global day
        global identity_list
        flag = True
        while flag:
            num = int(input("预言家可以验明一个人的身份: "))
            if is_exist_player(num) and is_alive_player(num):
                if day == 1 and num == foresee_protect:
                    print("首验保护!请重新选择")
                else:
                    if identity_list[num] == constant.ROLE_KILLER[1]:
                        print("好人、坏人,ta是这个 (坏人)")
                    else:
                        print("好人、坏人,ta是这个 (好人)")
                    flag = False
            else:
                print("角色号有误")

    if day == 1:
        night_common(constant.ROLE_PROPHET, True, foreseeing)
    else:
        night_common(constant.ROLE_PROPHET, False, foreseeing)


###### 白天



###### 判定

# y/n
def equals_y(flag):
    if flag == 'y' or flag == 'Y':
        return True
    return False

# 玩家位置是否存在
def is_exist_player(num):
    global players_count
    if num > 0 and num <= players_count:
        return True
    return False

# 当前存活玩家
def alive_players():
    global identity_list
    alive = []
    for num, code in enumerate(identity_list):
        if code != constant.ROLE_DEAD:
            alive.append(num)
    return alive

# 玩家是否还活着
def is_alive_player(num):
    global identity_list
    if identity_list[num] != constant.ROLE_DEAD:
        return True
    return False

# 夜晚死亡情况
def night_dying_msg():
    pass

# 白天死亡情况(并加1天)
def day_dying_msg():
    pass

# 游戏是否结束
def is_end():
    pass

###### 记录

# 写入文件中,防止丢失
def log():
    pass

if __name__ == '__main__':
    pre_start()
    start()