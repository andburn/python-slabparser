import pytest
import shaderlab
from helper import *


@pytest.fixture
def basic_shader():
	data = read_text_data("basic.shader")
	return shaderlab.parse(data)


@pytest.fixture
def uber_shader():
	data = read_text_data("uber.shader")
	return shaderlab.parse(data)


@pytest.fixture
def stripped_shader():
	data = read_text_data("stripped.shader")
	return shaderlab.parse(data)


def test_basic_shader_name(basic_shader):
	assert basic_shader.name == "Basic"


def test_basic_shader_structure(basic_shader):
	assert len(basic_shader.subshaders) == 1
	assert len(basic_shader.subshaders[0].passes) == 1
	assert len(basic_shader.subshaders[0].passes[0].programs) == 2


def test_basic_shader_vp(basic_shader):
	vp = basic_shader.vertex_programs
	assert len(vp) == 1
	assert vp[0].format == shaderlab.ProgramFormat.D3D9


def test_basic_shader_fp(basic_shader):
	fp = basic_shader.fragment_programs
	assert len(fp) == 1
	assert fp[0].format == shaderlab.ProgramFormat.D3D9


def test_basic_shader_properties(basic_shader):
	assert len(basic_shader.properties) == 2
	first = basic_shader.properties[0]
	assert first.name == "_MainTex"
	assert first.description == "Main Texture"
	assert first.type == "2D"
	assert first.value == "white"


def test_basic_shader_fallback(basic_shader):
	assert basic_shader.fallback.value == "Diffuse"


def test_uber_shader_name(uber_shader):
	assert uber_shader.name == "Uber"


def test_uber_shader_structure(uber_shader):
	assert len(uber_shader.subshaders) == 1
	assert len(uber_shader.subshaders[0].passes) == 1
	assert len(uber_shader.subshaders[0].passes[0].programs) == 2


def test_uber_shader_vp(uber_shader):
	vp = uber_shader.vertex_programs
	assert len(vp) == 2
	assert vp[1].format == shaderlab.ProgramFormat.D3D9
	assert set(["LYR4_COMBINE"]) == set(vp[1].keywords)


def test_uber_shader_fp(uber_shader):
	fp = uber_shader.fragment_programs
	assert len(fp) == 2
	assert fp[1].format == shaderlab.ProgramFormat.D3D9
	assert set(["LYR4", "BLENDALPHA_L3"]) == set(fp[1].keywords)


def test_uber_shader_properties(uber_shader):
	assert len(uber_shader.properties) == 4
	first = uber_shader.properties[0]
	assert first.name == "_MainTex"
	assert first.description == "Portrait (RGB)"
	assert first.type == "2D"
	assert first.value == "black"


def test_uber_shader_fallback(uber_shader):
	assert uber_shader.fallback.value == "Diffuse"
