#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import locales.i18n as i18n
#  print locales.i18n
_ = i18n.ugettext('i18n_demo')


def i18n(n=1):
    if n == 1:
        return _('This is a translatable string.')
    else:
        return _('This is a translatable string2.')


if __name__ == '__main__':
    print repr(i18n())
    print type(i18n())
    print i18n()
