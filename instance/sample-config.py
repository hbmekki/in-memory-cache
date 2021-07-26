class Config(object):
    """Parent configuration class."""
    DEBUG = False
    NUMBER_OF_SLOTS = 10
    TIME_TO_LIVE = 60 
    EVICTION_POLICY = 'REJECT'

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True

class TestingOldesFirstConfig(TestingConfig):
    """Configurations for Testing."""
    EVICTION_POLICY = 'OLDEST_FIRST'

class TestingNewesFirstConfig(TestingConfig):
    """Configurations for Testing."""
    EVICTION_POLICY = 'NEWEST_FIRST'

class ProductionConfig(Config):
    """Configurations for Production."""
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'testing-oldest-first': TestingOldesFirstConfig,
    'testing-newest-first': TestingNewesFirstConfig,
    'production': ProductionConfig,
}
