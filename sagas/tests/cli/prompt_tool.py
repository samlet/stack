from __future__ import unicode_literals

class PromptTool(object):
    """
    ⊕ [Building prompts — prompt_toolkit 1.0.14 documentation](https://python-prompt-toolkit.readthedocs.io/en/1.0.14/pages/building_prompts.html#printing-text-output-in-color)
    """
    def input(self):
        """
        $ python -m sagas.tests.cli.prompt_tool input
        :return:
        """
        from prompt_toolkit import prompt

        text = prompt('Give me some input: ')
        print('You said: %s' % text)

    def color(self):
        from pygments.token import Token
        from prompt_toolkit.shortcuts import prompt
        from prompt_toolkit.styles import style_from_dict

        example_style = style_from_dict({
            # User input.
            Token: '#ff0066',

            # Prompt.
            Token.Username: '#884444',
            Token.At: '#00aa00',
            Token.Colon: '#00aa00',
            Token.Pound: '#00aa00',
            Token.Host: '#000088 bg:#aaaaff',
            Token.Path: '#884444 underline',
        })

        def get_prompt_tokens(cli):
            return [
                (Token.Username, 'john'),
                (Token.At, '@'),
                (Token.Host, 'localhost'),
                (Token.Colon, ':'),
                (Token.Path, '/user/john'),
                (Token.Pound, '# '),
            ]

        text = prompt(get_prompt_tokens=get_prompt_tokens, style=example_style)

    def hello(self):
        from prompt_toolkit.shortcuts import print_tokens
        from prompt_toolkit.styles import style_from_dict
        from pygments.token import Token

        # Create a stylesheet.
        style = style_from_dict({
            Token.Hello: '#ff0066',
            Token.World: '#44ff44 italic',
        })

        # Make a list of (Token, text) tuples.
        tokens = [
            (Token.Hello, 'Hello '),
            (Token.World, 'World'),
            (Token, '\n'),
        ]

        # Print the result.
        print_tokens(tokens, style=style)

    def bar(self):
        from prompt_toolkit import prompt
        from prompt_toolkit.styles import style_from_dict
        from prompt_toolkit.token import Token

        p = ' This is a toolbar. '
        def get_bottom_toolbar_tokens(cli):
            return [(Token.Toolbar, p)]

        style = style_from_dict({
            Token.Toolbar: '#ffffff bg:#333333',
        })

        while True:
            text = prompt('> ', get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                          style=style)
            print('You said: %s' % text)
            p=text

            if text=='q':
                break

if __name__ == '__main__':
    import fire
    fire.Fire(PromptTool)


