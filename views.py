#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import re
import textwrap
import requests
import unicodedata
from datetime import datetime, timedelta

from flask import Flask, g, request, render_template, abort, make_response
from flask_babel import Babel, gettext
from jinja2 import evalcontextfilter, Markup

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
LOGO_PYCON = 'logo/pycon_logo_square.svg'

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
    "image": DOMAIN + "/static/img/logo/pycon_long_2018.png",
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

# calendar settings
ICAL_LEN = 70  # length of a calendar (ical) line
ICAL_NL = '\\n\n'  # calendar newline
IGNORE_TALKS = ['Break', 'Coffee Break']

TYPE = {
    'talk': gettext('Talk'),
    'workshop': gettext('Workshop'),
}

TAGS = {
    'ai': gettext('Machine Learning / AI'),
    'community': gettext('Community / Diversity / Social'),
    'data': gettext('Data Science'),
    'devops': 'DevOps',
    'docs': gettext('Documentation'),
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
    {"pause": 5, 'title': gettext("Conference Opening"), 'duration': 25},
    {"pause": 5, 'title': gettext("When your wetware has too many threads - Tips from an ADHDer on how to improve your focus")},
    {"pause": 15, 'title': gettext("Docs or it didn't happen")},
    {"pause": 5, 'title': gettext("GraphQL is the new black")},
    {"pause": 60, 'title': gettext("To the Google in 80 Days")},
    {"pause": 5, 'title': gettext("Unsafe at Any Speed")},
    {"pause": 15, 'title': gettext("Protecting Privacy and Security — For Yourself and Your Community")},
    {"pause": 5, 'title': gettext("ZODB: The Graph database for Python Developers.")},
    {"pause": 15, 'title': gettext("Differentiable programming in Python and Gluon for (not only medical) image analysis")},
    {"pause": 5, 'title': gettext("Vim your Python, Python your Vim")},
    {"pause": 5, 'title': gettext("Quiz"), 'duration': 30, 'flag': 'other', 'type': 'talk'},
    {"pause": 5, 'title': gettext("Lightning Talks"), 'duration': 30, 'flag': 'other', 'type': 'talk'},
)

FRIDAY_TRACK2 = (
    {"pause": 5, 'title': gettext("Conference Opening in Kiwi.com Hall"), 'duration': 25},
    {"pause": 5, 'title': gettext("Python Days in Martin and follow-up activities")},
    {"pause": 15, 'title': gettext("Python programming till graduation")},
    {"pause": 5, 'title': gettext("Open educational resources for learning Python")},
    {"pause": 60, 'title': gettext("About Ninjas and Mentors: CoderDojo in Slovakia")},
    {"pause": 5, 'title': gettext("Community based courses")},
    {"pause": 15, 'title': gettext("How do we struggle with Python in Martin?")},
    {"pause": 5, 'title': gettext("Why hardware attracts kids and adults to IT")},
    {"pause": 15, 'title': gettext("EDU Talks"), 'duration': 30, 'language': 'SK', 'flag': 'edu', 'type': 'talk'},
    {"pause": 15, 'title': gettext("Panel discussion: Teaching IT in Slovakia - where is it heading?")},
)

FRIDAY_WORKSHOPS1 = (
    {"pause": 10, 'title': gettext("How to create interactive maps in Python / R")},
    {"pause": 60, 'title': gettext("Working with XML")},
    {"pause": 5, 'title': gettext("Managing high-available applications in production")},
)

FRIDAY_WORKSHOPS2 = (
    {"pause": 40, 'title': gettext("Workshop: An Introduction to Ansible")},
    {"pause": 5, 'title': gettext("Introduction to Machine Learning with Python")},
)

SATURDAY_TRACK1 = (
    {"pause": 5, 'title': gettext("Conference Opening"), 'duration': 25},
    {"pause": 5, 'title': gettext("Solutions Reviews")},
    {"pause": 15, 'title': gettext("Campaign Automation & Abusing Celery Properly")},
    {"pause": 5, 'title': gettext("The Truth about Mastering Big Data")},
    {"pause": 60, 'title': gettext("Industrial Machine Learning: Building scalable distributed machine learning pipelines with Python")},
    {"pause": 5, 'title': gettext("Pythonic code, by example")},
    {"pause": 15, 'title': gettext("Our DevOps journey, is SRE the next stop?")},
    {"pause": 5, 'title': gettext("Implementing distributed systems with Consul")},
    {"pause": 15, 'title': gettext("Designing fast and scalable Python MicroServices with django")},
    {"pause": 5, 'title': gettext("FaaS and Furious - Zero to Serverless in 60 seconds - Anywhere")},
    {"pause": 5, 'title': gettext("Programming Python as performance: live coding with FoxDot")},
    {"pause": 5, 'title': gettext("Programming Contest Finale"), 'duration': 30, 'flag': 'other', 'type': 'talk', 'language': 'EN'},
    {"pause": 5, 'title': gettext("Lightning Talks"), 'duration': 30, 'flag': 'other', 'type': 'talk'},
)

