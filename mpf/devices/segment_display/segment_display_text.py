"""Specialized text support classes for segment displays."""
import abc
from collections import namedtuple
from typing import Optional, List, Union

from mpf.core.rgb_color import RGBColor

DisplayCharacter = namedtuple("DisplayCharacter", ["char_code", "dot", "comma", "color"])

DOT_CODE = ord(".")
COMMA_CODE = ord(",")
SPACE_CODE = ord(" ")


class SegmentDisplayText(metaclass=abc.ABCMeta):

    """A list of characters with specialized functions for segment displays. Use for display text effects."""

    __slots__ = ["_text", "embed_dots", "embed_commas"]

    def __init__(self, char_list, embed_dots, embed_commas):
        """Initialize segment display text."""
        self.embed_dots = embed_dots
        self.embed_commas = embed_commas
        self._text = char_list

    # pylint: disable=too-many-arguments
    @classmethod
    def from_str_with_color(cls, text: str, display_size: int, collapse_dots: bool, collapse_commas: bool,
                            colors: List[RGBColor]) -> "ColoredSegmentDisplayText":
        """Create colored text."""
        char_colors = colors[:]
        # when fewer colors are supplied than text, extend the last color to the end of the text
        if len(char_colors) < len(text):
            char_colors.extend([colors[-1]] * (len(text) - len(char_colors)))
        return ColoredSegmentDisplayText(
            cls._create_characters(text, display_size, collapse_dots, collapse_commas, char_colors),
            collapse_dots, collapse_commas)

    # pylint: disable=too-many-arguments
    @classmethod
    def from_str(cls, text: str, display_size: int, collapse_dots: bool, collapse_commas: bool,
                 colors: Optional[List[RGBColor]] = None) -> \
            Union["ColoredSegmentDisplayText", "UncoloredSegmentDisplayText"]:
        """Create from string."""
        if colors:
            return cls.from_str_with_color(text, display_size, collapse_dots, collapse_commas, colors)

        char_colors = [None] * len(text)
        return UncoloredSegmentDisplayText(
            cls._create_characters(text, display_size, collapse_dots, collapse_commas, char_colors),
            collapse_dots, collapse_commas)

    @classmethod
    def _create_characters(cls, text: str, display_size: int, collapse_dots: bool, collapse_commas: bool,
                           colors: List[Optional[RGBColor]]) -> List[DisplayCharacter]:
        char_has_dot = False
        char_has_comma = False
        char_list = []
        default_color = colors[0] if colors else None
        assert len(text) <= len(colors)
        for char in reversed(text):
            char_code = ord(char)
            if collapse_dots and char_code == DOT_CODE:
                char_has_dot = True
                continue
            if collapse_commas and char_code == COMMA_CODE:
                char_has_comma = True
                continue

            char_list.insert(0, DisplayCharacter(char_code, char_has_dot, char_has_comma, colors.pop()))
            char_has_dot = False
            char_has_comma = False

        # ensure list is the same size as the segment display (cut off on left or right justify characters)
        current_length = len(char_list)
        if current_length > display_size:
            for _ in range(current_length - display_size):
                char_list.pop(0)
        elif current_length < display_size:
            for _ in range(display_size - current_length):
                char_list.insert(0, DisplayCharacter(SPACE_CODE, False, False, default_color))

        return char_list

    def blank_segments(self, flash_mask) -> "SegmentDisplayText":
        """Return new SegmentDisplayText with chars blanked."""
        return ColoredSegmentDisplayText(
            [char if mask != "F" else DisplayCharacter(SPACE_CODE, False, False, char.color)
             for char, mask in zip(self._text, flash_mask)],
            self.embed_dots, self.embed_commas
        )

    def convert_to_str(self):
        """Convert back to normal text string."""
        text = ""
        for display_character in self:
            text += chr(display_character.char_code)
            if display_character.dot:
                text += "."
            if display_character.comma:
                text += ","

        return text

    def __len__(self):
        """Return length."""
        return self._text.__len__()

    def __getitem__(self, item):
        """Return item or slice."""
        if isinstance(item, slice):
            return self.__class__(self._text.__getitem__(item), self.embed_dots, self.embed_commas)

        return self._text.__getitem__(item)

    def __eq__(self, other):
        """Return true if two texts and colors are the same."""
        # pylint: disable-msg=protected-access
        return isinstance(other, SegmentDisplayText) and self._text == other._text

    def extend(self, other_list):
        """Extend list."""
        # pylint: disable-msg=protected-access
        self._text.extend(other_list._text)

    @abc.abstractmethod
    def get_colors(self) -> Optional[List[RGBColor]]:
        """Get the list of colors for each character (if set)."""
        raise NotImplementedError()

    def __repr__(self):
        """Return string representation."""
        return "<{} {}>".format(self.__class__, self._text)


class UncoloredSegmentDisplayText(SegmentDisplayText):

    """Segment text without colors."""

    def get_colors(self) -> None:
        """Return None as we are transparent."""
        return None


class ColoredSegmentDisplayText(SegmentDisplayText):

    """Segment text with colors."""

    def get_colors(self) -> List[RGBColor]:
        """Get the list of colors for each character (if set)."""
        return [display_character.color for display_character in self]
