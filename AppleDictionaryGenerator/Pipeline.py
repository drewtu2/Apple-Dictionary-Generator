from AppleDictionaryGenerator.DictionaryDirective import DictionaryRenderer, DictionaryDirective
import mistune
import shutil
import os
import subprocess

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

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

def PrepareOutputDirectory(dictionary_name):
    """
    """

    output_file = dictionary_name
    output_file.replace(" ", "-")
    output_file_xml = output_file + ".xml"
    
    toolkit_dir = "Apple-Dictionary-Development-Kit"

    # Copy the template files.
    src = "{}/project_templates".format(toolkit_dir)
    output_directory = "build/{}".format(output_file)
    
    if(os.path.exists(output_directory)):
        print("template already exists!")
        return
    
    shutil.copytree(src, output_directory)

def Move(dictionary_name):
    """
    """

    output_file = dictionary_name
    output_file.replace(" ", "-")
    output_file_xml = output_file + ".xml"
    output_directory = "build/{}".format(output_file)


    if(os.path.exists("{}/{}".format(output_directory, output_file_xml))):
        os.remove("{}/{}".format(output_directory, output_file_xml))
        print("Overwriting old dictionary file!")

    # Move the generated file to the output directory. 
    shutil.move(output_file_xml, output_directory)

def GenerateDictionary(dictionary_name):
    """
    """

    output_file = dictionary_name
    output_file.replace(" ", "-")
    output_file_xml = output_file + ".xml"

    project_base_dir = os.getcwd()
    toolkit_dir = "Apple-Dictionary-Development-Kit"
    
    output_directory = "build/{}".format(output_file)

    # Cd to the directory, execute the makefile. 
    with cd(output_directory):
        toolkit = "DICT_BUILD_TOOL_DIR ={}/{}".format(project_base_dir, toolkit_dir)
        dict_name = "DICT_NAME={}".format(dictionary_name)
        output_var = "DICT_SRC_PATH={}".format(output_file_xml)

        # subprocess.run(["make", dict_name, output_var, toolkit])
        # subprocess.run(["make", dict_name, output_var, toolkit, "install"])
        
    

