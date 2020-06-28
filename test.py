import mistune
from DictionaryDirective import DictionaryDirective, DictionaryRenderer

with open("dictionary.md", "r") as f:
    contents = f.read()
    print(contents)

print("*"*20)
print("HTML")
print("*"*20)
md_html = mistune.create_markdown( 
        renderer=DictionaryRenderer(),
        plugins=[DictionaryDirective()])
print()
print()
print(md_html(contents))

with open("output.xml", "w") as f:
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<d:dictionary xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:d=\"http://www.apple.com/DTDs/DictionaryService-1.0.rng\">\n")
    f.write(md_html(contents))
    f.write("</d:dictionary>")

# print("*"*20)
# print("AST")
# print("*"*20)
# md_ast = mistune.create_markdown(renderer=mistune.AstRenderer(),
#         plugins=[DictionaryDirective()])
# ast = md_ast(contents)
