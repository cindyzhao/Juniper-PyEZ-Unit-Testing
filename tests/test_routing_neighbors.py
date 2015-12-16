"""Test PyEZ Example Module

:Organization:  Juniper Networks
:Copyright:     Juniper Networks

:Author:  Christian Giese
:Contact: cgiese@juniper.net

:Date:    12/16/2015
:Version: 0.1
"""
from __future__ import unicode_literals
from pyez_mock import rpc_replys, mocked_device
from routing_neighbors import Neighbors
from lxml import etree
import os

# ------------------------------------------------------------------------------
# test functions
# ------------------------------------------------------------------------------


def test_bind_to_pyez_dev(mocked_device):
    """bind istance of neighbors to device """
    mocked_device.bind(neighbors=Neighbors)
    assert mocked_device.neighbors.display


def test_isis(mocked_device):
    """isis adjacencys"""
    isis = mocked_device.neighbors.isis
    assert len(isis) == 3


def test_isis_dynamic(mocked_device, rpc_replys):
    """isis with dynamic reply"""
    # read rpc-reply from file
    rpc_request = 'get-isis-adjacency-information'
    fname = os.path.join(os.path.dirname(__file__), 'rpc-reply', rpc_request + '.xml')
    with open(fname, 'r') as f:
        xml = etree.fromstring(f.read())
    # updated rpc-reply (delete first adjacency)
    xml[0].remove(xml[0][0])
    # store in rpc_replys fixture
    rpc_replys[rpc_request] = etree.tostring(xml)
    # get isis neighbors and check if number has decreased from 3 to 2
    isis = mocked_device.neighbors.isis
    assert len(isis) == 2
