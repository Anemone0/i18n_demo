#!/usr/bin/env python
# coding=utf-8

# @file i18n.py
# @brief i18n
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2018-03-13 13:50

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


def ugettext(domain_name):
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    try:
        t = gt.translation(domain_name, language_dir)
    except IOError:
        return gettext(domain_name)
    return t.ugettext


if __name__ == '__main__':
    lgettext('test')
    gettext('test')
