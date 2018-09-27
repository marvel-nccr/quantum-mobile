import pytest
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_helpers_file_permissions(host):
    config = host.file('/etc/xdg/ansible-default-web-browser/xfce4/helpers.rc')

    assert config.exists
    assert config.is_file
    assert config.user == 'root'
    assert config.group == 'root'
    assert oct(config.mode) == '0644'
    assert config.contains('WebBrowser=google-chrome')


def test_desktop_file_permissions(host):
    helper_dir = '/etc/xdg/ansible-default-web-browser/xfce4/helpers'
    desktop = host.file(helper_dir + '/google-chrome.desktop')

    assert desktop.exists
    assert desktop.is_file
    assert desktop.user == 'root'
    assert desktop.group == 'root'
    assert oct(desktop.mode) == '0644'


@pytest.mark.parametrize('expected', [
    'Type=X-XFCE-Helper',
    'X-XFCE-Category=WebBrowser',
    'X-XFCE-Commands=/usr/bin/google-chrome-stable',
    'X-XFCE-CommandsWithParameter=/usr/bin/google-chrome-stable "%s"'
])
def test_desktop_file(host, expected):
    helper_dir = '/etc/xdg/ansible-default-web-browser/xfce4/helpers'
    desktop = host.file(helper_dir + '/google-chrome.desktop')

    assert desktop.exists
    assert desktop.is_file
    assert desktop.contains(expected)
