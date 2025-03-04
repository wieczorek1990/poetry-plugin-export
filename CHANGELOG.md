# Change Log

## [1.0.4] - 2022-05-26

### Fixed

- Fixed an issue where the exported dependencies did not list their active extras. [#65](https://github.com/python-poetry/poetry-plugin-export/pull/65)

## [1.0.3] - 2022-05-23

This release fixes test suite compatibility with upcoming Poetry releases. No functional changes.

## [1.0.2] - 2022-05-10

### Fixed

- Fixed an issue where the exported hashes were not sorted. [#54](https://github.com/python-poetry/poetry-plugin-export/pull/54)

### Changes

- The implicit dependency group was renamed from "default" to "main". (Requires poetry-core > 1.1.0a7 to take effect.) [#52](https://github.com/python-poetry/poetry-plugin-export/pull/52)


## [1.0.1] - 2022-04-11

### Fixed

- Fixed a regression where export incorrectly always exported default group only. [#50](https://github.com/python-poetry/poetry-plugin-export/pull/50)

## [1.0.0] - 2022-04-05

### Fixed

- Fixed an issue with dependency selection when duplicates exist with different markers. [poetry#4932](https://github.com/python-poetry/poetry/pull/4932)
- Fixed an issue where unconstrained duplicate dependencies are listed with conditional on python version. [poetry#5141](https://github.com/python-poetry/poetry/issues/5141)

### Changes

- Export command now constraints all exported dependencies with the root project's python version constraint. [poetry#5156](https://github.com/python-poetry/poetry/pull/5156)

### Added

- Added support for `--without-urls` option. [poetry#4763](https://github.com/python-poetry/poetry/pull/4763)


## [0.2.1] - 2021-11-24

### Fixed

- Fixed the output for packages with markers. [#13](https://github.com/python-poetry/poetry-plugin-export/pull/13)
- Check the existence of the `export` command before attempting to delete it. [#18](https://github.com/python-poetry/poetry-plugin-export/pull/18)


## [0.2.0] - 2021-09-13

### Added

- Added support for dependency groups. [#6](https://github.com/python-poetry/poetry-plugin-export/pull/6)


[Unreleased]: https://github.com/python-poetry/poetry-plugin-export/compare/1.0.4...main
[1.0.4]: https://github.com/python-poetry/poetry-plugin-export/compare/1.0.4
[1.0.3]: https://github.com/python-poetry/poetry-plugin-export/compare/1.0.3
[1.0.2]: https://github.com/python-poetry/poetry-plugin-export/compare/1.0.2
[1.0.1]: https://github.com/python-poetry/poetry-plugin-export/compare/1.0.1
[1.0.0]: https://github.com/python-poetry/poetry-plugin-export/compare/1.0.0
[0.2.1]: https://github.com/python-poetry/poetry-plugin-export/compare/0.2.1
[0.2.0]: https://github.com/python-poetry/poetry-plugin-export/compare/0.2.0
