from services.checkers.password_checker import PasswordChecker
from services.checkers.email_checker import EmailChecker

CHECKERS = {
    "password": PasswordChecker(),
    "email": EmailChecker(),
}


def get_checker(check_type):
    return CHECKERS.get(check_type)