import logging
import re
from collections import Counter
from itertools import chain

from .base import base
from .._jobs import CmdJob, add_job

similar_chars = [
    '珥尔耳鲁露卢勒拉菈利莉丽里吕李',
    '书修休杰珠裘鸠吉基其姬奇齐',
    '库克古谷格铬科赫黑海哈',
    '托图多朵特提狄缇德蒂黛',
    '丝斯司兹茨',
    '娅亚雅阿安',
    '肯卡嘉加伽',
    '菲福飞弗芙',
    '莎沙纱萨',
    '西希席叙',
    '娜纳那',
    '空柯寇',
    '艾爱埃',
    '贝培佩',
    '赛瑟札',
    '乌厄',
    '佛沃',
    '因茵',
    '塞泽',
    '奥欧',
    '威维',
    '尤由',
    '昴昂',
    '梅麦',
    '汀丁',
    '碧比',
    '米蜜',
    '菜莱',
    '蕾雷',
    '.·',
]

all_chars = ''.join(similar_chars)
if len(all_chars) != len(set(all_chars)):
    chars_counter = Counter(''.join(similar_chars))
    logging.error(chars_counter.most_common(16))
    assert 0

names = [  # 多字少字的
    '菜月·?昴',
    '安娜斯?塔西娅',
    '培提尔其乌?斯',
    '威尔海(鲁)?姆',
    '莱茵哈鲁?特',
]
names += [  # 普通的
    '丝碧卡',
    '亚拉基亚',
    '亨克尔',
    '伽那库斯',
    '佛拉基亚',
    '佛格',
    '克林德',
    '利布雷',
    '卡佩拉',
    '卡吉雷斯',
    '卡尔兰',
    '卡尔斯腾',
    '卡德蒙',
    '卡拉拉基',
    '卡斯图鲁平原',
    '卡萝',
    '卡蜜拉',
    '古斯提科',
    '史泰德',
    '裘斯',
    '塞西尔斯',
    '夏乌拉',
    '夏库纳尔',
    '多鲁特洛',
    '奇力塔卡',
    '娅艾',
    '安妮罗泽',
    '密涅瓦',
    '尤里乌斯',
    '希尔菲',
    '希斯尼娅',
    '帕克',
    '帕特拉修',
    '库乌德',
    '库奥克',
    '库珥修',
    '库鲁刚',
    '弗琉盖尔',
    '弗莱巴尔',
    '弗鲁夫',
    '戴因',
    '拉塞尔',
    '提姆兹',
    '文森特',
    '斯芬克丝',
    '普拉姆',
    '普莉希拉',
    '李凯尔特',
    '查普',
    '格拉姆达特',
    '格拉希丝',
    '格蕾丝',
    '梅卡德',
    '梅娜',
    '梅拉奎拉',
    '欧尔尼娅',
    '欧米伽',
    '比恩',
    '汉娜',
    '沃尔夫',
    '波尔多',
    '波尔肯尼卡',
    '泰玛艾',
    '潘多拉',
    '特蕾西亚',
    '玛洛妮',
    '琉兹',
    '琉加',
    '璞可',
    '皮波特',
    '盖因',
    '碧翠丝',
    '福斯特',
    '米尔多',
    '米捷尔',
    '米路德',
    '约书亚',
    '缇丰',
    '缇莉艾娜',
    '罗伊',
    '罗兹瓦尔',
    '梅札斯',
    '罗姆爷',
    '艾佐',
    '艾力欧尔大森林',
    '艾奇多娜',
    '艾米莉娅',
    '艾西亚湿地',
    '芙蕾德莉卡',
    '荒地的合辛',
    '莉可莉丝',
    '莉莉安娜',
    '莎克拉',
    '莎缇拉',
    '莱伊',
    '莱普',
    '菜月菜穗子',
    '菜月贤一',
    '菲莉丝',
    '萨尔姆',
    '葛利奇',
    '蒂亚斯',
    '蕾姆',
    '蜜蜜',
    '席里乌斯',
    '谢尔盖',
    '贾雷克',
    '赛赫麦特',
    '赫克托尔',
    '赫罗西欧',
    '赫鲁贝尔',
    '达德利',
    '达芙妮',
    '迈尔斯',
    '邱登',
    '里卡多',
    '铁之牙',
    '阿尼茉尼',
    '阿拉姆村',
    '阿斯特雷亚',
    '阿汉',
    '阿珍',
    '阿顿',
    '雷古勒斯',
    '雷诺',
    '露伊',
    '露格尼卡',
    '马可仕',
    '麦克罗托夫',
    '黑塔罗',
    '基尔提拉乌',
    '巴登凯托斯',
    '塞坦塔',
    '特里亚斯',
    '欧德古勒斯',
    '拉古那',
    '埃尔纱幕',
    '汀泽尔',
    '贝阿托莉丝',
    '奥斯洛',
    '雷金',
    '柯司兹尔',
    '福尔图娜',
    '汤普森',
    '莉西亚',
]
names += [  # 需要特判的
    '加菲尔(?!丝)(?!特)(?!艾)',
    '拉菲尔(?!丝)(?!特)(?!艾)',
    '(?<!加)(?<!拉)菲鲁特(?!娜)',
    '利格鲁(?!卡)(?!姆)',
    '佩特拉(?!其乌斯)(?!姆)',
    '格林(?!德)',
    '(?<!艾米)莉亚拉',
    '(?<!萨)(?<!伽)拉姆(?!莉鲁)',
    '(?<!帕)贝尔托',
    '(?<!帕)提修雅',
    '凯缇(?!尔)(?!斯)',
    '(?<!莱茵哈鲁)缇碧(?!翠)',
    '艾尔莎(?!幕)',
    '(?<!多萝西)(?<!艾米莉)(?<!贝)(?<!约书)亚齐',
    '(?<!艾尔)萨德(?!拉)(?!兰)',
    '梅尔蒂(?!典)',
    '弗雷德(?!莉卡)',
    '(?<!丢)芙拉姆',
    '(?<!加)弗利艾',
]

_ = [  # 特判太麻烦的，不处理
    '梅丽(?!乌)(?!奎拉)(?!蒂)',
    '(?<!格)(?<!芙)(?<!·)雷德',
    '(?<!格拉姆)达兹(?!利)',
    '(?<!莉)卢安娜',
    '(?<!文森)狄加',
]

repl = base.copy()

for n in names:
    o = n
    n = n.replace('?', '')
    n = re.sub(r'\(.*?\)', '', n)
    for s in similar_chars:
        o = re.sub(rf'[{s}]', rf'[{s}]', o)
    if o != n:
        repl += [o, n]

pairs = [  # 难以用similar_chars自动生成的部分
    ('[凛萍苹]果', '凛果'),
    ('半精灵', '半Elf'),
    ('贝阿托莉丝', '碧翠丝'),
    ('[奥欧]德', '欧德'),
    ('[奥欧]托', '奥托'),
    ('[修舒]尔特', '修尔特'),
    ('(?<!莉)(?<!希斯尼)阿[珥尔耳鲁露卢勒拉菈利莉丽里吕李](?!姆)(?!伯)(?!基亚)', '阿尔'),
    ('欧德(?!古勒斯)|魂力', '{{Od}}'),
    ('拉古那|源池', '{{Laguna}}'),
    (r'\{\{Od\}\}\{\{Laguna\}\}', '{{Od}}·{{Laguna}}'),
    ('空斯图卢', '柯司兹尔'),
]

repl.extend(chain(*pairs))

add_job(CmdJob(repl))
