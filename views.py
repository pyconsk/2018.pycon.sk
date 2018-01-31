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

DATA = (
    # {
    #     'name': '',
    #     'bio': gettext(''),
    #     'country': '',
    #     'url': '',
    #     'avatar': 'img/speakers/.jpg',
    #     'talk': '',
    #     'tag': TAGS[''],
    #     'abstract': gettext(''),
    # },
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
        'name': 'František Benko',
        'bio': gettext('Working at Exponea as DevOps Engineer for about a year after finishing studies of '
                       'Telecommunications at FEI STU in Bratislava. Virtualization and container platforms were '
                       'always his passion.'),
        'country': 'SK',
        'url': '#',
        'avatar': 'img/speakers/frantisek_benko.jpg',
        'talk': 'To the Google in 80 Days',
        'tag': 'devops',
        'abstract': gettext('<p>We invite You on the journey of making Exponea and it\'s multi-terabyte in-memory '
                            'databases possible in the containerized environment of the Google Cloud.</p>'
                            '<p>Join us as we grasp the wheel of our multi-server hardware-based spaceship, navigate '
                            'through the dangerous oceans of no-downtime live migrations to safely dock in the calm '
                            'waters of Google bay or did we?</p>'),
    },
    {
        'name': 'Aaron Bassett',
        'bio': gettext(
            'Aaron is a senior software engineer turned developer advocate at Nexmo. A life-long tinkerer, Aaron has been creating things with code and electronics for as long as he can remember. He spends his time building cool stuff and helping other people build unbelievably cool stuff 🔥🔥🎉'),
        'country': 'UK',
        'url': 'https://nexmo.com',
        'avatar': 'img/speakers/aaron_bassett.jpg',
        'talk': 'When your wetware has too many threads - Tips from an ADHDer on how to improve your focus',
        'tag': 'softskills',
        'abstract': gettext(
            '<p>My brain is different. The regions involved in concentration, impulse control, and inhibition are '
            'smaller than usual; Like somewhere between 5% and 12% of adults I have ADHD. Even if you do not have the '
            'disorder yourself you probably work, live or know someone who does. But the world is not designed for '
            'people with ADHD, so to be successful I’ve had to develop techniques to keep my concentration and '
            'procrastination in check.</p>'
            '<p>In this talk, we’ll briefly look at what ADHD is and how it impairs not only concentration but also '
            'executive function. Then we’ll explore how changes in the workplace can benefit not just those with ADHD, '
            'but anyone whose work requires creativity or extended periods of focus. Next, we’ll look at some '
            'persistent myths about productivity, and what you can do personally to increase your concentration and '
            'output without burning out. Then I’ll present some techniques you can rollout within your team to remove '
            'distractions while improving the quality of communication.</p>'),
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
        'name': 'Tomáš Ehrlich',
        'bio': gettext('Full-stack developer who loves Python but got stuck in Javascript world for a long time and '
                       'now is drifting somewhere in between. Passionate triathlete and wannabe entrepreneur.'),
        'country': 'CZ',
        'url': '#',
        'avatar': 'img/speakers/tomas_ehrlich.jpg',
        'talk': 'GraphQL is the new black',
        'tag': 'web',
        'abstract': gettext('<p>GraphQL is a query language for web APIs, an alternative to REST. It allows clients to '
                            'define the structure of the required data. It’s strongly typed and allows introspection, '
                            'which make clients more flexible.</p>'
                            '<p>The talk will demonstrate usage of GraphQL on examples with Graphene '
                            '(http://graphene-python.org/), a GraphQL framework for Python. Most developers are '
                            'familiar with REST APIs, so the talk will compare GraphQL with REST, how they differ '
                            'and what problems GraphQL is trying to solve.</p>'
                            '<p>The outline is following:<ul>'
                            '<li>Comparison of GraphQL with REST API.</li>'
                            '<li>Queries, data types and introspection</li>'
                            '<li>Mutations</li></ul></p>'),
    },
    # {
    #     'name': 'Alex Ellis',
    #     'bio': gettext('Alex Ellis is a Docker Captain, the lead and author of the award-winning open-source serverless project OpenFaaS. Alex has 12 years of experience writing enterprise software and scaling distributed systems for over 500k clients. He is well known in the cloud and container community where he mentors and writes on all things tech from Docker to Raspberry Pi.'),
    #     'country': 'UK',
    #     'url': 'https://www.openfaas.com/',
    #     'avatar': 'img/speakers/alex_ellis.jpg',
    #     'talk': 'FaaS and Furious - Zero to Serverless in 60 seconds - Anywhere',
    #     'tag': 'devops',
    #     'abstract': gettext('<p>OpenFaaS (Functions as a Service) makes building serverless functions simple by using '
    #                         'containers to avoid vendor-lock-in. That means you can run your functions on your own '
    #                         'terms - anywhere.</p>'
    #                         '<p>This talk introduces the OpenFaaS project, how to build functions and then explores '
    #                         'real-world examples of how and why people are leveraging an event-driven architecture for '
    #                         'data science, cancer research and automation on-premise.</p>'
    #                         '<p>You can deploy OpenFaaS in 60 seconds on Kubernetes and other orchestrators through '
    #                         'the extensible architecture. Functions can then be built using code templates for your '
    #                         'favourite programming language or deployed directly from the community Function Store. '
    #                         'The project focuses on ease of use through its UI and CLI which can be used to test and '
    #                         'monitor functions. Observability and auto-scaling for demand are provided through '
    #                         'integrations with Prometheus and AlertManager.</p>'
    #                         '<p>OpenFaaS won Best Cloud Computing Software 2017 from InfoWorld and has a thriving '
    #                         'community with 70 contributors, 1500 commits and over 9k stars.</p>'),
    # },
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
        'bio': gettext(
            'Katharine Jarmul is a pythonista and lover of all things Unix. She runs a data consulting company called Kjamistan in Berlin, Germany and loves to rant about data analysis, natural language processing, ethical machine learning and automation workflows. When she\'s not ranting, she\'s likely cooking or maybe taking photos, or quite possibly reading and retweeting other rants on Twitter.'),
        'country': 'DE',
        'url': 'http://kjamistan.com/',
        'avatar': 'img/speakers/katharine_jarmul.jpg',
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
        'bio': gettext(
            'Michael Kennedy is a technologist, podcaster, and entrepreneur. He is the host and founder of the two most popular Python podcasts: Talk Python To Me and Python Bytes. He teaches online courses for developers through his business Talk Python Training. Michael loves to help fellow podcasters and developers make their way in the world. Connect with him on Twitter via @mkennedy and check out his podcasts as https://talkpython.fm and https://pythonbytes.fm.'),
        'country': 'USA',
        'url': 'https://talkpython.fm/',
        'avatar': 'img/speakers/michael_kennedy.jpg',
        'talk': '',
        'tag': '',
        'abstract': gettext('TBD'),
    },
    {
        'name': 'Rae Knowler',
        'bio': gettext('Rae Knowler is a web developer in Zürich, where they develop product data APIs and work on '
                       'Open Data projects. They are interested in the fascinating, comical and sometimes tragic '
                       'results of attempting to cram the complexity of life and society into computer systems. In '
                       'their spare time they read a lot of science fiction and hug cats.'),
        'country': 'CH',
        'url': 'http://raeknowler.com',
        'avatar': 'img/speakers/rae_knowler.jpg',
        'talk': 'Unsafe at Any Speed',
        'tag': 'generic',
        'abstract': gettext('<p>The default settings of some libraries and tools are so useless, or even dangerous, '
                            'that they should never be used. While they give the impression of being easy to use or '
                            'performant, they actually represent traps for the unwary user. I will show the concrete '
                            'problems caused by such defaults, and explore how to create tools with '
                            'good_defaults.</p>'),
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
        'name': 'Patricia Regina',
        'bio': gettext('Patricia is a Python developer working at Olist, a brazilian marketplace services platform. '
                       'She started developing web applications in 2010 and currently is interested in technologies '
                       'like Big Data and Search Engines. Being an enthusiast for women in tech, Patricia is involved '
                       'with women empowerment initiatives like Pyladies Brazil, Django Girls Curitiba and TechLadies '
                       'Brazil.'),
        'country': 'BR',
        'url': 'https://github.com/pattyvader',
        'avatar': 'img/speakers/patricia_regina.jpg',
        'talk': 'Search Engines with Python and Elasticsearch',
        'tag': 'web',
        'abstract': gettext('<p>A search engine is a software responsible for search into large amounts of data. Often,'
                            ' involved algorithms are complex and their architecture are not trivial. In this scenario,'
                            ' Elasticsearch appears as a great solution to solve the indexing and searching tasks. In '
                            'this talk I will show how Elasticsearch and Python can make the development of search '
                            'engines more easier. Also, I will show how Python can be used to build Web Crawlers and '
                            'Scrapers and how to send gathered data from the web to be indexed in Elasticsearch."</p>'),
    },
    {
        'name': 'Alejandro Saucedo',
        'bio': gettext(
            'Alejandro Saucedo is the Head of Deployed (ML) Engineering at Eigen Technologies, a Machine Learning LegalTech company, leading 10+ ML and DevOps engineers in London and New York. Alejandro is also the Founder and CTO at Exponential Technologies, a ML consultancy that tackles challenges in industrial sectors. In his previous lives he co-founded HackTrain, a technology consultancy that operated in the railway sector, worked as a Full-stack software developer at Bloomberg LP, and started HackaGlobal which is a global NGO that created multiple hackathon communities around the world that are still active to date.'),
        'country': 'UK',
        'url': 'http://e-x.io/',
        'avatar': 'img/speakers/alejandro_saucedo.jpg',
        'talk': 'Industrial Machine Learning: Building scalable distributed machine learning pipelines with Python',
        'tag': 'ai',
        'abstract': gettext('<p>This talk would provide useful and practical understanding on how to build '
                            'industry-ready machine learning models in python through distributed, '
                            'horizontally-scalable architectures. I will include why and when these architectures are '
                            'required, best practices, caveats, technologies to use them, and a practical '
                            'implementation using celery + rabbitmq.</p>'),
    },
    {
        'name': 'Václav Sauer',
        'bio': gettext(
            'Studoval jsem na FIT VUT v Brně, nyní pracuji v Kiwi.com a zajímam se o Python a komunitu kolem.'),
        'country': 'CZ',
        'url': '#',
        'avatar': 'img/speakers/no_avatar.svg',
        'talk': 'Práce s XML',
        'tag': 'generic',
        'abstract': gettext('<p>Workshop pro začátečníky</p>'
                            '<p>Obsah:<ul>'
                            '<li>Stručný úvod do XML</li>'
                            '<li>Instalace parseru</li>'
                            '<li>Nahrání, úprava, uložení XML</li>'
                            '<li>práce s daty v XML formátu</li>'
                            '<li>serializace a deserializace objektu do XML</li></ul></p>'),
    },
    {
        'name': 'Natalie Serebryakova',
        'bio': gettext('My name is Natalie; I have a Networking and Security background, but recently decided to '
                       'challenge myself in different space. That\'s why currently I work at Vevo as Software Engineer '
                       'in coolest DevOps team in San Francisco, CA, USA. Where part of my job includes building and '
                       'automating various tools that help our development team be more productive and happy.'
                       'I have an MS in Computer Since degree. For my first job, I had to do a lot of scripting for '
                       'configuring and managing thousands of switches, routers and other networking devices in our '
                       'company testing lab. After using sed, awk, Tcl I discovered and learned Python. It was '
                       'straightforward to pick up and worked well since then Python became my language of preference. '
                       'I also like Python for its big community.'
                       'In my spare time, I like to spend time with my pup Chai, bake and blog about baking.'
                       'Thank you, organizers, for giving me and people the opportunity to speak and this conference '
                       'and share our knowledge with the community.'),
        'country': 'USA',
        'url': 'http://01101110.com/',
        'avatar': 'img/speakers/no_avatar.svg',
        'talk': 'Maintaining reliable and secure continuous delivery for python microservices',
        'tag': 'devops',
        'abstract': gettext('<p>Guide for Python developers who are shifting to the new microservices-based '
                            'development.</p>'
                            '<p>In the agile methodology the speed at which software gets shipped these days in DevOps '
                            'there is no time to do traditional Secure SDLC like process where every stage of the '
                            'software development cycle has a security checklist. The only way is to automate as much '
                            'as possible and remove check gate style security practice.</p>'
                            '<p>Continuous Delivery is a software development discipline where you build software in '
                            'such a way that the software can be released to production at any time. It relies on the '
                            'complete automation of the deployment process.</p>'
                            '<p>Creating secure and reliable microservices before they land in production should be '
                            'important for every software developer. The software developer doesn’t have to be a '
                            'security expert in everything to work within a microservices architecture.</p>'),
    },
    {
        'name': 'Maciej Szulik',
        'bio': gettext(
            'Maciej is a passionate developer with over 10 years of experience in many languages. Currently, he is hacking on bugs.python.org and CPython\'s IMAP library by night. Whereas in the light of day, he\'s working on OpenShift and Kubernetes for Red Hat. In his spare time he organizes PyCon PL, helps reviewing talks for PyCon, talks at various events and meet ups around Europe.'),
        'country': 'PL',
        'url': '',
        'avatar': 'img/speakers/maciej_szulik.jpg',
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
    },
    {
        'name': 'Štěpán Tomsa',
        'bio': gettext(
            'Jazykozpytec, škarohlíd, mrzout... Již mnohaletý (asi senior prej) PHP vývojář z povolání. Zatím koníčkový, již brzy i profesionální (no, ehm… junior, batole) Ruby vývojář. Několikaletý pomocný kouč na ostravských PyLadies. Hrdá slezská náplava. Jediný člověk na světě, který si jako novoroční předsevzetí dal častější hraní počítačových her.'),
        'country': 'CZ',
        'url': 'https://github.com/glutexo',
        'avatar': 'img/speakers/stepan_tomsa.jpg',
        'talk': 'Cesta kolem světa za 30 minut',
        'tag': 'data',
        'abstract': gettext(
            '<p>Lidé mluví různými jazyky. Ba co hůř, oni jimi i píší a to i na počítači. Tyto jazyky se nepíší vždy '
            'latinkou. A i když ano, není ani ta vždy stejná. Tito lidé mají navíc v těchto jazycích a znakových '
            'sadách dokonce i jména, poštovní adresy atd. a vyplňují je třeba do webových formulářů. A to vše je jen '
            'začátek boje s řetězci...</p>'
            '<p>To, že v řetězcích se většinou ukrývá text v nějakém lidském jazyce, asi všichni tušíme. Snad jsme se '
            'každý i pokusili někdy nějaký takový zpracovat, porovnávat, řadit, ti odvážnější třeba i skloňovat. '
            'Odhrňme závěs a posviťme si na některé z těch unicodových nestvůr. Nakonec budeme rádi, že se nám takový '
            'text aspoň zobrazí na obrazovce; a někdy dokonce i správně. Alespoň dokud se nám na webu nezaregistruje '
            'někdo z Klingonské říše...</p>'),
    },
    {
        'name': 'Matej Vetrák',
        'bio': gettext('Matej Vetrak is a senior DevOps engineer that has been puzzled for the longest time as how to '
                       'build a proper high-available infrastructure composed of many small collaborative services for '
                       'systems at huge scale, until he got a change to build one. His favourite programming language '
                       'is Python and he is interested in a Docker, Kubernetes and open-source community in general. '
                       'He is currently employed by Exponea.'),
        'country': 'SK',
        'url': '#',
        'avatar': 'img/speakers/matej_vetrak.jpg',
        'talk': 'Managing high-available applications in production',
        'tag': 'devops',
        'abstract': gettext('<p>In this workshop we\'ll look at common problems that all developers are facing in the '
                            'latest trends of the ever changing scalable app world. We\'ll learn how to deploy, scale, '
                            'and manage high-available microservices using Docker, Kubernetes and other open-source '
                            'tools.</p>'
                            '<p>We will also address some of these problems: building and deploying applications, '
                            'pipelines, rolling updates, load balancing, scaling, replication, configuration, health '
                            'checking and self healing, monitoring, alerting, log aggregation, resource constraints, '
                            'capacity planning, data stores, security, key management, debugging and best '
                            'practices.</p>'
                            '<p>Who should attend?</p>'
                            '<p>People who are interested in containerized applications, are in the process of moving '
                            'to microservice architecture or are managing high-available production environments.</p>'
                            '<p>Why you should attend?</p>'
                            '<p>You want to start using Kubernetes in development and production.</p>'
                            '<p>You are already using Kubernetes, but you are not ready for production.</p>'
                            '<p>You would like to better understand new trend of high-available microservices.</p>'
                            '<p>How to prepare for the workshop?</p>'
                            '<p>Bring laptop with installed minikube: https://kubernetes.io/docs/tasks/tools/install-minikube/ and docker: https://docs.docker.com/engine/installation/</p>'),
    },

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
    variables['tags'] = TAGS

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
    variables['tags'] = TAGS

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
