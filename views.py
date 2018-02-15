#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import re
import requests
import unicodedata
from datetime import datetime, timedelta
from operator import itemgetter
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

TYPE = {
    'talk': gettext('Talk'),
    'workshop': gettext('Workshop'),
}

TAGS = {
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

FRIDAY_START = datetime(2018, 3, 9, hour=9)
SATURDAY_START = datetime(2018, 3, 10, hour=9)
SUNDAY_START = datetime(2018, 3, 11, hour=10, minute=15)

FRIDAY_TRACK1 = (
    {"pause": 5, 'title': "Conference Opening", 'duration': 25},
    {"pause": 5, 'title': "When your wetware has too many threads - Tips from an ADHDer on how to improve your focus"},
    {"pause": 15, 'title': "Docs or it didn't happen"},
    {"pause": 5, 'title': "GraphQL is the new black"},
    {"pause": 60, 'title': "To the Google in 80 Days"},
    {"pause": 5, 'title': "The Concierge Paradigm"},
    {"pause": 15, 'title': "Skynet your Infrastructure with QUADS"},
    {"pause": 5, 'title': "The Z Object Database"},
    {"pause": 15, 'title': "Differentiable programming in Python and Gluon for (not only medical) image analysis"},
    {"pause": 5, 'title': "Vim your Python, Python your Vim"},
    {"pause": 5, 'title': "Protecting Privacy and Security — For Yourself and Your Community"},
    {"pause": 5, 'title': "Lightning Talks", 'duration': 30, 'flag': 'other', 'type': 'talk'},
)

FRIDAY_TRACK2 = (
    {"pause": 5, 'title': "Conference Opening in Kiwi.com Hall", 'duration': 25},
    {"pause": 5, 'title': "Konferencia Python Days v Martine a následné aktivity"},
    {"pause": 15, 'title': "Programujeme v Pythone až k maturite"},
    {"pause": 5, 'title': "Otvorené vzdelávacie zdroje pre štúdium jazyka Python"},
    {"pause": 60, 'title': "O nindžoch a mentoroch: CoderDojo na Slovensku"},
    {"pause": 5, 'title': "Komunitní kurzy"},
    {"pause": 15, 'title': "Ako sa pasujeme s Pythonom v Martine?"},
    {"pause": 5, 'title': "Prečo hardvér priťahuje k informatike žiakov i dospelých"},
    {"pause": 15, 'title': "EDU TALKS", 'duration': 30, 'language': 'SK', 'flag': 'edu', 'type': 'talk'},
    {"pause": 15, 'title': "Panel Discussion", 'duration': 65, 'language': 'SK', 'flag': 'edu', 'type': 'talk'},
)

FRIDAY_WORKSHOPS1 = (
    {"pause": 10, 'title': "Ako vytvárať interaktívne mapy v Python / R"},
    {"pause": 60, 'title': "Práce s XML"},
    {"pause": 5, 'title': "Managing high-available applications in production"},
)

FRIDAY_WORKSHOPS2 = (
    {"pause": 40, 'title': "Základy Ansible Workshop"},
    {"pause": 5, 'title': "Introduction to Machine Learning with Python"},
)

SATURDAY_TRACK1 = (
    {"pause": 5, 'title': "Conference Opening", 'duration': 25},
    {"pause": 5, 'title': "Solutions Reviews"},
    {"pause": 15, 'title': "Campaign Automation & Abusing Celery Properly"},
    {"pause": 5, 'title': "Search Engines with Python and Elasticsearch"},
    {"pause": 60, 'title': "Industrial Machine Learning: Building scalable distributed machine learning pipelines with Python"},
    {"pause": 5, 'title': "Pythonic code, by example"},
    {"pause": 15, 'title': "Our DevOps journey, is SRE the next stop?"},
    {"pause": 5, 'title': "Maintaining reliable and secure continuous delivery for python microservices"},
    {"pause": 15, 'title': "Designing fast and scalable Python MicroServices with django"},
    {"pause": 5, 'title': "FaaS and Furious - Zero to Serverless in 60 seconds - Anywhere"},
    {"pause": 5, 'title': "Programming Python as performance: live coding with FoxDot"},
    {"pause": 5, 'title': "Lightning Talks", 'duration': 30, 'flag': 'other', 'type': 'talk'},
)

SATURDAY_TRACK2 = (
    {"pause": 5, 'title': "Conference Opening in Kiwi.com Hall", 'duration': 25},
    {"pause": 5, 'title': "Meteodáta v Pythone. Efektívne."},
    {"pause": 15, 'title': "Cesta kolem světa za 30 minut"},
    {"pause": 5, 'title': "LOCKED SHIELDS - ako má vypadať dobre urobené kybertestovanie"},
    {"pause": 60, 'title': "Kiwi.com v ZOO"},
    {"pause": 5, 'title': "Keynote in Kiwi.com Hall", 'duration': 30, 'flag': 'generic', 'type': 'talk'},
    {"pause": 15, 'title': "TBD", 'duration': 30, 'flag': 'other', 'type': 'talk'},
    {"pause": 5, 'title': "Automated network OS testing"},
    {"pause": 15, 'title': "Tools to interact with Bitcoin and Ethereum"},
    {"pause": 5, 'title': "Unsafe at Any Speed"},
    {"pause": 5, 'title': "7 Steps to a Clean Issue Tracker"},
)

SATURDAY_WORKSHOPS1 = (
    {"pause": 40, 'title': "Effectively running python applications in Kubernetes/OpenShift"},
    {"pause": 5, 'title': "Roboworkshop"},
)
SATURDAY_WORKSHOPS2 = (
    {"pause": 40, 'title': "Microbit:Slovensko"},
    {"pause": 5, 'title': "Programujeme v Pythone – učíme seminár z programovania na strednej škole"},
)

SUNDAY_TRACK1 = (
    {"pause": 5, 'title': "Charon a cesta z pickle pekla"},
    {"pause": 15, 'title': "Making Python Behave"},
    {"pause": 5, 'title': "\"Utajené\" informácie o kóde ktorý píšeš", 'duration': 30},
    {"pause": 60, 'title': "How to connect objects with each other in different situations with Pythonic ways - association, aggregation, composition and etc."},
    {"pause": 5, 'title': "Getting started with HDF5 and PyTables"},
    {"pause": 15, 'title': "The Truth about Mastering Big Data"},
    {"pause": 5, 'title': "Real-time personalized recommendations using embeddings"},
)

SUNDAY_WORKSHOPS1 = (
    {"pause": 40, 'title': "Real-time transcription and sentiment analysis of audio streams; on the phone and in the browser"},
    {"pause": 5, 'title': "Learn MongoDB by modeling PyPI in a document database"},
)

SUNDAY_WORKSHOPS2 = (
    {"pause": 15, 'title': "Testing Essentials for Scientists and Engineers"},
    {"pause": 5, 'title': "Cython: Speed up your code without going insane"},
)

SUNDAY_WORKSHOPS3 = (
    {"pause": 5, 'title': "TBD", 'duration': 180, 'flag': 'devops', 'type': 'workshop'},
    {"pause": 5, 'title': "TBD", 'duration': 180, 'flag': 'data', 'type': 'workshop'},
)

SUNDAY_WORKSHOPS4 = (
    {"pause": 5, 'title': "Django Girls", 'duration': 520, 'flag': 'web', 'type': 'workshop'},
)

AULA1 = {
    'name': gettext('Kiwi.com Hall'),
    'number': '-1.61',
}
AULA2 = {
    'name': gettext('Python Software Foundation Hall'),
    'number': '-1.60',
}

AULA3 = {
    'name': gettext('Babbage Hall 1/2'),
    'number': '-1.57',
}

AULA4 = {
    'name': gettext('Babbage Hall 2/2'),
    'number': '-1.57',
}

AULA5 = {
    'name': gettext('Jobs Auditorium'),
    'number': '1.XX',
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


def generate_track(api_data, track_data, start, flag=None):
    """Helper function to mix'n'match API data, with schedule order defined here, to generate schedule dict"""
    template_track_data = []

    for talk in track_data:

        # Check if talk is in API
        talk_api_data = next((item for item in api_data if item['title'] == talk['title']), None)

        # If talk is not in API data we'll use text from track_data dict == same structure for template generation
        if not talk_api_data:
            talk_api_data = talk

        if not flag or ('flag' in talk_api_data and flag == talk_api_data['flag']):

            # Store data to be displayed in template
            template_track_data.append({
                "start": start,
                "talk": talk_api_data
            })

        start = start + timedelta(minutes=talk_api_data['duration'])

        if not flag:
            # Generate break
            break_name = gettext('Break')

            if talk['pause'] in (40, 60):
                break_name = gettext('Lunch 🍱')

            if talk['pause'] in (15, ):
                break_name = gettext('Coffee Break ☕')

            template_track_data.append({
                'start': start,
                'talk': {'title': break_name},
                'css': 'break'
            })

        start = start + timedelta(minutes=talk['pause'])  # break time does not comes from API always defined in track

    return template_track_data


def generate_schedule(api_data, flag=None):
    return [
        {
            'room': AULA1,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_TRACK1, FRIDAY_START, flag=flag),
        },
        {
            'room': AULA2,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_TRACK2, FRIDAY_START, flag=flag),
        },
        {
            'room': AULA3,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_WORKSHOPS1, FRIDAY_START+timedelta(minutes=30), flag=flag),
        },
        {
            'room': AULA4,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_WORKSHOPS2, FRIDAY_START+timedelta(minutes=30), flag=flag),
        },
        {
            'room': AULA1,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_TRACK1, SATURDAY_START, flag=flag),
        },
        {
            'room': AULA2,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_TRACK2, SATURDAY_START, flag=flag),
        },
        {
            'room': AULA3,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_WORKSHOPS1, SATURDAY_START+timedelta(minutes=30), flag=flag),
        },
        {
            'room': AULA4,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_WORKSHOPS2, SATURDAY_START+timedelta(minutes=30), flag=flag),
        },
        {
            'room': AULA1,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_TRACK1, SUNDAY_START, flag=flag),
        },
        {
            'room': AULA2,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS1, SUNDAY_START, flag=flag),
        },
        {
            'room': AULA3,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS2, SUNDAY_START, flag=flag),
        },
        {
            'room': AULA4,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS3, SUNDAY_START, flag=flag),
        },
        {
            'room': AULA5,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS4, SUNDAY_START-timedelta(minutes=90), flag=flag),
        },
    ]


