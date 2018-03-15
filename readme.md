# Step 0: 确认已经安装语言包，如简体中文（它负责将Unicode编码按$LANG encode，如缺失则会使用ascii encode，报错）
```bash
$ sudo apt-get -y install language-pack-zh-hans-base
$ locale -a|grep zh_CN
zh_CN
zh_CN.gb2312
zh_CN.utf8
```
# Step 1: 编写Python 脚本
## 单文件版 i18n_demo.py
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gettext
import os
appName = 'i18n_demo'
languageDir = os.path.abspath('locales')
gettext.bindtextdomain(appName, languageDir)
gettext.bind_textdomain_codeset(appName, 'utf-8')    #输出utf-8编码后的字符串
gettext.textdomain(appName)    #这里返回utf-8编码后的结果

_ = gettext.gettext

print _('This is a translatable string.')
```

## 多文件时建议封装gettext，如：
locales/i18n.py: 
```python
import sys
import gettext as gt
import os
reload(sys)
sys.setdefaultencoding("utf-8")
def lgettext(domain_name, coding='utf-8'):
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    gt.bindtextdomain(domain_name, language_dir)
    gt.bind_textdomain_codeset(domain_name, coding)
    gt.textdomain(domain_name)
    return gt.lgettext
def gettext(domain_name):
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    gt.bindtextdomain(domain_name, language_dir)
    gt.textdomain(domain_name)
    return gt.gettext
def ugettext(domain_name):    #返回Unicode字符串，推荐使用
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    try:
        t = gt.translation(domain_name, language_dir)
    except IOError:
        return gettext(domain_name)
    return t.ugettext
```

其他文件只需导入
```python
import locales.i18n as i18n
_ = i18n.ugettext('i18n_demo')
```

# Step 2: xgettext命令

```bash
mkdir locales
#获取项目中所有需要翻译的文件
find . -name "*.py" > POTFILES
xgettext -k_ -o locales/i18n_demo.pot --from-code=UTF8 -n --files-from=POTFILES
#单文件
xgettext -k_ -o locales/i18n_demo.pot --from-code=UTF8 i18n_demo.py
```

# *Step 3: (添加新语言包时)根据语言创建po

```bash
mkdir -p locales/zh_CN/LC_MESSAGES/
cd locales/zh_CN/LC_MESSAGES
msginit -l zh_CN -i ../../i18n_demo.pot
#更新
msgmerge zh_CN.po ../../mt_apksec.pot -U
```

编辑上一步生成的po文件，切记将charset=CHARSET改成charset=utf-8，将Content-Transfer-Encoding的值改为8bit，然后将对应的中文翻译赋值给msgstr，即只需要编辑3个地方

```po
# Chinese translations for i package.
# Copyright (C) 2018 THE i'S COPYRIGHT HOLDER
# This file is distributed under the same license as the i package.
# "" <anemone@desktop-anemone.localdomain>, 2018.
#
msgid ""
msgstr ""
"Project-Id-Version: i 18n_demo\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2018-03-11 15:04+0800\n"
"PO-Revision-Date: 2018-03-11 15:44+0800\n"
"Last-Translator: \"\" <anemone@desktop-anemone.localdomain>\n"
"Language-Team: Chinese (simplified)\n"
"Language: zh_CN\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
#: i18n_demo.py:14
msgid "This is a translatable string."
msgstr "这是翻译后的字符串"
```


# *Step 4: 创建mo文件
```bash
cd zh_CN/LC_MESSAGES
msgfmt -o i18n_demo.mo zh_CN.po    #mo的文件名与domain_name相同
```

# *Step 5: 设置环境变量，输出中文
```bash
export LANG=zh_CN.UTF-8 && python i18n_demo.py
```

**注：一个字符串中出现两个%格式化会出现问题（无法分辨位置）**

解决：
```python
my_string = "Hello %(person)s, it is %(time)s o'clock." % ({'person':'Foo', 'time':'two'})
```
