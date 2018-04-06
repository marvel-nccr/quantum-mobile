import pytest

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_mimeapps_file_permissions(File):
    config = File('/etc/xdg/ansible-default-web-browser/mimeapps.list')

    assert config.exists
    assert config.is_file
    assert config.user == 'root'
    assert config.group == 'root'
    assert oct(config.mode) == '0644'


@pytest.mark.parametrize('expected', [
    'text/html=google-chrome.desktop',
    'x-scheme-handler/http=google-chrome.desktop',
    'x-scheme-handler/https=google-chrome.desktop',
    'x-scheme-handler/about=google-chrome.desktop',
    'x-scheme-handler/unknown=google-chrome.desktop'
])
def test_mimeapps_file(File, expected):
    config = File('/etc/xdg/ansible-default-web-browser/mimeapps.list')

    assert config.exists
    assert config.is_file
    assert config.contains(expected)