SATURDAY_TRACK2 = (
    {"pause": 5, 'title': gettext("Conference Opening in Kiwi.com Hall"), 'duration': 25},
    {"pause": 5, 'title': gettext("Meteo data in Python. Effectively.")},
    {"pause": 15, 'title': gettext("Around the World in 30 minutes")},
    {"pause": 5, 'title': gettext("LOCKED SHIELDS: What a good cyber testing looks like")},
    {"pause": 60, 'title': gettext("Kiwi.com in ZOO")},
    {"pause": 5, 'title': gettext("Keynote in Kiwi.com Hall"), 'duration': 30, 'flag': 'generic', 'type': 'talk'},
    {"pause": 15, 'title': gettext("Skynet your Infrastructure with QUADS")},
    {"pause": 5, 'title': gettext("Automated network OS testing")},
    {"pause": 15, 'title': gettext("Tools to interact with Bitcoin and Ethereum")},
    {"pause": 5, 'title': gettext("7 Steps to a Clean Issue Tracker")},
    {"pause": 5, 'title': gettext("The Concierge Paradigm")},
)

SATURDAY_WORKSHOPS1 = (
    {"pause": 55, 'title': gettext("Effectively running python applications in Kubernetes/OpenShift")},
    {"pause": 5, 'title': gettext("Roboworkshop")},
)
SATURDAY_WORKSHOPS2 = (
    {"pause": 55, 'title': gettext("Microbit:Slovakia")},
    {"pause": 5, 'title': gettext("Coding in Python: A high-school programming lesson")},
)

SATURDAY_HALLWAY = (
    {"pause": 0, 'title': gettext("Pandas documentation sprint"), 'duration': 360},
)

SUNDAY_TRACK1 = (
    {"pause": 5, 'title': gettext("Charon and the way out from a pickle hell")},
    {"pause": 15, 'title': gettext("Making Python Behave")},
    {"pause": 5, 'title': gettext("\"Secret\" information in code you write")},
    {"pause": 60, 'title': gettext("How to connect objects with each other in different situations with Pythonic ways - association, aggregation, composition and etc.")},
    {"pause": 5, 'title': gettext("APIs: Gateway to world's data")},
    {"pause": 15, 'title': gettext("Getting started with HDF5 and PyTables")},
    {"pause": 5, 'title': gettext("Real-time personalized recommendations using embeddings")},
)

SUNDAY_WORKSHOPS1 = (
    {"pause": 40, 'title': gettext("Real-time transcription and sentiment analysis of audio streams; on the phone and in the browser")},
    {"pause": 5, 'title': gettext("Learn MongoDB by modeling PyPI in a document database")},
)

SUNDAY_WORKSHOPS2 = (
    {"pause": 15, 'title': gettext("Testing Essentials for Scientists and Engineers")},
    {"pause": 5, 'title': gettext("Cython: Speed up your code without going insane")},
)

SUNDAY_WORKSHOPS3 = (
    {"pause": 15, 'title': gettext("Meet the pandas")},
    {"pause": 5, 'title': gettext("Serverless with OpenFaaS and Python")},
)

SUNDAY_WORKSHOPS4 = (
    {"pause": 5, 'title': gettext("Django Girls"), 'duration': 520, 'flag': 'web', 'type': 'workshop'},
)

AULA1 = {
    'name': gettext('Kiwi.com Hall'),
    'number': '-1.61',
}
AULA2 = {
    'name': gettext('Python Software Foundation Hall'),
    'number': '-1.65',
}

AULA3 = {
    'name': gettext('SPy - Hall A'),
    'number': '-1.57',
}

AULA4 = {
    'name': gettext('SPy - Hall B'),
    'number': '-1.57',
}

AULA5 = {
    'name': gettext('Django Girls Auditorium'),
    'number': '+1.31',
}

HALLWAY = {
    'name': gettext('Hallway'),
    'number': '',
}


def get_conference_data(url='', filters=''):
    """Connect to API and get public talks and speakers data."""
    url = API_DOMAIN + url

    if filters:
        url = url + '&' + filters

    r = requests.get(url)
    return r.json()


