#!/usr/bin/env python

import click
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()  # @cli, not @click!
def sync():
    click.echo('Syncing')

@cli.command()
def plain():
    from sagas.tool.misc import MiscTool
    r=MiscTool().plain()
    print(r)

if __name__ == '__main__':
    cli()
