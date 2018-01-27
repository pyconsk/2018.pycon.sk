#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from datetime import datetime
from flask import Flask, g, request, render_template, abort, make_response
from flask_babel import Babel, gettext

app = Flask(__name__, static_url_path='/static')
app.config['BABEL_DEFAULT_LOCALE'] = 'sk'
app.jinja_options = {'extensions': ['jinja2.ext.with_', 'jinja2.ext.i18n']}
babel = Babel(app)

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOGO_PYCON = 'logo/pycon.svg'

LANGS = ('en', 'sk')
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'
NOW = datetime.utcnow().strftime(TIME_FORMAT)


def get_mtime(filename):
    mtime = datetime.fromtimestamp(os.path.getmtime(filename))
    return mtime.strftime(TIME_FORMAT)


SITEMAP_DEFAULT = {'prio': '0.1', 'freq': 'weekly'}
SITEMAP = {
    'sitemap.xml': {'prio': '0.9', 'freq': 'daily', 'lastmod': get_mtime(__file__)},
    'index.html': {'prio': '1', 'freq': 'daily'},
}
LDJSON = {
    "@context": "http://schema.org",
    "@type": "Organization",
    "name": "PyCon SK",
    "url": "https://2018.pycon.sk",
    "logo": "https://2018.pycon.sk/static/logo/pycon.png",
    "sameAs": [
        "https://facebook.com/pyconsk",
        "https://twitter.com/pyconsk",
        "https://www.linkedin.com/company/spy-o--z-",
        "https://github.com/pyconsk",
    ]
}

