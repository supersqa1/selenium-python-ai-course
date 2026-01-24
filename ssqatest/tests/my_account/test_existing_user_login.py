
import pytest
from ssqatest.src.helpers.api_helpers import create_user
from ssqatest.src.pages.MyAccountSignedOut import MyAccountSignedOut

@pytest.mark.usefixtures('init_driver')
class TestExistingUserLogin:

    @pytest.mark.xxy
    def test_existing_user_login(self):
        my_acct_singed_out = MyAccountSignedOut(self.driver)

        user_info = create_user()
        my_acct_singed_out.go_to_my_account()
        my_acct_singed_out.input_login_username(username=user_info['email'])
        my_acct_singed_out.input_login_password(password=user_info['password'])
        my_acct_singed_out.click_login_button()