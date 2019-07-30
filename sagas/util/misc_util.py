def secret_key():
    import os
    return(os.urandom(16))

def enabled_opt(options, opt):
    return opt in options and options[opt]
def disabled_opt(options, opt):
    return opt in options and not options[opt]