DATA = (
    {
        'name': 'Mikey Ariel',
        'bio': gettext('You might know her as That Docs Lady, and you won\'t be wrong! Mikey spent the better part of '
                       'the last 10 years documenting super-geeky enterprise software, most recently for OpenStack '
                       'Platform at Red Hat. She is also a community lead for Write the Docs, Django Girls alumni, and '
                       'documentation coach for open-source projects.<br />'
                       'Since crash-landing on open-source planet in 2013, Mikey presented talks and wrote articles '
                       'about docs, DevOps, and community. She also runs documentation workshops, hackfests, and '
                       'sprints at developer events, primarily for the Python and Django communities but also Fedora, '
                       'Plone, KDE, and NixOS.'),
        'country': 'CZ',
        'url': 'http://docsideofthemoon.com/',
        'avatar': 'img/speakers/mikey_ariel.jpg',
        'talk': gettext('Docs or it didn\'t happen'),
        'tag': 'other',
        'abstract': gettext('<p>If you ever skimmed through a README, tried to follow a quickstart tutorial, '
                            'attempted to decipher an error message, or typed \'--help\' in your terminal, '
                            'congratulations -- you have encountered documentation!</p>'
                            '<p>Long gone are the days of massive books with never-ending stories about your '
                            'software. Today\'s users are smarter and less patient, which means that we no longer '
                            'need to document *all the things*, as long as what we do document is clear, concise, '
                            'helpful, and accessible. And that\'s where the real work starts.</p>'
                            '<p>Documentation requires some attitude adjustment, since prose doesn\'t neatly '
                            'compile into binaries as code does. But Don\'t Panic(tm)! No matter what your role is '
                            'in the community, you can apply a few key principles from the technical writing world '
                            'to make your project more docs-friendly, and therefore more user- and '
                            'contributor-friendly.</p>'
                            '<p>This high-level (and all-level) talk aims to introduce or re-acquaint you with '
                            'topics such as content strategy, docs-as-code, optimized DevOps for docs, and '
                            'contribution workflows. Open-source projects of all shapes, ages, sizes are '
                            'welcome!</p>'),

    },
    {
        'name': 'Gareth Brown',
        'bio': gettext('Gareth has been working with DevOps organisations and DevOps tools like monitoring systems for '
                       'over 13 years. Gareth would like to share his experience of running containers in production '
                       'from the early days to scaling and operating in cloud environments. The pains and strains of '
                       'previous decisions and our successes with The Autopilot Pattern and ultimately developing the '
                       'Concierge Paradigm to drastically simplify containers at scale.'),
        'country': 'UK',
        'url': 'http://www.mesoform.com',
        'avatar': 'img/speakers/no_avatar.svg',
        'talk': gettext('The Concierge Paradigm'),
        'tag': 'devops',
        'abstract': gettext('<p>The Concierge Paradigm idea was born over time but initially came from challenges '
                            'we had by working out how to operate scalable and enterprise-grade application '
                            'containers. This meant monitoring, logging, deploying, scaling, load-balancing and '
                            'service discovery. We needed to do this both on-premise and in AWS. We were running '
                            'some docker tasks in ECS and a Kubernetes and CoreOS cluster on-premise but we hadn\'t'
                            ' chosen these by researching different options, they were pretty much the first '
                            'options we came across. We\'d felt the difficulties of our decision, so started to '
                            'look out to the wider community at other options.</p>'
                            '<p>This is the story of what we discovered. How we made our application monitoring '
                            'more efficient and accurate; how we radically simplified the infrastructure needed for'
                            ' running containers and how we utilised Zabbix as an container scheduler.</p>'),

    },
    {
        'name': 'Peter Garaj',
        'bio': gettext('I was paid to kill people. I quit the job.'),
        'country': 'SK',
        'url': '#',
        'avatar': 'img/speakers/no_avatar.svg',
        'talk': 'LOCKED SHIELDS - ako má vypadať dobre urobené kybertestovanie',
        'tag': 'security',
        'abstract': gettext('<p>Cvičenie LOCKED SHIELDS je organizované Centrom výnimočnosti pre oblasť kybernetickej '
                            'obrany (CCD CoE). Jedným s jeho počinov je cvičenie LOCKED SHIELDS, ktoré je svojou '
                            'veľkosťou, rozsiahlosťou a zameraním jedným s najunikátnejších kybercvičení na svete.</p>'
                            '<p>Ako človek, ktorý sa tohto každoročného cvičenia sporadicky zúčastňuje by som rád '
                            'povedal niečo o tom, ako to vypadá zvnútra a ako sa slovenská vojenská kybernetická '
                            'elita cvičí na zásah proti kybernarušiteľom.</p>'),
    },
    {
        'name': 'Katharine Jarmul',
        'bio': gettext('Katharine Jarmul is a pythonista and lover of all things Unix. She runs a data consulting company called Kjamistan in Berlin, Germany and loves to rant about data analysis, natural language processing, ethical machine learning and automation workflows. When she\'s not ranting, she\'s likely cooking or maybe taking photos, or quite possibly reading and retweeting other rants on Twitter.'),
        'country': 'DE',
        'url': 'http://kjamistan.com/',
        'avatar': 'img/speakers/katharine_jarmul.jpeg',
        'talk': 'Introduction to Machine Learning with Python',
        'tag': 'ai',
        'abstract': gettext('<p>In this half-day workshop, we\'ll take a walk through a Kaggle competition on house '
                            'prices to explore our dataset. Then, we\'ll build a model to submit our predictions to '
                            'Kaggle. Finally, we\'ll introspect what our model has learned. By the end of the course, '
                            'you should have an idea of how to get competing on Kaggle or building your own models '
                            'with Python and scikit-learn.</p>'
                            '<p>Students are expected to arrive ready to learn and with all packages properly '
                            'installed. There will also be some theoretical discussions on machine learning practices, '
                            'and some group work.</p>'
                            '<p>GitHub Repo: https://github.com/kjam/intro-to-ml</p>'),
    },
    {
        'name': 'Michael Kennedy',
        'bio': gettext('Michael Kennedy is a technologist, podcaster, and entrepreneur. He is the host and founder of the two most popular Python podcasts: Talk Python To Me and Python Bytes. He teaches online courses for developers through his business Talk Python Training. Michael loves to help fellow podcasters and developers make their way in the world. Connect with him on Twitter via @mkennedy and check out his podcasts as https://talkpython.fm and https://pythonbytes.fm.'),
        'country': 'USA',
        'url': 'https://talkpython.fm/',
        'avatar': 'img/speakers/michael_kennedy.jpg',
        'talk': '',
        'tag': '',
        'abstract': gettext('TBD'),
    },
    {
        'name': 'Ryan Kirkbride',
        'bio': gettext('Ryan is currently in the middle of his practice-led PhD researching communication and '
                       'collaboration in live coding ensembles through software development, composition, and '
                       'performance. He developed the Python-driven live coding language, FoxDot, for live coding '
                       'musical patterns with a focus on object-oriented and creating dynamic musical systems. He '
                       'performs regularly on the "Algorave" circuit under the moniker of “Qirky” and is also a '
                       'founding member of The Yorkshire Programming Ensemble (TYPE), alongside Lucy Cheesman and '
                       'Laurie Johnson, who enjoy exploring constraints for group improvisation as composition and '
                       'generally making a lot of noise.'),
        'country': 'UK',
        'url': '#',
        'avatar': 'img/speakers/no_avatar.svg',
        'talk': gettext('Programming Python as performance: live coding with FoxDot'),
        'tag': 'other',
        'abstract': gettext('<p>In this talk I will introduce the topic of live coding; the interactive programming'
                            ' experience for generating audio and visuals but this talk will mainly focus on audio.'
                            ' Live coders use programming languages to describe rules for generating music but then'
                            ' re-write these rules while the program is running. By continually writing and '
                            're-writing these rules live coders creating a shifting musical experience that is '
                            'always in flux. All of this happens live in front of audience with the code projected '
                            'for all to see. I will go on to discuss the multiple tools that are available for '
                            'live coding and showcase the FoxDot environment, which allows you to live code music '
                            'using Python. I will talk about the motivation for developing FoxDot and describe some'
                            ' of its key features as well as how you can set it up yourself at home. The talk will '
                            'be concluded with a short demonstration that will be part explanation and part '
                            'performance.'),

    },
    {
        'name': 'Maciej Szulik',
        'bio': gettext('Maciej is a passionate developer with over 10 years of experience in many languages. Currently, he is hacking on bugs.python.org and CPython\'s IMAP library by night. Whereas in the light of day, he\'s working on OpenShift and Kubernetes for Red Hat. In his spare time he organizes PyCon PL, helps reviewing talks for PyCon, talks at various events and meet ups around Europe.'),
        'country': 'PL',
        'url': '',
        'avatar': 'img/speakers/maciej_szulik.png',
        'talk': 'Effectively running python applications in Kubernetes/OpenShift',
        'tag': 'devops',
        'abstract': gettext('<p>Google, Red Hat, Intel, Huawei, Mirantis, Deis and many, many others are investing'
                            'a lot of time and effort into improving Kubernetes.  I bet, you have encountered'
                            'that name at least once in the past twelve months, either on Hacker News, Reddit,'
                            'or somewhere else.  Do you want to learn more about the best container orchestration'
                            'in the universe, but were afraid of the setup complexity?  Do you want to see how'
                            'easy it is to run any application using containers?  Do you want to experience'
                            'the joy of scaling application with a single click?  This, and a lot more will be'
                            'discussed in details.</p>'
                            '<p>In this tutorial, every attendee will be provided with an environment, and step by'
                            'step instructions necessary to setup the environment, build and deploy a microservices'
                            'based sample application.  Alternatively, a sample application of any choosing can'
                            'be used throughout the entire tutorial.  All that will be performed on OpenShift,'
                            'which is a Red Hat distribution of Kuberenets with some add-ons that will be described'
                            'in details at the beginning of the tutorial.  To wet your appetite even more, here'
                            'are some of the topics we are going to cover:<ul>'
                            '<li>automatic build and deployment</li>'
                            '<li>git integration</li>'
                            '<li>image registry integration</li>'
                            '<li>scaling application</li>'
                            '<li>containers security</li>'
                            '<li>batch tasks</li>'
                            '</ul>and much more.</p>'
                            '<p>After the session, every person will be able to play around with the accompanying'
                            'code repository that was used in the tutorial, which includes detailed instructions'
                            'how to run it on your own from scratch.</p>'),
    }
)


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


