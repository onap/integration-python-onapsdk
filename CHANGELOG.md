# Python ONAP SDK Changelog

## v14.4.0

### Added

- add opentelemetry `@tracer` decorator to `Service.distributions` method

### Removed

- remove dependency on `cryptography` and `pyOpenSSL` since they are not
  actually used in the project

## v1.0

[Documentation](https://readthedocs.org/dashboard/python-onapsdk/version/v1.0)

Main new features:

- Onboard a simple service via SDC
- Instantiate a simple service via SO using GR API
- Instantiate a simple service via NBI
- create business objects in AAI
