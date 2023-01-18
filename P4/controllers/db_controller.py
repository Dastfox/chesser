from tinydb import TinyDB as tiny, where


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
        db = tiny("{}.json".format(db_name))
        table = db.table(table_name)
        obj = table.search(where("name") == name)
        if obj:
            obj = obj[0]
            for updated_player in updated_data["players"]:
                for i, obj_player in enumerate(obj["players"]):
                    if obj_player['firstname'] == updated_player['firstname'] and obj_player['lastname'] == updated_player['lastname']:
                        obj["players"][i] = updated_player
                        break
            obj["players"].sort(key=lambda x: x["lastname"])
            del updated_data["players"]

            obj.update(updated_data)
            table.update(obj)
        else:
            print("No object found with the name: ", name)
