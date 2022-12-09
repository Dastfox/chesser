from tinydb import TinyDB as tiny
from pathlib import Path

class Database:
    
    def export_to_db(data:dict, table_name:str,db_name="db"):
        db=tiny("{}.json".format(db_name))
        table=db.table(table_name)
        # table.truncate()
        table.insert_multiple(data)

    def import_from_db(table_name:str,db_name="db"):
        db=tiny("{}.json".format(db_name))
        table=db.table(table_name)
        return table.all()
    
    def read_db(table:str ,db_name="db"):
        db=tiny("{}.json".format(db_name))
        list=db.table(table)
        return list.all()
    
