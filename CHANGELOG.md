# Changelog

All notable changes to this project will be documented in this file.

## [0.0.3] - 2026-05-10

### Added
- CLI tool (`cli.py`) for Oracle Cloud instance management
  - `list` command: list all instances with table/JSON output
  - `info` command: view instance details
  - `start` command: start instance(s)
  - `stop` command: stop instance
  - `--account` filter for multi-account support
- `CLAUDE.md` documentation for Claude Code guidance
- `OracleInstance` dataclass with `instance_id` and `account_index` fields
- Logging configuration across all modules
- Type annotations for all functions

### Changed
- **oracle_sdk/oracle_cloud.py**
  - Renamed `start_stopped_insance` to `start_instance` (typo fix)
  - Added return values for `start_instance` and `stop_instance`
  - Added `_create_oracle_instance` helper function to reduce code duplication
  - Added proper exception handling with logging
  - Added `oci.exceptions.ServiceError` specific handling
- **model/model.py**
  - Converted to `@dataclass` for cleaner code
  - Added `to_dict()` method using `asdict()`
- **notion_sdk/notion_api.py**
  - Replaced multiple `if` statements with dictionary mapping
  - Removed `sys.path.append(os.getcwd())` (bad practice)
  - Added proper docstrings and type annotations
- **notion_sdk/databases.py**
  - Removed `sys.path.append(os.getcwd())`
  - Added `response.raise_for_status()` for proper error handling
  - Added type annotations and improved docstrings
- **conf/config.py**
  - Changed from `os.getcwd()` to `__file__` relative path (more reliable)
  - Changed from `yaml.load` to `yaml.safe_load` (security best practice)
  - Added lazy loading pattern with global state management
- **requirements.txt**
  - Updated PyYAML from `5.4.1` to `>=6.0` for Python 3.13 compatibility

### Fixed
- PyYAML compatibility issue with Python 3.13
- `--account 0` parameter not working due to falsy value check
- Silent exception handling - now logs errors properly
- Unused variables (`response`, `wait_until_response`, `e`)
- Missing return values in instance action functions