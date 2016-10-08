# Integration tests for the libvirt/bhyve driver

This is a very basic tests to ensure that libvirt/bhyve is operational.

It defines and boots domains, and checks that it's accessible through SSH.
It also checks some host-level commands (nodeinfo etc).

The goal is too get a reasonable coverage for all the features provided
by libvirt/bhyve or libvirt on FreeBSD in general to increase stability of libvirt
for FreeBSD users.

# Prerequisites

Tests assume libvirt is running and that the `default` network is started.

# Running tests

Tests are designed to be executed using `tox`; out-of-tree execution is not supported.
One should edit `test.ini` to specify connection URI and image information.

To run all the tests:

```tox -epy27```

To run specific tests:

```tox -epy27 -- tests.host_test```
