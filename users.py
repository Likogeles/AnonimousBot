import sqlite3
from user import User


class UsersList:

    _usersList = []

    def __init__(self):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE users(id, first_name, second_name)")
        except Exception:
            pass

        result = list(cur.execute("SELECT * FROM users;").fetchall())

        for i in result:
            self._usersList.append(User(int(i[0]), i[1], i[2]))

        con.close()

    def addUser(self, new_user):
        self._usersList.append(new_user)
        con = sqlite3.connect("users.db")
        cur = con.cursor()

        cur.execute(f"""INSERT INTO users VALUES('{new_user.getId()}', '{new_user.getFirstName()}', '{new_user.getSecondName()}')""")
        con.commit()
        con.close()

    def getUserById(self, id) -> User | None:
        for i in self._usersList:
            if i.getId() == id:
                return i
        return None

    def __str__(self):
        usersStr = ""
        for i in self._usersList:
            usersStr += f"{i.getId()}: {i.getFirstName()} {i.getSecondName()}\n"
        return usersStr
