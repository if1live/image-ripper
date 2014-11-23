#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from importd import d
import os
import rippers
import settings

d(
    DEBUG=True,
    INSTALLED_APPS=(
        # external library
        'django_nose',

        # my applications
        'rippers',
    ),
    # django-nose
    TEST_RUNNER='django_nose.NoseTestSuiteRunner',
)

@d('/')
def view_index(request):
    if request.method == 'POST':
        return dispatch_url(request)
    else:
        return d.render_to_response('index.jinja2')

def dispatch_url(request):
    url = request.POST['url']
    site_name = rippers.site_detector.detect(url)
    print('site : %s' % (site_name,))
    site_mod = rippers.get_site_module(site_name)
    return site_mod.handle_url(url)

if __name__ == '__main__':
    for site_mod_path in settings.SITE_LIST:
        rippers.register_site(site_mod_path)

    d.main()
