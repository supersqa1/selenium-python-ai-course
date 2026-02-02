# Scripts

Standalone scripts for test data setup. Run from **project root**.

## create_user_with_one_order.py

Creates a WooCommerce customer with one completed order. Use for My Account Orders tab tests (e.g. TC-157, `user_with_one_order`).

**Requirements:** `.env` with `API_KEY`, `API_SECRET`, `ENV` (and optionally `DB_*` if other helpers are used).

**Run:**
```bash
python scripts/create_user_with_one_order.py
```

**Then:** Add the printed `USER_WITH_ONE_ORDER_USERNAME` and `USER_WITH_ONE_ORDER_PASSWORD` lines to your `.env` file.
