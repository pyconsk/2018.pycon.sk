from flask_frozen import Freezer
from views import app

LANGUAGES = (
    {'lang_code': 'sk'},
    {'lang_code': 'en'}
)
freezer = Freezer(app)


@freezer.register_generator
def index():
    for lang in LANGUAGES:
        yield lang


if __name__ == '__main__':
    freezer.freeze()
