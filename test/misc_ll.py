"""
$ python -m test.misc_ll trans_clip tr 'en;zh-CN;ja' ja False 'Bir bira isterim.'
"""

if __name__ == '__main__':
    import fire
    from sagas.tool.misc import MiscTool
    fire.Fire(MiscTool)
