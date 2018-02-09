#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import re
import requests
import unicodedata
from operator import itemgetter
from datetime import datetime
from flask import Flask, g, request, render_template, abort, make_response
from flask_babel import Babel, gettext
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__, static_url_path='/static')
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)

EVENT = gettext('PyCon SK 2018')
DOMAIN = 'https://2018.pycon.sk'
API_DOMAIN = 'https://api.pycon.sk'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'
NOW = datetime.utcnow().strftime(TIME_FORMAT)

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOGO_PYCON = 'logo/spy-logo.svg'

LDJSON_SPY = {
    "@type": "Organization",
    "name": "SPy o. z.",
    "url": "https://spy.pycon.sk",
    "logo": "https://spy.pycon.sk/img/logo/spy-logo.png",
    "sameAs": [
        "https://facebook.com/pyconsk",
        "https://twitter.com/pyconsk",
        "https://www.linkedin.com/company/spy-o--z-",
        "https://github.com/pyconsk",
    ]
}

LDJSON_PYCON = {
    "@context": "http://schema.org",
    "@type": "Event",
    "name": EVENT,
    "description": gettext("PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference "
                           "for the Python programming language."),
    "startDate": "2018-03-09T9:00:00+01:00",
    "endDate": "2018-03-11T18:00:00+01:00",
    "image": DOMAIN + "/static/img/backgrounds/lecture_hall.jpg",
    "location": {
        "@type": "Place",
        "name": "FIIT STU",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Ilkovičova 2",
            "addressLocality": "Bratislava 4",
            "postalCode": "842 16",
            "addressCountry": gettext("Slovak Republic")
        },
    },
    "url": DOMAIN,
    "workPerformed": {
        "@type": "CreativeWork",
        "name": EVENT,
        "creator": LDJSON_SPY
    }
}


TAGS = {
    'talk': gettext('Talk'),
    'workshop': gettext('Workshop'),
    'ai': gettext('Machine Learning / AI'),
    'community': gettext('Community / Diversity / Social'),
    'data': gettext('Data Science'),
    'devops': 'DevOps',
    'edu': gettext('Education'),
    'generic': gettext('Python General'),
    'security': gettext('Security'),
    'softskills': gettext('Soft Skills'),
    'hardware': gettext('Hardware'),
    'web': gettext('Web Development'),
    'other': gettext('Other'),
}


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        if request.view_args['lang_code'] not in LANGS:
            return abort(404)
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. The best match wins.
    # return request.accept_languages.best_match(['de', 'sk', 'en'])
    return g.get('current_lang', app.config['BABEL_DEFAULT_LOCALE'])


@app.template_filter()
@evalcontextfilter
def linebreaks(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@app.template_filter()
@evalcontextfilter
def linebreaksbr(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'%s' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@app.template_filter()
@evalcontextfilter
def strip_accents(eval_ctx, value):
    """Strip non ASCII characters and convert them to ASCII."""
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode("utf-8")


def get_conference_data(url='', filters=''):
    """Connect to API and get public talks and speakers data."""
    url = API_DOMAIN + url

    if filters:
        url = url + '&' + filters

    r = requests.get(url)
    return r.json()


def _get_template_variables(**kwargs):
    """Collect variables for template that repeats, e.g. are in body.html template"""
    lang = get_locale()
    variables = {
        'title': EVENT,
        'logo': LOGO_PYCON,  # TODO: Do we need this?
        'ld_json': LDJSON_PYCON
    }
    variables['ld_json']['url'] = DOMAIN + '/' + lang + '/'
    variables.update(kwargs)

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

    return variables


@app.route('/<lang_code>/index.html')
def index():
    return render_template('index.html', **_get_template_variables(li_index='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/schedule.html')
def schedule():
    variables = _get_template_variables(li_schedule='active')
    variables['data'] = get_conference_data(url='/event/2018/talks/')
    variables['tags'] = TAGS

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/speakers.html')
def speakers():
    variables = _get_template_variables(li_speakers='active')
    variables['data'] = get_conference_data(url='/event/2018/speakers/')
    variables['tags'] = TAGS

    return render_template('speakers.html', **variables)


@app.route('/<lang_code>/cfp.html')
def cfp():
    return render_template('cfp.html', **_get_template_variables(li_cfp='active'))


@app.route('/<lang_code>/coc.html')
def coc():
    return render_template('coc.html', **_get_template_variables(li_coc='active'))


@app.route('/<lang_code>/hall-of-fame.html')
def hall_of_fame():
    return render_template('hall-of-fame.html', **_get_template_variables(li_hall_of_fame='active'))


@app.route('/<lang_code>/venue.html')
def venue():
    return render_template('venue.html', **_get_template_variables(li_venue='active'))


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    return render_template('sponsoring.html', **_get_template_variables(li_sponsoring='active'))


def get_mtime(filename):
    """Get last modification time from file"""
    mtime = datetime.fromtimestamp(os.path.getmtime(filename))
    return mtime.strftime(TIME_FORMAT)


SITEMAP_DEFAULT = {'prio': '0.1', 'freq': 'weekly'}
SITEMAP = {
    'sitemap.xml': {'prio': '0.9', 'freq': 'daily', 'lastmod': get_mtime(__file__)},
    'index.html': {'prio': '1', 'freq': 'daily'},
    'schedule.html': {'prio': '0.9', 'freq': 'daily'},
    'speakers.html': {'prio': '0.9', 'freq': 'daily'},
    'hall_of_fame.html': {'prio': '0.5', 'freq': 'weekly'},
    'tickets.html': {'prio': '0.5', 'freq': 'weekly'},

}


def get_lastmod(route, sitemap_entry):
    """Used by sitemap() below"""
    if 'lastmod' in sitemap_entry:
        return sitemap_entry['lastmod']

    template = route.rule.split('/')[-1]
    template_file = os.path.join(SRC_DIR, 'templates', template)

    if os.path.exists(template_file):
        return get_mtime(template_file)

    return NOW


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []

    # static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            if len(rule.arguments) == 0:
                indx = rule.rule.replace('/', '')
                sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                pages.append({
                    'loc': DOMAIN + rule.rule,
                    'lastmod': get_lastmod(rule, sitemap_data),
                    'freq': sitemap_data['freq'],
                    'prio': sitemap_data['prio'],
                })

            elif 'lang_code' in rule.arguments:
                indx = rule.rule.replace('/<lang_code>/', '')

                for lang in LANGS:
                    alternate = []

                    for alt_lang in LANGS:
                        if alt_lang != lang:
                            alternate.append({
                                'lang': alt_lang,
                                'url': DOMAIN + rule.rule.replace('<lang_code>', alt_lang)
                            })

                    sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                    pages.append({
                        'loc': DOMAIN + rule.rule.replace('<lang_code>', lang),
                        'alternate': alternate,
                        'lastmod': get_lastmod(rule, sitemap_data),
                        'freq': sitemap_data['freq'],
                        'prio': sitemap_data['prio'],
                    })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "text/xml"

    return response


if __name__ == "__main__":
    app.run(debug=True, host=os.environ.get('FLASK_HOST', '127.0.0.1'), port=int(os.environ.get('FLASK_PORT', 5000)),
            use_reloader=True)
