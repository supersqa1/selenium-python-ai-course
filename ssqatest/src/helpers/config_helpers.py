

import os

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
