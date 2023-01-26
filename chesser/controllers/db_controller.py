
from tinydb import TinyDB as tiny, where


class Database:
    @staticmethod
    def export_to_db(data: list[dict], table_name: str, db_name="db"):
        db = tiny("{}.json".format(db_name))
        table = db.table(table_name)
        # table.truncate()
        if table_name == "players":
            data.sort(key=lambda x: x["lastname"])
        table.insert_multiple(data)

    @staticmethod
    def read_db(table: str, db_name="db"):
        db = tiny("{}.json".format(db_name))
        list = db.table(table)
        return [dict(i) for i in list.all()]

    @staticmethod
    def update_db_object(
        name: str, updated_data: dict, table_name: str, db_name="db"
    ):
        db = tiny("{}.json".format(db_name))
        table = db.table(table_name)
        table.update(updated_data, where("name") == name)

    @staticmethod
    def delete_db_object(name: str, table_name: str, db_name="db"):
        db = tiny("{}.json".format(db_name))
        table = db.table(table_name)
        table.remove(where("name") == name)
