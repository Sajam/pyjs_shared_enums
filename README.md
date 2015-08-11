# PyJS shared enums

This program allows you to keep enums in JavaScript synchronized with those defined in Python files.
No more need for repeating definition manually.

## How do I setup it?

* Put `pyjs_shared_enums` somewhere in your project. Let it be `tools` directory.
* Set class name for enums in `pyjs_shared_enums` (`ENUM_CLASS_NAME` variable).
* Set up file watcher for Python (`*.py`) files (if you're using IntelliJ IDE you can just import and adjust
  `intellij_watcher.xml`):
  
    - scope: Project's Python files,
    - program: `[PROJECT_DIR]/tools/pyjs_shared_enums`,
    - arguments: `[PROJECT_DIR]/statis/js/enums.js [FILE_PATH]`:
        - `[PROJECT_DIR]/statis/js/enums.js` is path to output JavaScript file, 
        - `[FILE_PATH]` is path to changed file that triggered watcher (macro usually).
      
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
