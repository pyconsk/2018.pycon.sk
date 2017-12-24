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
    return render_template('speakers.html', **_get_template_variables(ld_json=LDJSON_EVENT, li_speakers='active'))


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
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


if __name__ == "__main__":
    app.run(debug=True, host=os.environ.get('FLASK_HOST', '127.0.0.1'), port=int(os.environ.get('FLASK_PORT', 5000)),
            use_reloader=True)
