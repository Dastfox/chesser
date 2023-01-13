from tinydb import TinyDB as tiny, where
from pathlib import Path


class Database:
    def export_to_db(data: dict, table_name: str, db_name="db"):
        db = tiny("{}.json".format(db_name))
        table = db.table(table_name)
        # table.truncate()
        if table_name == "players":
            data.sort(key=lambda x: x["lastname"])
        table.insert_multiple(data)

    def read_db(table: str, db_name="db"):
        db = tiny("{}.json".format(db_name))
        list = db.table(table)
        return list.all()

    def update_by_name(name: str, updated_data: dict, table_name: str, db_name="db"):
        # print("Updating {} in {}...".format(name, table_name), updated_data)
        db = tiny("{}.json".format(db_name))
        table = db.table(table_name)
        obj = table.search(where("name") == name)
        if obj:
            obj = obj[0]
            for player in updated_data["players"]:
                if player not in obj["players"]:
                    obj["players"].append(player)
            obj["players"].sort(key=lambda x: x["lastname"])
            del updated_data["players"]

            obj.update(updated_data)
            table.update(obj)
        else:
            print("No object found with the name: ", name)
