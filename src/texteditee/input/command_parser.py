from typing import Optional, Callable, Dict, Tuple
import re


class Command:
    def __init__(self, name: str, handler: Callable, args: list = None):
        self.name = name
        self.handler = handler
        self.args = args or []


class CommandParser:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self._register_default_commands()
    
    def _register_default_commands(self) -> None:
        pass
    
    def register(self, name: str, handler: Callable) -> None:
        self.commands[name] = handler
    
    def parse(self, command_line: str) -> Optional[Command]:
        if not command_line:
            return None
        
        parts = command_line.split(maxsplit=1)
        cmd_name = parts[0]
        args_str = parts[1] if len(parts) > 1 else ''
        
        if cmd_name in self.commands:
            args = self._parse_args(args_str)
            return Command(cmd_name, self.commands[cmd_name], args)
        
        if cmd_name.isdigit():
            return Command('goto', lambda editor, line: editor.goto_line(int(line) - 1), [cmd_name])
        
        match = re.match(r'^(\d+),(\d+)s/(.+)/(.*)/$', command_line)
        if match:
            start, end, pattern, replacement = match.groups()
            return Command('substitute', 
                         lambda e, s, en, p, r: e.substitute(int(s)-1, int(en)-1, p, r),
                         [start, end, pattern, replacement])
        
        match = re.match(r'^s/(.+)/(.*)/$', command_line)
        if match:
            pattern, replacement = match.groups()
            return Command('substitute_line',
                         lambda e, p, r: e.substitute_current_line(p, r),
                         [pattern, replacement])
        
        return None
    
    def _parse_args(self, args_str: str) -> list:
        if not args_str:
            return []
        
        args = []
        current_arg = ''
        in_quotes = False
        quote_char = None
        
        for char in args_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char.isspace() and not in_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ''
            else:
                current_arg += char
        
        if current_arg:
            args.append(current_arg)
        
        return args
    
    def complete(self, partial: str) -> list[str]:
        if not partial:
            return sorted(self.commands.keys())
        
        return sorted([cmd for cmd in self.commands.keys() if cmd.startswith(partial)])
