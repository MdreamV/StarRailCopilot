import re
from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from module.exception import ScriptError
import module.config.server as server

REGEX_PUNCTUATION = re.compile(r'[ ,.\'"，。\-—/\\\n\t()（）]')


def parse_name(n):
    n = REGEX_PUNCTUATION.sub('', str(n)).lower()
    return n


def text_to_variable(text):
    text = re.sub('[ \-]', '_', text)
    text = re.sub('[()]', '', text)
    return text


@dataclass
class Keyword:
    id: int
    cn: str
    en: str
    jp: str
    cht: str

    """
    Instance attributes and methods
    """

    @cached_property
    def cn_parsed(self) -> str:
        return parse_name(self.cn)

    @cached_property
    def en_parsed(self) -> str:
        return parse_name(self.en)

    @cached_property
    def jp_parsed(self) -> str:
        return parse_name(self.jp)

    @cached_property
    def cht_parsed(self) -> str:
        return parse_name(self.cht)

    @cached_property
    def name(self) -> str:
        return text_to_variable(self.en)

    def __str__(self):
        return self.name

    __repr__ = __str__

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.name)

    def __bool__(self):
        return True

    def _keywords_to_find(self, in_current_server=False, ignore_punctuation=True):
        if in_current_server:
            match server.server:
                case 'cn':
                    if ignore_punctuation:
                        return [self.cn_parsed]
                    else:
                        return [self.cn]
                case 'en':
                    if ignore_punctuation:
                        return [self.en_parsed]
                    else:
                        return [self.en]
                case 'jp':
                    if ignore_punctuation:
                        return [self.jp_parsed]
                    else:
                        return [self.jp]
                case 'tw':
                    if ignore_punctuation:
                        return [self.cht_parsed]
                    else:
                        return [self.cht]
        else:
            if ignore_punctuation:
                return [
                    self.cn_parsed,
                    self.en_parsed,
                    self.jp_parsed,
                    self.cht_parsed,
                ]
            else:
                return [
                    self.cn,
                    self.en,
                    self.jp,
                    self.cht,
                ]

    """
    Class attributes and methods
    """

    instances: ClassVar = {}

    def __post_init__(self):
        self.__class__.instances[self.id] = self

    @classmethod
    def find(cls, name, in_current_server=False, ignore_punctuation=True):
        """
        Args:
            name: Name in any server or instance id.
            in_current_server: True to search the names from current server only.
            ignore_punctuation: True to remove punctuations and turn into lowercase before searching.

        Returns:
            Keyword instance.

        Raises:
            ScriptError: If nothing found.
        """
        # Already a keyword
        if isinstance(name, Keyword):
            return name
        # Probably an ID
        if isinstance(name, int) or (isinstance(name, str) and name.isdigit()):
            try:
                return cls.instances[int(name)]
            except KeyError:
                pass

        if ignore_punctuation:
            name = parse_name(name)
        else:
            name = str(name)
        instance: Keyword
        for instance in cls.instances.values():
            for keyword in instance._keywords_to_find(
                    in_current_server=in_current_server, ignore_punctuation=ignore_punctuation):
                if name == keyword:
                    return instance

        raise ScriptError(f'Cannot find a {cls.__name__} instance that matches "{name}"')
