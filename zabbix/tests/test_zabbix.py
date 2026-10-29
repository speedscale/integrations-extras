import json
from unittest.mock import patch

import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.zabbix import ZabbixCheck


def test_empty_instance(aggregator, instance_empty):
    check = ZabbixCheck('zabbix', {}, [instance_empty])

    with pytest.raises(ConfigurationError):
        check.check(instance_empty)


def test_missing_pass(aggregator, instance_missing_pass):
    check = ZabbixCheck('zabbix', {}, [instance_missing_pass])

    with pytest.raises(ConfigurationError):
        check.check(instance_missing_pass)


def test_missing_url(aggregator, instance_missing_url):
    check = ZabbixCheck('zabbix', {}, [instance_missing_url])

    with pytest.raises(ConfigurationError):
        check.check(instance_missing_url)


@pytest.mark.parametrize(
    'responses, expected_keys, expected_token',
    [
        ([{'result': 'token'}], ['username'], 'token'),
        ([{'error': {'code': -32602, 'data': 'Invalid parameter "/": unexpected parameter "username".'}},
          {'result': 'legacy-token'}], ['username', 'user'], 'legacy-token'),
        ([{'error': {'code': -32602, 'data': 'Incorrect user name or password.'}}], ['username'], None),
    ],
)
def test_login_parameter_compatibility(responses, expected_keys, expected_token):
    check = ZabbixCheck('zabbix', {}, [{}])
    with patch.object(check, 'request', side_effect=responses) as request:
        assert check.login('Admin', 'password', 'http://localhost/api_jsonrpc.php') == expected_token
    assert request.call_count == len(expected_keys)
    for call, key in zip(request.call_args_list, expected_keys):
        assert json.loads(call.args[1])['params'] == {key: 'Admin', 'password': 'password'}
