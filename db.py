users = [{
    "email": "user1234@gmail.com",
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlcjEyMzQifQ.w5Tp8LQ8CawGKh2zjyrnejyWKGhXIaP9KdHnKPm-Adg",
    "pw_hash": "$2b$12$fpqn409/iL6qVc/X5mcg0.arh8as/94xY6zxuvCSe8hH0OQ/3VL0S",
    "user_id": "user1234"
},{
    "email": "user1235@gmail.com",
    "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlcjEyMzUifQ.tMwBJ5OgFTM8d1l4CjzlOJGa-Npu-zwkU195tDmXl3A",
    "pw_hash": "$2b$12$X9hDYBie3rbf3fzY9Ds7muE6vwfSqe3B7y5MqRPlI1Aj4rrfjIXI6",
    "user_id": "user1235"
}

]


def get_user_by_id(user_id):
    for user in users:
        if user_id == user['user_id']:
            return True
    return False


def get_user(email):
    for user in users:
        if user['email'] == email:
            return [user]

    return None
