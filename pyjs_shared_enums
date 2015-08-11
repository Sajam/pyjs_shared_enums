#!/usr/bin/env python
import os
import ast
import re
from optparse import OptionParser

BASE_PATH = os.path.normpath(os.path.dirname(__file__))


class AstHelpers(object):
    converters = {
        ast.Num: lambda o: o.n,
        ast.Str: lambda o: '\'{}\''.format(o.s),
        ast.List: lambda o: '[{}]'.format(', '.join([str(AstHelpers.ast_as_js(el)) for el in o.elts]))
    }

    supported_ast_types = converters.keys()

    @staticmethod
    def ast_as_js(v):
        try:
            return AstHelpers.converters[type(v)](v)
        except Exception:
            return v

    @staticmethod
    def get_child_classes(node, class_name_or_names):
        class_name_or_names = tuple(class_name_or_names)
        classes = []

        for n in ast.walk(node):
            if isinstance(n, ast.ClassDef):
                classes.append(n)

        return filter(lambda o: any([b.id in class_name_or_names for b in o.bases]), classes)

    @staticmethod
    def get_assignments(node):
        assignments = []

        for n in node:
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    assignments.append([t.id, n.value])

        return dict(filter(lambda i: isinstance(i[1], tuple(AstHelpers.supported_ast_types)), assignments))


class CommonEnumGenerator(object):
    ENUM_CLASSES_NAMES = ('Enum', 'IntEnum', 'enum.Enum', 'enum.IntEnum',)

    # Must be a string that contain enum's source file path (relative_enum_file_path).
    AS_JS_ENUM_START = '// {python_relative_file_path}\n'

    # Must be an unique string that indicates end of single enum definition.
    AS_JS_ENUM_END = '// {}\n\n'.format('-' * 80)

    ENUM_AS_JS = '// lineno: {enum_lineno}\nvar {enum_name} = {{\n{enum_members}\n}};\n'
    ENUM_AS_JS = '{start}{enum}{end}'.format(start=AS_JS_ENUM_START, enum=ENUM_AS_JS, end=AS_JS_ENUM_END)

    def __init__(self, python_file_path, js_file_path):
        self.python_file_path = os.path.normpath(python_file_path)
        self.js_file_path = os.path.normpath(js_file_path)
        self.python_relative_file_path = self.python_file_path.replace(
            os.path.commonprefix([BASE_PATH, self.python_file_path]), '')
        print 'after init'

    def __enter__(self):
        self.python_file_handler = open(self.python_file_path, 'r')
        self.js_file_handler = open(self.js_file_path, 'rw+')

        self.python_file_contents = self.python_file_handler.read()
        self.output = self.js_file_handler.read()

        self.js_file_handler.truncate(0)
        self.js_file_handler.seek(0)

        return self

    def generate(self):
        self.output_remove_current_enums()
        enums = self.get_enums_from_python_file()

        for enum in enums:
            self.output_add_enum(enum)

        self.js_file_handler.write(self.output)

    def output_remove_current_enums(self):
        enums_from_python_file = re.compile('{start}(?:.*?){end}'.format(
            start=re.escape(self.AS_JS_ENUM_START.format(python_relative_file_path=self.python_relative_file_path)),
            end=re.escape(self.AS_JS_ENUM_END)), re.DOTALL | re.MULTILINE)
        self.output = re.sub(enums_from_python_file, '', self.output)

    def get_enums_from_python_file(self):
        ast_tree = ast.parse(self.python_file_contents)
        return AstHelpers.get_child_classes(ast_tree, self.ENUM_CLASSES_NAMES)

    def output_add_enum(self, enum):
        members = AstHelpers.get_assignments(enum.body)
        members_as_js_strings_list = ['\t{}: {}'.format(k, AstHelpers.ast_as_js(v)) for k, v in members.iteritems()]

        self.output += self.ENUM_AS_JS.format(
            python_relative_file_path=self.python_relative_file_path,
            enum_lineno=enum.lineno,
            enum_name=enum.name,
            enum_members=',\n'.join(members_as_js_strings_list)
        )

    def __exit__(self, type, value, traceback):
        self.python_file_handler.close()
        self.js_file_handler.close()


def main():
    parser = OptionParser(usage='Usage: %prog python_input_file_path [options]', version='%prog 1.0')
    parser.add_option('-o', '--output', dest='output', metavar='OUTPUT_FILE_PATH', help='Path to output JS file.')
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error('Missing argument.')
    elif not options.output:
        parser.error('No output file specified.')
    
    with CommonEnumGenerator(str(args[0]), options.output) as common_enum_generator:
        common_enum_generator.generate()


if __name__ == '__main__':
    main()
