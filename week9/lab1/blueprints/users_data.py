USERS = {
    1: {"first_name": "Van", "last_name": "Nguyen", "email": "a@vnu.vn"},
    2: {"first_name": "Trang", "last_name": "Tran", "email": "b@vnu.vn"}
}


def get_user(uid):
    return USERS.get(uid)


def add_user(first_name, last_name, email):
    uid = max(USERS, default=0) + 1
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }
    USERS[uid] = user
    return uid, user