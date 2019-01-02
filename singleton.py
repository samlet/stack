class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_the_instance'):
            print("* create one.")
            cls._the_instance = object.__new__(cls, *args, **kwargs)
        return cls._the_instance
        