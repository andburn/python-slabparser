import pytest
import mojoshader
import shaderlab
from test_helper import *


@pytest.fixture
def notags_blob():
	return shaderlab.Blob(read_data("notags.blob"))


@pytest.fixture
def tags_blob():
	return shaderlab.Blob(read_data("tags.blob"))


def test_notags_blob(notags_blob):
	assert len(notags_blob.shaders) == 2
	print(notags_blob.shaders)
	tag0, data0 = notags_blob.shaders[0]
	tag1, data1 = notags_blob.shaders[1]
	assert len(tag0) == 0
	assert len(tag1) == 0
	assert len(data0) == 236
	assert len(data1) == 160


def test_tags_blob(tags_blob):
	assert len(tags_blob.shaders) == 2
	print(tags_blob.shaders)
	tag0, data0 = tags_blob.shaders[0]
	tag1, data1 = tags_blob.shaders[1]
	assert len(tag0) == 0
	assert len(tag1) == 1
	assert tag1[0] == "LOW"
	assert len(data0) == 236
	assert len(data1) == 224
