# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Oracle Cloud instance management tool that monitors Oracle Cloud compute instances and automatically restarts stopped instances. Syncs instance status to a Notion database for visibility.

## Commands

```bash
# Install dependencies (use virtualenv)
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run the main script (sync instances to Notion)
python main.py

# CLI for OCI operations
python cli.py list                   # List all instances
python cli.py list --format json     # JSON output
python cli.py list --account 0       # Filter by account index
python cli.py info INSTANCE_ID       # Show instance details
python cli.py start INSTANCE_ID      # Start instance
python cli.py start --all-stopped    # Start all stopped instances
python cli.py stop INSTANCE_ID       # Stop instance
```

## Configuration

Copy `conf/config_sample.yaml` to `conf/config.yaml` and fill in:
- Notion integration token and database ID
- Oracle Cloud account credentials (user OCID, fingerprint, tenancy, region, compartment ID)
- PEM key files placed in `conf/file/`

## Architecture

```
cli.py                  # CLI entry point - argparse subcommands (list/start/stop/info)
main.py                 # Entry point - orchestrates the workflow
├── oracle_sdk/         # Oracle Cloud SDK wrapper
│   └── oracle_cloud.py  # Instance listing, IP retrieval, auto-start/stop functions
├── notion_sdk/         # Notion API client
│   ├── notion_api.py   # High-level: write instances to Notion (upsert logic)
│   └── databases.py    # Low-level: query, insert, update rows in Notion database
├── model/
│   └── model.py        # OracleInstance dataclass with to_dict()
└── conf/
    ├── config.py       # Loads config.yaml, exposes ACCOUNTS, NOTION_TOKEN, DATABASE_ID
    └── file/           # OCI API key PEM files
```

### Key Flow
1. `get_instance_from_account()` fetches all instances across configured OCI accounts
2. Stopped instances are automatically restarted via `start_stopped_insance()`
3. Instance data (IP, region, state, processor) is synced to Notion via `write_instance2notion()`
4. Notion sync uses upsert pattern: query by display_name, update existing or insert new

## Dependencies

- `oci` - Oracle Cloud Infrastructure SDK
- `python-telegram-bot` - Telegram integration (currently unused in main flow)
- `PyYAML` - Configuration parsing
- `requests` - HTTP calls to Notion API