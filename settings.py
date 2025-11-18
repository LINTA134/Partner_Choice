from os import environ

SESSION_CONFIGS = [
    dict(
        name='Gossip_Experiment',
        display_name="協力に関する実験",
        num_demo_participants=1,
        app_sequence=[
            'App_01_Intro',
            'App_02_MainTask',
            'App_03_Questionnaire',
            'App_04_Debriefing',
        ],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ja'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'JPY'
USE_POINTS = True

ADMIN_USERNAME = environ.get('OTREE_ADMIN_USERNAME', 'admin')
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', '32c2e8cf2ac9fdfe1e063f2b16d1fe54')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = environ.get('OTREE_SECRET_KEY', '1647361268177')
