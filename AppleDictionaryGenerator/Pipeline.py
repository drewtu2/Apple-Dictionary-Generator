from AppleDictionaryGenerator.DictionaryDirective import DictionaryRenderer, DictionaryDirective
from AppleDictionaryGenerator.ConfigReader import ConfigReader
from AppleDictionaryGenerator.Utils import *
import mistune
import shutil
import os
import subprocess

PROJECT_DIR = os.environ["APPLE_DICTIONARY_GENERATOR_HOME"]

def GenerateXML(input_file: str, dictionary_name: str):
    """
    Generates the Apple XML Source file used for the dictionary. 

    Reads from the given md file and writes it to <dictionary_name>.xml in the current working 
    directory.
    """

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

def PrepareOutputDirectory(input_file: str, dictionary_name: str):
    """
    Prepares the output directory for the dictionary.
    - Copies the toolkit project template to the build directory.
    - Copies the source file to the build directory.
    - Copies the images from the source file to the build directory. 
    """
    
    output_file = dictionary_name
    output_file.replace(" ", "-")

    toolkit_dir = "{}/Apple-Dictionary-Development-Kit".format(PROJECT_DIR)

    # Copy the template files to the output directory.
    template_src = "{}/project_templates".format(toolkit_dir)
    output_directory = "build/{}".format(output_file)
    
    if(os.path.exists(output_directory)):
        print("Template already exists! No need to copy again.")
    else:
        shutil.copytree(template_src, output_directory)

    # Copy the input_file to the output directory.
    shutil.copy(input_file, "{}/{}".format(output_directory, os.path.basename(input_file)))

    # TODO (drewtu2): This requires the user to pass in the input_file as 
    # `dict_folder/input_file.xml` to succeed. This is a bit brittle....
    # Copy the images over! 
    # Need to use the copytree helper so that we can copy the contents of the given directory to the 
    # existing directory wihtout throwing an error.
    dict_dir = os.path.dirname(input_file)
    copytree("{}/{}".format(dict_dir, "Images"), "{}/{}".format(output_directory, "OtherResources/Images"))

def Move(dictionary_name: str):
    """
    Move the generated dictionary file to the build directory. 

    OVERWRITES the xml in the build directory if it already exists.
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

def UpdatePlist(config: ConfigReader):
    """
    Updates te plist with the given config.
    """
    # TODO (drewtu2): Implement this
    pass

def GenerateDictionary(dictionary_name: str):
    """
    Calls the makefile in the build directory.
    """

    output_file = dictionary_name
    output_file.replace(" ", "-")
    output_file_xml = output_file + ".xml"
    toolkit_dir = "{}/Apple-Dictionary-Development-Kit".format(PROJECT_DIR)
    output_directory = "build/{}".format(output_file)

    # Cd to the directory, execute the makefile. 
    with cd(output_directory):
        toolkit = "DICT_BUILD_TOOL_DIR ={}".format(toolkit_dir)
        dict_name = "DICT_NAME={}".format(dictionary_name)
        output_var = "DICT_SRC_PATH={}".format(output_file_xml)

        # TODO (drewtu2): Not sure if we should actually run this here... 
        # subprocess.run(["make", dict_name, output_var, toolkit])
        # subprocess.run(["make", dict_name, output_var, toolkit, "install"])
        
def Pipeline(config_file: str):
    """
    """

    config_dir = os.path.dirname(config_file)

    config = ConfigReader(config_file)

    input_file = "{}/{}".format(config_dir, config.input_file())
    dictionary_name = config.dictionary_name()
    
    # Give md file and output name. 
    GenerateXML(input_file, dictionary_name)
    
    # Copy the necessary template files. 
    PrepareOutputDirectory(input_file, dictionary_name)

    # Move generated files. 
    Move(dictionary_name)

    # Updates the plist. 
    UpdatePlist(config)

    # Execute the make.
    GenerateDictionary(dictionary_name)
