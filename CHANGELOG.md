# Python ONAP SDK Changelog

## v14.5.0

### Added

- `Acm` class for the CLAMP automation composition management runtime API
  (commission, prime, instantiate, deploy and the matching teardown calls).
- `Policy.get_policy_status` for the PAP policy deployment status endpoint.
- `CLAMP_ACM_URL` setting pointing at the in-cluster runtime-acm service.

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
