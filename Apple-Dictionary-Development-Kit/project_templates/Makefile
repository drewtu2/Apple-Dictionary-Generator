#
# Makefile
#
# Build
# `make DICT_NAME=<dict name> DICT_SRC_PATH=<path>`
#
# Install 
# `make DICT_NAME=<dict name> DICT_SRC_PATH=<path> install`
#

###########################


# You need to edit these values.
ifndef DICT_NAME
DICT_NAME		=	"My Dictionary"
endif

ifndef DICT_SRC_PATH
DICT_SRC_PATH		=	MyDictionary.xml
endif

ifndef CSS_PATH 
CSS_PATH		=	MyDictionary.css
endif

ifndef PLIST_PATH 
PLIST_PATH		=	MyInfo.plist
endif

DICT_BUILD_OPTS		=
# Suppress adding supplementary key.
# DICT_BUILD_OPTS		=	-s 0	# Suppress adding supplementary key.

###########################

# The DICT_BUILD_TOOL_DIR value is used also in "build_dict.sh" script.
# You need to set it when you invoke the script directly.

ifndef DICT_BUILD_TOOL_DIR 
DICT_BUILD_TOOL_DIR	=	"${HOME}/Developer/Extras/Dictionary\ Development\ Kit"
endif
DICT_BUILD_TOOL_BIN	=	"$(DICT_BUILD_TOOL_DIR)/bin"

###########################

DICT_DEV_KIT_OBJ_DIR	=	./objects
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	~/Library/Dictionaries
RM			=	/bin/rm

###########################

all:
	$(DICT_BUILD_TOOL_BIN)/build_dict.sh $(DICT_BUILD_OPTS) $(DICT_NAME) $(DICT_SRC_PATH) $(CSS_PATH) $(PLIST_PATH)
	echo "Done."


install:
	echo "Installing into $(DESTINATION_FOLDER)".
	mkdir -p $(DESTINATION_FOLDER)
	ditto --noextattr --norsrc $(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary  $(DESTINATION_FOLDER)/$(DICT_NAME).dictionary
	touch $(DESTINATION_FOLDER)
	echo "Done."
	echo "To test the new dictionary, try Dictionary.app."

clean:
	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)
