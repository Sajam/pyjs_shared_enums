# PyJS shared enums

This program allows you to keep enums in JavaScript synchronized with those defined in Python files.
File watcher can observe for changes in Python files and synchronize enums by compiling them to corresponding
output to JavaScript file. No need to define it twice anymore!

## How do I setup it?

* Put `pyjs_shared_enums` somewhere in your project. Let it be `tools` directory.
* Set class name(s) for enums in `pyjs_shared_enums` (`ENUM_CLASSES_NAMES` variable).
* Set up file watcher for Python (`*.py`) files (if you're using IntelliJ IDE you can just import and adjust
  `intellij_watcher.xml`):
  
    - scope: Project's Python files,
    - program: `$PROJECT_DIR/tools/pyjs_shared_enums`,
    - arguments: `$FILE_PATH --output=$PROJECT_DIR/app/js/enums.js`:
        - `$FILE_PATH` is path to changed file that triggered watcher (macro usually),
        - `$PROJECT_DIR/app/js/enums.js` is path to output JavaScript file.

* That's all ... !

## How it works?

* ... Now when you change some Python code program will:

    - read contents of output JS file and Python input file
    - truncate output JS file
    - remove all enums that comes from Python input file from saved output JS file contents
    - parse Python input file (using ast), and find classes that inherits after enum class
    - generate corresponding JS code
    - append generated code to output JS content
    - save output JS file  

## Run manually

```
Usage: pyjs_shared_enums python_input_file_path [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OUTPUT_FILE_PATH, --output=OUTPUT_FILE_PATH
                        Path to output JS file.
```