API_DATA_SPEAKERS = get_conference_data(url='/event/2018/speakers/')
API_DATA_TALKS = get_conference_data(url='/event/2018/talks/')


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

        start = start + timedelta(minutes=talk_api_data.get('duration', 0))
        # start = start + timedelta(minutes=talk_api_data['duration'])

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
            'day': 'friday',
            'block_start': True,
        },
        {
            'room': AULA2,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_TRACK2, FRIDAY_START, flag=flag),
            'day': 'friday'
        },
        {
            'room': AULA3,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_WORKSHOPS1, FRIDAY_START+timedelta(minutes=30), flag=flag),
            'day': 'friday'
        },
        {
            'room': AULA4,
            'start': FRIDAY_START,
            'schedule': generate_track(api_data, FRIDAY_WORKSHOPS2, FRIDAY_START+timedelta(minutes=30), flag=flag),
            'day': 'friday',
            'block_end': True,
        },
        {
            'room': AULA1,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_TRACK1, SATURDAY_START, flag=flag),
            'day': 'saturday',
            'block_start': True,
        },
        {
            'room': AULA2,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_TRACK2, SATURDAY_START, flag=flag),
            'day': 'saturday'
        },
        {
            'room': AULA3,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_WORKSHOPS1, SATURDAY_START+timedelta(minutes=30), flag=flag),
            'day': 'saturday'
        },
        {
            'room': AULA4,
            'start': SATURDAY_START,
            'schedule': generate_track(api_data, SATURDAY_WORKSHOPS2, SATURDAY_START+timedelta(minutes=30), flag=flag),
            'day': 'saturday'
        },
        {
            'room': HALLWAY,
            'start': SATURDAY_START+timedelta(minutes=60),
            'schedule': generate_track(api_data, SATURDAY_HALLWAY, SATURDAY_START+timedelta(minutes=60), flag=flag),
            'day': 'saturday',
            'block_end': True,
        },
        {
            'room': AULA1,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_TRACK1, SUNDAY_START, flag=flag),
            'day': 'sunday',
            'block_start': True,
        },
        {
            'room': AULA2,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS1, SUNDAY_START, flag=flag),
            'day': 'sunday'
        },
        {
            'room': AULA3,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS2, SUNDAY_START, flag=flag),
            'day': 'sunday'
        },
        {
            'room': AULA4,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS3, SUNDAY_START, flag=flag),
            'day': 'sunday'
        },
        {
            'room': AULA5,
            'start': SUNDAY_START,
            'schedule': generate_track(api_data, SUNDAY_WORKSHOPS4, SUNDAY_START-timedelta(minutes=90), flag=flag),
            'day': 'sunday',
            'block_end': True,
        },
    ]


def _timestamp(dt=None):
    if dt is None:
        dt = datetime.now()
    fmt = '%Y%m%dT%H%M%S'
    return dt.strftime(fmt)


def _ignore_talk(title, names=IGNORE_TALKS):
    # yes, we can paste unicode symbols, but if we change the symbol this test will still work
    max_appended_symbols = 2
    return any((title == name or title[:-(_len+1)] == name)
               for _len in range(max_appended_symbols) for name in names)


def _hash_event(track, slot):
    room = track.get('room')
    name = room.get('name')
    ts = _timestamp(slot.get('start'))
    _hash = str(hash('{name}:{ts}'.format(name=name, ts=ts)))
    _hash = _hash.replace('-', '*')
    return '-'.join(_hash[i*5:(i+1)*5] for i in range(4))


def _normalize(text, tag=None, subsequent_indent=' ', **kwargs):
    # tag must be always included to determine amount of space left in the first line
    if tag:
        max_width = ICAL_LEN - len(tag) - 1
    else:
        max_width = ICAL_LEN

    text = text.strip().replace('\n', ICAL_NL)

    return '\n'.join(textwrap.wrap(text, width=max_width, subsequent_indent=subsequent_indent, **kwargs))


