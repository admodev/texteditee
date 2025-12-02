import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texteditee.main import Editor

# Create a simple test
editor = Editor('test_file.py')
print(f"Editor created successfully")
print(f"Buffer has {editor.buffer.line_count} lines")
print(f"Viewport height: {editor.viewport.height}")
print(f"Terminal height: {editor.term.height}")
print(f"Expected content height: {editor.term.height - 3}")
print("\nFirst 3 lines of buffer:")
for i in range(min(3, editor.buffer.line_count)):
    print(f"  Line {i}: {repr(editor.buffer.get_line(i))}")
