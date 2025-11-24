import pytest
from texteditee.core.buffer import Buffer, GapBuffer


class TestGapBuffer:
    def test_insert_single_char(self):
        buf = GapBuffer()
        buf.insert(0, 'a')
        assert buf.get_text() == 'a'
    
    def test_insert_multiple_chars(self):
        buf = GapBuffer()
        buf.insert(0, 'h')
        buf.insert(1, 'e')
        buf.insert(2, 'l')
        buf.insert(3, 'l')
        buf.insert(4, 'o')
        assert buf.get_text() == 'hello'
    
    def test_delete_char(self):
        buf = GapBuffer()
        buf.insert(0, 'h')
        buf.insert(1, 'e')
        buf.insert(2, 'l')
        deleted = buf.delete(1)
        assert deleted == 'l'
        assert buf.get_text() == 'he'
    
    def test_get_char(self):
        buf = GapBuffer()
        buf.insert(0, 'a')
        buf.insert(1, 'b')
        buf.insert(2, 'c')
        assert buf.get_char(0) == 'a'
        assert buf.get_char(1) == 'b'
        assert buf.get_char(2) == 'c'


class TestBuffer:
    def test_create_empty_buffer(self):
        buf = Buffer()
        assert buf.line_count == 1
        assert buf.get_line(0) == ''
    
    def test_insert_char(self):
        buf = Buffer()
        buf.insert_char(0, 0, 'a')
        assert buf.get_line(0) == 'a'
    
    def test_insert_newline(self):
        buf = Buffer()
        buf.insert_char(0, 0, 'h')
        buf.insert_char(0, 1, 'i')
        buf.insert_char(0, 2, '\n')
        assert buf.line_count == 2
        assert buf.get_line(0) == 'hi'
        assert buf.get_line(1) == ''
    
    def test_delete_char(self):
        buf = Buffer()
        buf.insert_char(0, 0, 'a')
        buf.insert_char(0, 1, 'b')
        deleted = buf.delete_char(0, 0)
        assert deleted == 'a'
        assert buf.get_line(0) == 'b'
    
    def test_delete_line(self):
        buf = Buffer()
        buf.insert_char(0, 0, 'l')
        buf.insert_char(0, 1, 'i')
        buf.insert_char(0, 2, 'n')
        buf.insert_char(0, 3, 'e')
        deleted = buf.delete_line(0)
        assert deleted == 'line'
        assert buf.line_count == 1
        assert buf.get_line(0) == ''
    
    def test_join_lines(self):
        buf = Buffer()
        buf.insert_line(0, 'first')
        buf.insert_line(1, 'second')
        buf.join_lines(0)
        assert buf.line_count == 1
        assert buf.get_line(0) == 'firstsecond'
    
    def test_modified_flag(self):
        buf = Buffer()
        assert not buf.modified
        buf.insert_char(0, 0, 'a')
        assert buf.modified
