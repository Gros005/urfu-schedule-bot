from .database.user_data import UserData

def main():
    db_conection = UserData()
    db_conection.set_user_group(user_id=123456, group_id=34567)

    respons = db_conection.get_user_group(user_id=123456)
    print(respons)
    db_conection.delet_user(user_id=123456)
    respons = db_conection.get_user_group(user_id=123456)
    print(respons)



