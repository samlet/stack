def secret_key():
    import os
    return(os.urandom(16))

def enabled_opt(options, opt):
    return opt in options and options[opt]
def disabled_opt(options, opt):
    return opt in options and not options[opt]

# ⊕ [python - How to get a random number between a float range? - Stack Overflow](https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range)
def rand(a,b):
    import random
    return random.uniform(a,b)


