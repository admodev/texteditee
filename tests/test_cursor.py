import pytest
from texteditee.core.buffer import Buffer
from texteditee.core.cursor import Cursor


class TestCursor:
    def test_initial_position(self):
        buf = Buffer()
        cursor = Cursor(buf)
        assert cursor.position == (0, 0)
    
    def test_move_right(self):
        buf = Buffer()
        buf.insert_char(0, 0, 'h')
        buf.insert_char(0, 1, 'e')
        buf.insert_char(0, 2, 'l')
        cursor = Cursor(buf)
        cursor.move_right()
        assert cursor.col == 1
        cursor.move_right(2)
        assert cursor.col == 3
    
    def test_move_left(self):
        buf = Buffer()
        cursor = Cursor(buf)
        cursor.col = 3
        cursor.move_left()
        assert cursor.col == 2
        cursor.move_left(2)
        assert cursor.col == 0
    
    def test_move_down(self):
        buf = Buffer()
        buf.insert_line(0, 'line1')
        buf.insert_line(1, 'line2')
        cursor = Cursor(buf)
        cursor.move_down()
        assert cursor.line == 1
    
    def test_move_up(self):
        buf = Buffer()
        buf.insert_line(0, 'line1')
        buf.insert_line(1, 'line2')
        cursor = Cursor(buf)
        cursor.line = 1
        cursor.move_up()
        assert cursor.line == 0
    
    def test_move_to_line_start(self):
        buf = Buffer()
        cursor = Cursor(buf)
        cursor.col = 5
        cursor.move_to_line_start()
        assert cursor.col == 0
    
    def test_move_to_line_end(self):
        buf = Buffer()
        buf.insert_line(0, 'hello')
        cursor = Cursor(buf)
        cursor.move_to_line_end()
        assert cursor.col == 5
    
    def test_move_word_forward(self):
        buf = Buffer()
        buf.insert_line(0, 'hello world test')
        cursor = Cursor(buf)
        cursor.move_word_forward()
        assert cursor.col == 6
        cursor.move_word_forward()
        assert cursor.col == 12
    
    def test_move_word_backward(self):
        buf = Buffer()
        buf.insert_line(0, 'hello world test')
        cursor = Cursor(buf)
        cursor.col = 12
        cursor.move_word_backward()
        assert cursor.col == 6
        cursor.move_word_backward()
        assert cursor.col == 0
