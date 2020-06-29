# AppleDictionaryGenerator

## Setup 
`pip install -r requirements.txt`

## Usage
`python -m AppleDictionaryGenerator generate <md file path> <dictionary name>`

## Md File Format
Definition file written in markdown with CommonMark formatting. Each entry needs 
to be preceded with some front matter. 

```
.. entry:: <tile>
    :id: <id>
    :index: <index>
    :index: <index 2>
```
The entry tag defines the title of the entry.
The id tag defines a unique identifier for each word.
The index tag defines the words that an entry can be searched by.
One entry may have multiple indices.

```
.. entry:: cook 
    :id: cook
    :index: cook
    :index: cooking
    :index: cooks

    The definition of cook...

.. entry:: food
    :id: food
    :index: food 

    The definition of food...
```

## TODO
- test usage include tags to have a dictionary defined by multiple files
included in one another
- implement folder with img directory that copies imgs into the the project
template directory
