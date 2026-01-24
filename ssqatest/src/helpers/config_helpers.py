

import os
import sys

def validate_environment():
    """
    Validates environment variables at framework startup.
    Checks required variables and warns about missing optional variables.
    Raises EnvironmentError if critical variables are missing.
    """
    errors = []
    warnings = []
    
    # Required variables (framework won't work without these)
    required_vars = {
        'BROWSER': {
            'description': 'Browser to use for tests',
            'options': 'chrome, firefox, headlesschrome, headlessfirefox',
            'example': 'export BROWSER=chrome'
        },
        'RESULTS_DIR': {
            'description': 'Directory for test results and reports',
            'example': 'export RESULTS_DIR=./results'
        }
    }
    
    # Optional variables (needed for specific test types)
    optional_vars = {
        'API_KEY': {
            'description': 'WooCommerce API key (required for API tests)',
            'test_type': 'API-related tests',
            'example': 'export API_KEY=ck_...'
        },
        'API_SECRET': {
            'description': 'WooCommerce API secret (required for API tests)',
            'test_type': 'API-related tests',
            'example': 'export API_SECRET=cs_...'
        },
        'DB_USER': {
            'description': 'Database username (required for database tests)',
            'test_type': 'Database-related tests',
            'example': 'export DB_USER=root'
        },
        'DB_PASSWORD': {
            'description': 'Database password (required for database tests)',
            'test_type': 'Database-related tests',
            'example': 'export DB_PASSWORD=root'
        }
    }
    
    # Check required variables
    missing_required = []
    for var_name, var_info in required_vars.items():
        value = os.environ.get(var_name)
        if not value:
            missing_required.append(var_name)
            errors.append(
                f"   ❌ {var_name}: {var_info['description']}\n"
                f"      Example: {var_info.get('example', 'N/A')}"
            )
    
    # Check optional variables
    missing_optional = []
    for var_name, var_info in optional_vars.items():
        value = os.environ.get(var_name)
        if not value:
            missing_optional.append(var_name)
            warnings.append(
                f"   ⚠️  {var_name}: {var_info['description']}\n"
                f"      Needed for: {var_info.get('test_type', 'N/A')}\n"
                f"      Example: {var_info.get('example', 'N/A')}"
            )
    
    # Build error message
    if errors:
        error_msg = "❌ Missing required environment variables:\n\n"
        error_msg += "\n".join(errors)
        error_msg += "\n\n"
        error_msg += "To fix:\n"
        error_msg += "   1. Create a .env file in the project root (copy from .env.example)\n"
        error_msg += "   2. Or set manually: export BROWSER=chrome export RESULTS_DIR=./results\n"
        error_msg += "   3. Or source env.sh: source env.sh\n"
        
        if warnings:
            error_msg += "\n"
            error_msg += "⚠️  Also missing optional variables (some tests may fail):\n\n"
            error_msg += "\n".join(warnings)
            error_msg += "\n"
            error_msg += "   These are optional but required for specific test types.\n"
        
        raise EnvironmentError(error_msg)
    
    # Show warnings if optional vars are missing (but don't fail)
    if warnings:
        warning_msg = "⚠️  Missing optional environment variables (some tests may fail):\n\n"
        warning_msg += "\n".join(warnings)
        warning_msg += "\n"
        warning_msg += "   These are optional but required for specific test types.\n"
        warning_msg += "   To fix: Add them to your .env file or set them manually.\n"
        print(warning_msg, file=sys.stderr)
    
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
            f"   Set via: export ENV=test (defaults to 'test' if not set)"
        )

    db_info = {"db_host": db_host, "db_port": db_port,
               "db_user": db_user, "db_password": db_password}

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