# CALENDAR FUNCTIONS
def generate_event(track, slot):
    room = track.get('room')
    location = '{name} ({number})'.format(**room)
    talk = slot.get('talk')
    summary = talk.get('title', 'N/A')
    transp = 'OPAQUE'
    if _ignore_talk(summary):
        # skip breaks
        # alternatively we can include breaks into talks (duration=duration+pause)
        return {}
    summary = _normalize(summary, 'SUMMARY')
    start = slot.get('start')
    duration = talk.get('duration', 0)
    # TODO add missing duration handling (nonzero default duration? title based dictionary?
    dtend = _timestamp(start + timedelta(minutes=duration))
    dtstart = _timestamp(start)
    dtstamp = created = modified = _timestamp()
    # event_uuid caused the event not to be imported to calendar
    # this creates hash of name:start and split with dashes by 5
    uid = _hash_event(track, slot)

    author = ''
    main_description = ''
    tags = ''
    speaker = talk.get('primary_speaker')
    if speaker:
        name = ' '.join([speaker.get(n, '') for n in ['first_name', 'last_name']])
        author = '{name}{nl} {nl}'.format(name=name, nl=ICAL_NL)
    # this is to determine how many chars do we have in the first line
    # if author is used we start at position 1, otherwise it will be prefixed with tag:
    desc_tag = 'DESCRIPTION' if not author else ''
    abstract = talk.get('abstract', '')
    if abstract:
        main_description = _normalize(abstract, desc_tag, initial_indent=' ') + ICAL_NL
    if 'flag' in talk:
        tags = ' {nl} TAGS: {flag}'.format(nl=ICAL_NL, **talk)
    description = author + main_description + tags

    status = 'CONFIRMED'
    sequence = 0  # number of revisions, we will use default zero even if event changed

    return {'dtstart': dtstart, 'dtend': dtend, 'dtstamp': dtstamp, 'created': created,
            'last-modified': modified, 'uid': uid, 'location': location, 'sequence': sequence,
            'description': description, 'status': status, 'summary': summary, 'transp': transp, }


@app.route('/<lang_code>/calendar.ics')
def generate_ics():
    # https://tools.ietf.org/html/rfc5545#section-2.1
    # https://en.wikipedia.org/wiki/ICalendar#Technical_specifications
    omni_schedule = generate_schedule(API_DATA_TALKS)

    events = []
    uids = set()

    for track in omni_schedule:
        schedule = track.get('schedule')
        for slot in schedule:
            evt = generate_event(track, slot)
            if evt and evt.get('uid') not in uids:
                events.append(evt)
                uids.update([evt.get('uid')])

    calendar_ics = render_template('calendar.ics', events=events)
    response = make_response(calendar_ics.replace('\n', '\r\n'))
    response.headers["Content-Type"] = "text/calendar"

    return response


@app.route('/<lang_code>/index.html')
def index():
    return render_template('index.html', **_get_template_variables(li_index='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    return render_template('tickets.html', **_get_template_variables(li_tickets='active'))


@app.route('/<lang_code>/<flag>/<day>/schedule.html')
def schedule_day_filter(flag, day):
    variables = _get_template_variables(li_schedule_nav='active', li_schedule='active')
    variables['flag'] = flag
    variables['day'] = day
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = api_data = API_DATA_TALKS
    variables['schedule'] = generate_schedule(api_data, flag=flag)

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/<filter>/schedule.html')
def schedule_filter(filter):
    variables = _get_template_variables(li_schedule_nav='active', li_schedule='active')
    if filter in ('friday', 'saturday', 'sunday'):
        variables['day'] = filter
        variables['flag'] = None
    else:
        variables['flag'] = filter
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = api_data = API_DATA_TALKS
    variables['schedule'] = generate_schedule(api_data, flag=variables['flag'])

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/schedule.html')
def schedule():
    variables = _get_template_variables(li_schedule_nav='active', li_schedule='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = api_data = API_DATA_TALKS
    variables['schedule'] = generate_schedule(api_data)
    variables['disable_last'] = True

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/<flag>/talks.html')
def talks_filter(flag):
    variables = _get_template_variables(li_schedule_nav='active', li_talks='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = get_conference_data(url='/event/2018/talks/?flag=' + flag)

    return render_template('talks.html', **variables)


@app.route('/<lang_code>/talks.html')
def talks():
    variables = _get_template_variables(li_schedule_nav='active', li_talks='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}
    variables['data'] = API_DATA_TALKS

    return render_template('talks.html', **variables)


@app.route('/<lang_code>/speakers.html')
def speakers():
    variables = _get_template_variables(li_schedule_nav='active', li_speakers='active')
    variables['data'] = API_DATA_SPEAKERS
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}

    return render_template('speakers.html', **variables)


@app.route('/<lang_code>/speakers/<last_name>.html')
def profile(last_name):
    variables = _get_template_variables(li_schedule_nav='active')
    variables['tags'] = TAGS
    variables['all'] = {**TYPE, **TAGS}

    for speaker in API_DATA_SPEAKERS:
        if speaker['last_name'] == last_name:
            variables['speaker'] = speaker
            break

    variables['talks'] = []

    for track in generate_schedule(API_DATA_TALKS):
        for talk in track['schedule']:
            if ('primary_speaker' in talk['talk'] or 'secondary_speaker' in talk['talk']) and \
                    talk['talk']['primary_speaker']['last_name'] == variables['speaker']['last_name'] or (
                    'secondary_speaker' in talk['talk'] and
                    talk['talk']['secondary_speaker']['last_name'] == variables['speaker']['last_name']):
                variables['talks'].append((track, talk))
                break

    return render_template('profile.html', **variables)


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
