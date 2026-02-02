#!/usr/bin/env python3
"""
Data-setup script: creates a customer with one completed order for My Account Orders tab tests.

Run from project root (where .env and ssqatest/ live). Requires .env with API_KEY, API_SECRET, ENV.

Usage:
  python scripts/create_user_with_one_order.py

Then add the printed lines to your .env file (USER_WITH_ONE_ORDER_USERNAME, USER_WITH_ONE_ORDER_PASSWORD).
"""

import os
import sys

# Load .env before importing helpers that use os.environ
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)
else:
    print("Warning: .env not found. Set API_KEY, API_SECRET, ENV before running.", file=sys.stderr)

# Ensure project root is on path
sys.path.insert(0, str(project_root))

from ssqatest.src.helpers.api_helpers import create_customer, create_order_for_customer


def main():
    print("Creating customer and one completed order...")
    customer = create_customer()
    create_order_for_customer(customer["id"])
    print("Done. Add these lines to your .env file:\n")
    print(f"USER_WITH_ONE_ORDER_USERNAME={customer['email']}")
    print(f"USER_WITH_ONE_ORDER_PASSWORD={customer['password']}")


if __name__ == "__main__":
    main()
