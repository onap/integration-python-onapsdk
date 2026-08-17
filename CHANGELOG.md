# Python ONAP SDK Changelog

## v14.6.0

There is no 14.5.0 release. The release pipeline had already staged a 14.5.0
artifact built before any of the changes below, and the index it stages to
rejects re-uploads of a version that exists, so the version was skipped.

### Added

- `Acm` class for the CLAMP automation composition management runtime API
  (commission, prime, instantiate, deploy and the matching teardown calls).
- `Policy.get_policy_status` for the PAP policy deployment status endpoint.
- `CLAMP_ACM_URL` setting pointing at the in-cluster runtime-acm service.

### Changed

- Merge builds now publish their snapshot under a PEP 440 development version
  derived from the Jenkins build number, for example `14.6.0.dev123`, so a merge
  no longer fails once a version has been staged. Cutting a release now needs the
  clean version staged with a `stage-release` comment first, because the release
  job downloads that exact version rather than building it; see the README.
- Every function and method in the package now carries a return annotation, so
  type checkers no longer skip their bodies. This is an annotation-only change
  with one exception: `OnapService.get_guis` is declared as returning `GuiList`,
  the type all of its overrides already returned.

### Fixed

- `DeletionRequest.send_request` and its `VfModuleDeletionRequest` and
  `NetworkDeletionRequest` overrides declared return types that were wrong:
  `Deletion` and `VfModuleDeletion` do not exist at all, and the network
  variant claimed `VnfDeletionRequest`. Each now names the class it actually
  returns. Type hints only; the objects returned are unchanged.
- 48 docstrings documented a parameter or return type that disagreed with the
  annotation, including `[type]` placeholders on the six
  `update_informations_from_sdc*` methods and `platform`/`project` in
  `onapsdk.so.instantiation`, which take a name string rather than the
  `Platform`/`Project` object the docstrings named.
- `onapsdk.so.instantiation` could not be imported before another `onapsdk`
  module: an import cycle through the eager re-exports in
  `onapsdk.aai.business` raised `ImportError`. The A&AI business re-exports are
  now resolved lazily; the package exposes the same names as before.

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
