import os

import pytest

from datadog_checks.dev import docker_run, get_docker_hostname, get_here
from datadog_checks.dev.conditions import WaitFor
from datadog_checks.zabbix import ZabbixCheck

HERE = get_here()
HOST = get_docker_hostname()

CONFIG = {
    'zabbix_user': 'Admin',
    'zabbix_password': 'zabbix',
    'zabbix_api': 'http://{}:8080/api_jsonrpc.php'.format(HOST),
}


def api_ready():
    check = ZabbixCheck('zabbix', {}, [CONFIG])
    token = check.login(CONFIG['zabbix_user'], CONFIG['zabbix_password'], CONFIG['zabbix_api'])
    if not token:
        return False
    return check.logout(token, CONFIG['zabbix_api']).get('result') is True


@pytest.fixture(scope="session")
def dd_environment():
    compose_file = os.path.join(HERE, 'compose', 'docker-compose.yml')
    with docker_run(
        compose_file=compose_file,
        service_name='zabbix-web',
        endpoints=[CONFIG['zabbix_api'].replace('/api_jsonrpc.php', '/')],
        conditions=[WaitFor(api_ready, attempts=60, wait=2)],
    ):
        yield CONFIG


@pytest.fixture(scope="session")
def instance_e2e():
    return CONFIG


@pytest.fixture(scope="session")
def instance_empty():
    instance = {}
    return instance


@pytest.fixture(scope="session")
def instance_missing_pass():
    instance = {"zabbix_user": "zabbix"}
    return instance


@pytest.fixture(scope="session")
def instance_missing_url():
    instance = {"zabbix_user": "zabbix", "zabbix_password": "zabbix"}
    return instance
