#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 角色(添加的时候,可能要同时在后面的角色列表中添加,因为有些角色并不用于分配)
ROLE_DEAD       = ("死亡", -1)
ROLE_JUDGE      = ("法官", 0)
ROLE_KILLER     = ("狼人", 1)
ROLE_COMMONER   = ("平民", 2)
ROLE_WITCH      = ("女巫", 3)
ROLE_PROPHET    = ("预言家", 4)
ROLE_HUNTER     = ("猎人", 5)
ROLE_SB         = ("白痴", 6)
ROLE_CUPID      = ("丘比特", 7)
ROLE_GUARD      = ("守卫", 8)

# 可用角色
AVAILABLE_ROLE = [
    ROLE_KILLER,
    ROLE_COMMONER,
    ROLE_WITCH,
    ROLE_PROPHET,
    ROLE_HUNTER,
    ROLE_SB,
    ROLE_CUPID,
    ROLE_GUARD
]

# 角色列表
ROLE_ALLOCATE_LIST = {i[1]: i for i in AVAILABLE_ROLE}
'''
# 类似这样
ROLE_ALLOCATE_LIST = {
    1 : ROLE_KILLER,
    2 : ROLE_COMMONER,
    3 : ROLE_WITCH,
    4 : ROLE_PROPHET,
    5 : ROLE_HUNTER,
    6 : ROLE_SB,
    7 : ROLE_CUPID,
    8 : ROLE_GUARD
}
'''

# 玩家状态
STATUS_ALIVE    = ("存活", 100)
STATUS_DEAD     = ("死亡", 101)

# 事件
EVENT_OPEN_EYES     = ("睁眼", 1000)
EVENT_KILL          = ("狼人杀人", 1001)
EVENT_RESCUE        = ("女巫救人", 1002)
EVENT_POISON        = ("女巫毒人", 1003)
EVENT_SHOOT         = ("猎人开枪", 1004)
EVENT_SB_APPEAR     = ("白痴技能", 1005)
EVENT_MARRIED       = ("连结情侣", 1006)
EVENT_LOVERS_SEE    = ("情侣互相示意对方", 1007)
EVENT_GET_IDENTITY  = ("预言家验人", 1008)
EVENT_ELECT_POLICE  = ("竞选警长", 1009)
EVENT_SPEAK         = ("发言", 1010)
EVENT_VOTE          = ("投票出局", 1011)
EVENT_CLOSE_EYES    = ("闭眼", 1012)

# 获得中文含义 - meaning
def M(constant):
    try:
        return constant[0]
    except IndexError:
        return False

# 获得常量对应的编码 - code
def C(constant):
    try:
        return constant[1]
    except IndexError:
        return False

# 获得角色列表
def R():
    for k, v in ROLE_ALLOCATE_LIST.items():
        print(k, v[0])