def _get_template_variables(**kwargs):
    variables = {
        'title': gettext('PyCon SK'),
        'logo': LOGO_PYCON,
        'ld_json': LDJSON
    }
    variables.update(kwargs)

    if 'current_lang' in g:
        variables['lang_code'] = g.current_lang
    else:
        variables['lang_code'] = app.config['BABEL_DEFAULT_LOCALE']

    return variables


@app.route('/<lang_code>/index.html')
def index():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('index.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_index='active'))


@app.route('/<lang_code>/tickets.html')
def tickets():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('tickets.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_tickets='active'))


@app.route('/<lang_code>/schedule.html')
def schedule():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    variables = _get_template_variables(ld_json=LDJSON_EVENT, li_schedule='active')
    variables['data'] = DATA

    return render_template('schedule.html', **variables)


@app.route('/<lang_code>/speakers.html')
def speakers():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    variables = _get_template_variables(ld_json=LDJSON_EVENT, li_speakers='active')
    variables['data'] = DATA

    return render_template('speakers.html', **variables)


@app.route('/<lang_code>/cfp.html')
def cfp():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('cfp.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_cfp='active'))


@app.route('/<lang_code>/coc.html')
def coc():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('coc.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_coc='active'))


@app.route('/<lang_code>/hall-of-fame.html')
def hall_of_fame():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava",
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('hall-of-fame.html', **_get_template_variables(ld_json=LDJSON_EVENT,
                                                                          li_hall_of_fame='active'))


@app.route('/<lang_code>/venue.html')
def venue():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('venue.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_venue='active'))


@app.route('/<lang_code>/sponsoring.html')
def sponsoring():
    lang = get_locale()
    LDJSON_EVENT = {
        "@context": "http://schema.org",
        "@type": "Event",
        "name": u"PyCon SK 2018",
        "description": "PyCon will be back at Slovakia in 2018 again. PyCon SK is a community-organized conference for "
                       "the Python programming language.",
        "startDate": "2018-03-09T9:00:00+01:00",
        "endDate": "2018-03-11T18:00:00+01:00",
        "image": "https://2018.pycon.sk/static/img/backgrounds/lecture_hall.jpg",
        "location": {
            "@type": "Place",
            "name": "Bratislava"
        },
        "url": "https://2018.pycon.sk/" + lang + "/",
        "workPerformed": {
            "@type": "CreativeWork",
            "name": "PyCon SK 2018",
            "creator": {
                "@type": "Organization",
                "name": "SPy o.z.",
                "url": "https://spy.python.sk/",
                "logo": "https://spy.python.sk/img/logo/spy-logo.png",
            }
        }
    }
    return render_template('sponsoring.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_sponsoring='active'))


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
    domain = 'https://2018.pycon.sk'
    pages = []

    # static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            if len(rule.arguments) == 0:
                indx = rule.rule.replace('/', '')
                sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                pages.append({
                    'loc': domain + rule.rule,
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
                                'url': domain + rule.rule.replace('<lang_code>', alt_lang)
                            })

                    sitemap_data = SITEMAP.get(indx, SITEMAP_DEFAULT)
                    pages.append({
                        'loc': domain + rule.rule.replace('<lang_code>', lang),
                        'alternate': alternate,
                        'lastmod': get_lastmod(rule, sitemap_data),
                        'freq': sitemap_data['freq'],
                        'prio': sitemap_data['prio'],
                    })

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


if __name__ == "__main__":
    app.run(debug=True, host=os.environ.get('FLASK_HOST', '127.0.0.1'), port=int(os.environ.get('FLASK_PORT', 5000)),
            use_reloader=True)
