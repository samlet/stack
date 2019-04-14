from mako.template import Template

section_seg='''import 'package:flutter/material.dart';

class ${name} extends StatefulWidget {
  @override
  State<${name}> createState() => _${name}State();
}

class _${name}State extends State<${name}> {
  final TextEditingController _textController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
        child: Row(
      children: [
        Expanded(
          child: Padding(
            padding: EdgeInsets.only(left: 10.0),
            child: TextFormField(
              controller: _textController,
              decoration: InputDecoration(
                labelText: 'City',
                hintText: 'Chicago',
              ),
            ),
          ),
        ),
        IconButton(
          icon: Icon(Icons.search),
          onPressed: () {
            Navigator.pop(context, _textController.text);
          },
        )
      ],
    ));
  }
}

'''

class GenSections(object):
    def sample(self):
        tpl=Template(section_seg)
        print(tpl.render(name="LocationSelection"))

    def gen(self, name):
        import clipboard
        tpl = Template(section_seg)
        cnt = tpl.render(name=name)
        print(cnt)
        clipboard.copy(cnt)

if __name__ == '__main__':
    import fire
    fire.Fire(GenSections)
