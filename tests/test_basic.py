import pytest
from config.config import config_parser, config_parser_section, load_file
from search_engines.shodan_se import shodan_search
from search_engines.zoomeye_se import zoomeye_search


def test_config_parser():
    result = config_parser("misp","url")
    assert len(result) > 0


def test_config_parser_section():
    result = config_parser_section("misp")
    assert len(result) > 0


def test_software_list():
    result = load_file('dorks.txt')
    assert len(result) > 0
