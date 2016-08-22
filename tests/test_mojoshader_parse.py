import pytest
import mojoshader
from test_helper import *


@pytest.fixture
def parse_data():
	p = mojoshader.Parser()
	return p.parse(read_data("shader.cso"))


def test_error_count(parse_data):
	assert parse_data.error_count == 0


def test_profile(parse_data):
	assert parse_data.profile.decode("ascii") == "glsl"


def test_shader_type(parse_data):
	assert parse_data.shader_type == 2


def test_shader_output(parse_data):
	assert parse_data.output_len == 516
