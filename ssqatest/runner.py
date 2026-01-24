import pytest
import argparse
import os
import logging as logger

def add_drivers_to_path():
    pass


if __name__ == '__main__':
    pytest_arguments = ['tests']
    parser = argparse.ArgumentParser()

    parser.add_argument('--mark_to_run', required=False,
                        help='')
    parser.add_argument('--html', required=False,
                        help='Path to html report. Relative to the "runner.py" script.')
    parser.add_argument('--allure_dir', required=False,
                        help='Path to html report. Relative to the "runner.py" script.')

    args = parser.parse_args()
    mark_to_run = args.mark_to_run
    html = args.html
    allure_dir = args.allure_dir


    if mark_to_run:
        pytest_arguments.append(f'-m {mark_to_run}')

    if html:
        # if the html argument is passed then html report needs to be generated
        os.environ['HTML_REPORT_USED'] = 'true'
        result_dir = os.environ.get('RESULTS_DIR')
        pytest_arguments.append(f'--html={result_dir}/{html} --self-contained-html')
        print(f"pytest-html report will be: {html}")

    if allure_dir:
        # if 'allure_dir' argument is passed then allure report needs to be generated
        os.environ['ALLURE_USED'] = 'true'
        pytest_arguments.append(f'--alluredir={allure_dir}')
        print(f"Allure report will be: {allure_dir}")


    # run tests
    abc = pytest.main(pytest_arguments)
    print(pytest_arguments)
    print("*****")
    print(abc)
    print("*****")