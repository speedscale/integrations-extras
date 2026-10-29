import pytest

from datadog_checks.zabbix import ZabbixCheck


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_supported_server_api(instance_e2e):
    config = instance_e2e
    check = ZabbixCheck('zabbix', {}, [config])
    token = check.login(config['zabbix_user'], config['zabbix_password'], config['zabbix_api'])
    assert token
    try:
        assert isinstance(check.get_hosts(token, config['zabbix_api']), list)
    finally:
        assert check.logout(token, config['zabbix_api'])['result'] is True
