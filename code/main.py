# encoding: utf-8:
import json
import random
import datetime

import valorant

from datetime import datetime, timedelta

from khl import Bot, Message, EventTypes, Event
from khl.card import CardMessage, Card, Module, Element, Types, Struct
from khl.command import Rule

# 新建机器人，token 就是机器人的身份凭证
# 用 json 读取 config.json，装载到 config 里
# 注意文件路径，要是提示找不到文件的话，就 cd 一下工作目录/改一下这里
with open('./config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
# 用读取来的 config 初始化 bot，字段对应即可
bot = Bot(token=config['token'])


##########################################################################################
##########################################################################################


# @ 是「装饰器」语法，大家可以网上搜搜教程，我们这里直接用就行
# bot 是我们刚刚新建的机器人，声明这个指令是要注册到 bot 中的
# name 标示了指令的名字，名字也被用于触发指令，所以我们 /hello 才会让机器人有反应
# async def 说明这是一个异步函数，khl.py 是异步框架，所以指令也需要是异步的
# world 是函数名，可以自选；函数第一个参数的类型固定为 Message
@bot.command(name='hello')
async def world(msg: Message):
    await msg.reply('你好呀~')

# help命令
@bot.command()
async def Ahri(msg: Message):
    # msg 触发指令为 `/Ahri`,因为help指令和其他机器人冲突
    cm = CardMessage()

    c3 = Card(Module.Header('你可以用下面这些指令调戏本狸哦！'), Module.Context('更多调戏方式上线中...'))
    #实现卡片的markdown文本
    #c3.append(Module.Section(Element.Text('用`/hello`来和阿狸打个招呼吧！',Types.Text.KMD)))
    c3.append(Module.Section('「/hello」来和本狸打个招呼吧！\n「/Ahri」 帮助指令\n'))
    c3.append(Module.Divider())
    c3.append(Module.Header('上号，瓦一把！'))
    c3.append(Module.Section("「/val 错误码」 游戏错误码的解决方法，0为已包含的val报错码信息\n「/DX」 关于DirectX Runtime报错的解决方案\n\n「/saveid '游戏id'」 保存(修改)您的游戏id\n「/myid」 让阿狸说出您的游戏id\n"))
    c3.append(Module.Divider())
    c3.append(Module.Header('和阿狸玩小游戏吧~ '))
    c3.append(Module.Section('「/roll 1 100」 掷骰子1-100，范围可自主调节。可在末尾添加第三个参数实现同时掷多个骰子\n「/countdown 秒数」倒计时，默认60秒\n「更多…」 还有一些隐藏指令哦~\n'))
    c3.append(Module.Divider())
    c3.append(Module.Section(' 游戏打累了？想来本狸的家坐坐吗~',
              Element.Button('让我康康', 'https://github.com/Aewait/Valorant-kaiheila-bot', Types.Click.LINK)))
    cm.append(c3)

    await msg.reply(cm)


#################################################################################################
#################################################################################################

# 倒计时函数，单位为秒，默认60秒
@bot.command()
async def countdown(msg: Message,time: int = 60):
    cm = CardMessage()

    c1 = Card(Module.Header('本狸帮你按下秒表喽~'), color=(198, 65, 55)) # color=(90,59,215) is another available form
    c1.append(Module.Divider())
    c1.append(Module.Countdown(datetime.now() + timedelta( seconds=time), mode=Types.CountdownMode.SECOND))
    cm.append(c1)

    await msg.reply(cm)

# 掷骰子
# invoke this via saying `!roll 1 100` in channel,or `/roll 1 100 5` to dice 5 times once
@bot.command()
async def roll(msg: Message, t_min: int, t_max: int, n: int = 1):
    result = [random.randint(t_min, t_max) for i in range(n)]
    await msg.reply(f'掷出来啦: {result}')


# 当有人输入“/yes @某一个用户”时这个语句被触发（感觉没用？）
@bot.command(rules=[Rule.is_mention_all])
async def yes(msg: Message, mention_str: str):
    await msg.reply(f'yes! mentioned all with {mention_str}')

    
# 设定自己的规则
def my_rule(msg: Message) -> bool:
    return msg.content.find('khl') != -1
# 只有包含 'khl'的语句才能出发，比如 "/test_mine khl-go"
@bot.command(name='test_mine', rules=[my_rule])
async def test_mine(msg: Message, comment: str):
    await msg.reply(f'yes! {comment} can trigger this command')


# # 正则表达式（实测无效）
# @bot.command(regex = r'(.+)\\(met\\)ID\\(met\\)')
# async def cmd(msg: Message, text: str, user_id: str):
    # #pass 
    # await msg.reply('who are u')

# 当有人“/狸狸 @机器人”的时候进行回复，可识别出是否为机器人作者
@bot.command(name='狸狸', rules=[Rule.is_bot_mentioned(bot)])
async def atAhri(msg: Message, mention_str: str):
    if msg.author_id == '1961572535':
        await msg.reply(f'主人有何吩咐呀~')
    else:
        await msg.reply(f'呀，听说有人想我了，是吗？')


# for Bilibili Up @uncle艾登
@bot.command()
async def uncle(msg: Message):
    await msg.reply('本狸才不喜欢`又硬又细`的人呢~\n[https://s1.ax1x.com/2022/06/24/jFGjHA.png](https://s1.ax1x.com/2022/06/24/jFGjHA.png)')


###########################################################################################
####################################以下是游戏相关代码区#####################################
###########################################################################################

from val import kda123,skin123,saveid123,saveid1,saveid2,myid123,val123,dx123

# 中二病
@bot.command(name='kda')
async def kda(msg: Message):
    await kda123(msg)

# 查询皮肤系列
@bot.command()
async def skin(msg: Message,name:str):
    await skin123(msg,name)
 
# 存储用户游戏id
@bot.command()
async def saveid(msg: Message,game1:str):
    await saveid123(msg,game1)

# 存储id的help命令 
@bot.command(name='saveid1')
async def saveid(msg: Message):
    await saveid1(msg)
# 已保存id总数
@bot.command(name='saveid2')
async def saveid(msg: Message):
    await saveid2(msg)

# 实现读取用户游戏ID并返回
#@bot.command(rules=[Rule.is_bot_mentioned(bot)])# myid不需要at机器人
@bot.command(name="myid",aliases=['MYID']) # 这里的aliases是别名
async def myid(msg: Message):
    await myid123(msg)

# 查询游戏错误码
@bot.command()
async def val(msg: Message, num: int):
    await val123(msg,num)

#关于dx报错的解决方法
@bot.command(name='DX',aliases=['dx'])# 新增别名dx
async def dx(msg: Message):
    await dx123(msg)


# 凭证传好了、机器人新建好了、指令也注册完了
# 下面运行机器人，bot.run()是机器人的起跑线
bot.run()
