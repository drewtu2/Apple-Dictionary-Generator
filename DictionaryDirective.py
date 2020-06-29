import mistune
from mistune.directives.base import Directive
from mistune import HTMLRenderer

def GenerateXML(input_file, dictionary_name):

    # Read the md file.
    with open(input_file, "r") as f:
        contents = f.read()
        print(contents)
    
    # Generate the contents of the dictionary. 
    md_html = mistune.create_markdown( 
            renderer=DictionaryRenderer(),
            plugins=[DictionaryDirective()])
    
    # Output file. 
    output_file = dictionary_name
    output_file.replace(" ", "-")
    output_file += ".xml"

    # Write to the file with the appropriate surrounding dictionary matter. 
    with open(output_file, "w") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<d:dictionary xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:d=\"http://www.apple.com/DTDs/DictionaryService-1.0.rng\">\n")
        f.write(md_html(contents))
        f.write("</d:dictionary>")

class DictionaryRenderer(HTMLRenderer):
    NAME = "dictionary-xml"

class DictionaryDirective(Directive):
    SUPPORTED_NAMES = {"entry"}

    def parse(self, block, m, state):
        options = self.parse_options(m)

        # Convert to a dictionary where the values are lists. Take care to 
        # append to list in the cases of multiples of the same key. 
        options_dict = {}
        for i in options:  
            options_dict.setdefault(i[0],[]).append(i[1])

        
        name = m.group('name')
        title = m.group('value')
        text = self.parse_text(m)

        rules = list(block.rules)
        rules.remove('directive')
        children = block.parse(text, state, rules)
        return {
            'type': 'dictionary',
            'children': children,
            'params': (name, title, options_dict)
        }

    def __call__(self, md):
        for name in self.SUPPORTED_NAMES:
            self.register_directive(md, name)

        if 'xml' in md.renderer.NAME:
            md.renderer.register('dictionary', render_xml_dictionary)
        elif 'html' in md.renderer.NAME:
            md.renderer.register('dictionary', render_html_dictionary)
        elif 'ast' in md.renderer.NAME:
            md.renderer.register('dictionary', render_ast_dictionary)

def render_xml_dictionary(text, name, title, options):
    """
    <d:entry id="make_1" d:title="make">
            <d:index d:value="make"/>
            ...
            <d:index d:value="make"/>
            
            {{ contents }}
    </d:entry>
    """

    entry_id = options.get('id')[0]

    xml = "<d:entry id=\"{}\" d:title=\"{}\">\n".format(entry_id, title)
    for item in options.get("index"):
        xml += " <d:index d:value=\"{}\"/>\n".format(item)

    xml += text

    return xml + "</d:entry>\n"


def render_html_dictionary(text, name, title=None):
    html = '<section class="admonition ' + name + '">\n'
    if title:
        html += '<h1>' + title + '</h1>\n'
    if text:
        html += '<div class="admonition-text">\n' + text + '</div>\n'
    return html + '</section>\n'


def render_ast_dictionary(children, name, title=None):
    return {
        'type': 'dictonary',
        'children': children,
        'name': name,
        'title': title,
    }