@app.route('/<lang_code>/index.html')
def index():
    return render_template('index.html', **_get_template_variables(li_index='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/<flag>/schedule.html')
def schedule_filter(flag):
    variables = _get_template_variables(li_schedule='active')
    variables['flag'] = flag
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = api_data = get_conference_data(url='/event/2018/talks/')
    variables['schedule'] = generate_schedule(api_data, flag=flag)

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/schedule.html')
def schedule():
    variables = _get_template_variables(li_schedule='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = api_data = get_conference_data(url='/event/2018/talks/')
    variables['schedule'] = generate_schedule(api_data)
    variables['disable_last'] = True

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/<flag>/talks.html')
def talks_filter(flag):
    variables = _get_template_variables(li_schedule='active', li_talks='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = get_conference_data(url='/event/2018/talks/?flag=' + flag)

    return render_template('talks.html', **variables)


@app.route('/<lang_code>/talks.html')
def talks():
    variables = _get_template_variables(li_schedule='active', li_talks='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = get_conference_data(url='/event/2018/talks/')

    return render_template('talks.html', **variables)


@app.route('/<lang_code>/speakers.html')
def speakers():
    variables = _get_template_variables(li_speakers='active')
    variables['data'] = get_conference_data(url='/event/2018/speakers/')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}

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
