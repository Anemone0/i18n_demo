#!/usr/bin/env python
# -*- coding: utf-8 -*-


import locales.i18n as i18n

_ = i18n.ugettext('i18n_demo')


def i18n(n=1):
    if n == 1:
        return _('This is a translatable string3.')
    else:
        return _('This is a translatable string4.')


if __name__ == '__main__':
    print i18n()
