from .connection import get_db_connection
from typing import Optional


class UserData:
    def get_user_group(self, user_id: int) -> Optional[int]:
        """
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT group_id FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
        connection.close()
        return result[0] if result else None
    
    def set_user_group(self, user_id: int, group_id: int) -> None:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO Users (user_id, group_id) VALUES (?, ?)
                          ON CONFLICT(user_id) 
                          DO UPDATE SET 
                            group_id = excluded.group_id
                       """, (user_id, group_id))
        connection.commit()
        connection.close()

    def delet_user(self, user_id: int) -> None:
        """
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))

        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

