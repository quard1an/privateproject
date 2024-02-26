import pytest
from unittest.mock import Mock, patch

from client.client import create_or_delete_group_on_cluster


pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
@patch('client.client.send_create_request')
async def test_client_creation_passed(mock_object):
	mock_object.return_value = Mock()
	mock_object.return_value.status_code = 201
	result = await create_or_delete_group_on_cluster(["test1", "test2"], "group_id", "create")
	assert result


@pytest.mark.asyncio
@patch('client.client.send_create_request')
async def test_client_creation_rollback(mock_object):
	mock_object.return_value = Mock()
	mock_object.return_value.status_code = 400
	result = await create_or_delete_group_on_cluster(["test1", "test2"], "group_id", "create")
	assert not result


@pytest.mark.asyncio
@patch('client.client.send_delete_request')
async def test_client_deletion_passed(mock_object):
	mock_object.return_value = Mock()
	mock_object.return_value.status_code = 200
	result = await create_or_delete_group_on_cluster(["test1", "test2"], "group_id", "delete")
	assert result


@pytest.mark.asyncio
@patch('client.client.send_delete_request')
async def test_client_deletion_rollback(mock_object):
	mock_object.return_value = Mock()
	mock_object.return_value.status_code = 400
	result = await create_or_delete_group_on_cluster(["test1", "test2"], "group_id", "delete")
	assert not result
