

import os
import sys

def validate_environment():
    """
    Validates environment variables at framework startup.
    All variables are required to fail fast and prevent partial test suite failures.
    Raises EnvironmentError if any required variables are missing.
    """
    # All required variables (fail fast approach for CI/CD and full test runs)
    required_vars = {
        'BROWSER': {
            'description': 'Browser to use for tests',
            'options': 'chrome, firefox, headlesschrome, headlessfirefox',
            'example': 'export BROWSER=chrome'
        },
        'RESULTS_DIR': {
            'description': 'Directory for test results and reports',
            'example': 'export RESULTS_DIR=./results'
        },
        'API_KEY': {
            'description': 'WooCommerce API key (required for API tests)',
            'example': 'export API_KEY=ck_...'
        },
        'API_SECRET': {
            'description': 'WooCommerce API secret (required for API tests)',
            'example': 'export API_SECRET=cs_...'
        },
        'DB_USER': {
            'description': 'Database username (required for database tests)',
            'example': 'export DB_USER=root'
        },
        'DB_PASSWORD': {
            'description': 'Database password (required for database tests)',
            'example': 'export DB_PASSWORD=root'
        }
    }
    
    # Check all required variables
    missing_vars = []
    error_details = []
    
    for var_name, var_info in required_vars.items():
        value = os.environ.get(var_name)
        if not value:
            missing_vars.append(var_name)
            error_details.append(
                f"   ❌ {var_name}: {var_info['description']}\n"
                f"      Example: {var_info.get('example', 'N/A')}"
            )
    
    # If any variables are missing, raise error with clear message
    if missing_vars:
        raise EnvironmentError(
            f"""❌ Missing required environment variables:

{chr(10).join(error_details)}

To fix:
   1. Create a .env file in the project root (copy from .env.example)
   2. Or set manually: export BROWSER=chrome export RESULTS_DIR=./results export API_KEY=... export API_SECRET=... export DB_USER=... export DB_PASSWORD=...
   3. Or source env.sh: source env.sh

Note: All variables are required to ensure full test suite can run. 
      If you only want to run specific tests, use pytest markers or test selection."""
        )
    
    return True

def get_base_url():

    env = os.environ.get('ENV', 'test')

    if env.lower() == 'test':
        return 'http://demostore.supersqa.com'
        # return 'http://127.0.0.1:8888/localdemostore/'
    elif env.lower() == 'prod':
        return 'http://demostore.prod.supersqa.com'
    else:
        raise ValueError(
            f"❌ Unknown environment: '{env}'\n"
            f"   Valid environments are: 'test', 'prod'\n"
            f"   Set via: export ENV=test (defaults to 'test' if not set)"
        )

def get_database_credentials():

    env = os.environ.get('ENV', 'test')

    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    if not db_user or not db_password:
        missing_vars = []
        if not db_user:
            missing_vars.append("DB_USER")
        if not db_password:
            missing_vars.append("DB_PASSWORD")
        
        raise EnvironmentError(
            f"❌ Missing required database credentials: {', '.join(missing_vars)}\n"
            f"   These are required for database-related tests.\n"
            f"   \n"
            f"   To fix:\n"
            f"   1. Source the environment file: source env.sh\n"
            f"   2. Or set manually: export DB_USER=... export DB_PASSWORD=...\n"
            f"   3. Or create a .env file with these variables"
        )

    # Check if DB_HOST and DB_PORT are explicitly set (takes precedence over ENV defaults)
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    
    if db_host and db_port:
        # Use explicit configuration (ENV is ignored when DB_HOST/DB_PORT are set)
        try:
            db_port = int(db_port)
        except ValueError:
            raise ValueError(
                f"❌ Invalid DB_PORT value: '{db_port}'\n"
                f"   DB_PORT must be a valid integer (e.g., 3306, 8889)"
            )
        # Debug: Show that explicit config is being used
        print(f"🔍 Using explicit database configuration: {db_host}:{db_port} (ENV={env} is ignored)")
    else:
        # Fall back to ENV-based defaults (backward compatibility)
        if env == 'test':
            db_host = '127.0.0.1'
            db_port = 8889
        elif env == 'prod':
            db_host = 'demostore.supersqa.com'
            db_port = 3306
        else:
            raise ValueError(
                f"❌ Unknown environment: '{env}'\n"
                f"   Valid environments are: 'test', 'prod'\n"
                f"   Set via: export ENV=test (defaults to 'test' if not set)\n"
                f"   Or set DB_HOST and DB_PORT explicitly to override ENV defaults"
            )
        # Debug: Show that ENV defaults are being used
        print(f"🔍 Using ENV-based database configuration: {db_host}:{db_port} (ENV={env})")

    # Get database name from environment, fallback to GenericConfigs for backward compatibility
    from ssqatest.src.configs.generic_configs import GenericConfigs
    db_name = os.environ.get("DB_NAME") or GenericConfigs.DATABASE_SCHEMA

    db_info = {"db_host": db_host, "db_port": db_port,
               "db_user": db_user, "db_password": db_password,
               "db_name": db_name}

    return db_info


def get_api_credentials():

    base_url = get_base_url()
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    if not all([api_key, api_secret]):
        missing_vars = []
        if not api_key:
            missing_vars.append("API_KEY")
        if not api_secret:
            missing_vars.append("API_SECRET")
        
        raise EnvironmentError(
            f"❌ Missing required API credentials: {', '.join(missing_vars)}\n"
            f"   These are required for API-related tests.\n"
            f"   \n"
            f"   To fix:\n"
            f"   1. Source the environment file: source env.sh\n"
            f"   2. Or set manually: export API_KEY=... export API_SECRET=...\n"
            f"   3. Or create a .env file with these variables"
        )

    return {'base_url': base_url, 'api_key': api_key, 'api_secret': api_secret}


def get_test_user(user_id: str):
    """
    Load a test user definition by id from configs/test_users.json and resolve
    credentials from environment variables (username_env / password_env).
    Use for tests that need a specific user type (e.g. my_account_smoke_user).

    Returns:
        dict with keys: id, description (optional), username, password

    Raises:
        FileNotFoundError: if test_users.json is missing
        ValueError: if user_id is not found in config
        EnvironmentError: if required username/password env vars are not set
    """
    import json
    from pathlib import Path

    configs_dir = Path(__file__).resolve().parent.parent / "configs"
    users_path = configs_dir / "test_users.json"
    if not users_path.exists():
        raise FileNotFoundError(
            f"Test users config not found: {users_path}\n"
            f"   Expected a JSON file with a 'users' array of objects containing id, username_env, password_env."
        )

    with open(users_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    users = data.get("users") or []
    user_def = next((u for u in users if u.get("id") == user_id), None)
    if not user_def:
        available = [u.get("id") for u in users if u.get("id")]
        raise ValueError(
            f"Test user '{user_id}' not found in test_users.json.\n"
            f"   Available user ids: {available}"
        )

    username_env = user_def.get("username_env")
    password_env = user_def.get("password_env")
    if not username_env or not password_env:
        raise ValueError(
            f"Test user '{user_id}' in test_users.json must define username_env and password_env."
        )

    username = os.environ.get(username_env)
    password = os.environ.get(password_env)
    if not username or not password:
        missing = []
        if not username:
            missing.append(username_env)
        if not password:
            missing.append(password_env)
        raise EnvironmentError(
            f"❌ Missing test user credentials for '{user_id}': {', '.join(missing)}\n"
            f"   Set in .env or export: {username_env}=... {password_env}=..."
        )

    return {
        "id": user_def.get("id"),
        "description": user_def.get("description"),
        "username": username,
        "password": password,
    }
