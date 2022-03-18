import os

TG_TOKEN_TEST = ""
TG_TOKEN_PROD = ""

ADMIN_TG_ID = 0

def is_prod():
    if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
        return False
    else:
        return True


def get_tg_token():
    return TG_TOKEN_PROD if is_prod() else TG_TOKEN_TEST

def get_id_admin():
    return ADMIN_TG_ID
