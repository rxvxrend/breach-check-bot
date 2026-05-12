from services.checkers.password_checker import PasswordChecker
from services.checkers.email_checker import EmailChecker
from services.checkers.username_checker import UsernameChecker

CHECKERS = {
    "password": PasswordChecker(),
    "email": EmailChecker(),
    "username": UsernameChecker(),
}


def get_checker(check_type):
    return CHECKERS.get(check_type)