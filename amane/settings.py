#-*- coding: utf-8 -*-

import global_settings
import local_settings
import copy

SITE_LIST = []
if hasattr(local_settings, 'SITE_LIST'):
    SITE_LIST += local_settings.SITE_LIST
if hasattr(global_settings, 'SITE_LIST'):
    SITE_LIST += global_settings.SITE_LIST
