import click

# ⊕ [Welcome to Click — Click Documentation (7.x)](https://click.palletsprojects.com/en/7.x/)
# ⊕ [Commands and Groups — Click Documentation (7.x)](https://click.palletsprojects.com/en/7.x/commands/)

@click.command()
def main():
    click.echo("This is a CLI built with Click ✨")

if __name__ == "__main__":
    main()
