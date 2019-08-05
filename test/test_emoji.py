peach_1="""
{\__/} 
(• -•) 
🍑< \ 
"""
peach_2='''
{\__/} 
( •.•)
/ >🍑'''
class Emoji(object):
    def print_peach(self):
        print(peach_1)
        print(peach_2)

if __name__ == '__main__':
    import fire
    fire.Fire(Emoji)
