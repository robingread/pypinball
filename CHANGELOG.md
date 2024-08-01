# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Updated the `Scoring` class to include `set_score()` and `reset()` methods to make it easier to reset everything without needing to create a new instance of the `Scoring` class.
- Added the `set_lives()` method to the `Lives` class to allow setting of the value without needing to create a new instance of the class.
- Added the `pypinball.physics.utils` module with a `remove_all_balls()` helper function.

### Fixed

- Fixed the profiling script (`./scripts/profile-game.sh`) so that this works properly.

## v0.0.1 - 2024/2/12

### Added

- Initial development release. Basic working version of the `pypinball` project. Very much rough around the edges, but should be enough to get it working with an external project (just about).
