import sys
import argparse

from AppleDictionaryGenerator.Pipeline import *

def cli_argparser():
    """Define command line parsers.
    :returns: defined argumentparser
    :rtype: :obj:`argparse.ArgumentParser`
    """
    
    def check_no_space(value):
        svalue = str(value)
        if " " in value:
            raise argparse.ArgumentTypeError("%s cannot contain spaces" % svalue)
        return svalue

    # DECLARE PARSERS
    # ###############
    argparser = argparse.ArgumentParser(
            prog="Dictionary Generator",
            description='Interact with Dictionary Generator.')
    subparsers = argparser.add_subparsers(help='action help', dest='action')
    subparsers.required = True
    
    # Create site parser
    validator_parser = subparsers.add_parser('generate')
    validator_parser.add_argument('dictionary-md', type=check_no_space, help='The .md file with the dictionary contents')
    validator_parser.add_argument('dictionary-name', type=str, help='The dictionary name.')
    # END PARSER DECLARATIONS
    # #######################
    return argparser

def main():
    argsparser = cli_argparser()
    args = argsparser.parse_args()

    # Give md file and output name. 
    GenerateXML(getattr(args,"dictionary-md"), getattr(args,"dictionary-name"))
    
    # Copy the necessary template files. 
    PrepareOutputDirectory(getattr(args,"dictionary-md"), getattr(args,"dictionary-name"))

    # Move generated files. 
    Move(getattr(args, "dictionary-name"))

    # Execute the make.
    GenerateDictionary(getattr(args, "dictionary-name"))

if __name__ == "__main__":
    main()
