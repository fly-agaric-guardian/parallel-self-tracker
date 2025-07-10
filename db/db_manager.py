import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('db/data_system.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                my_paragon TEXT NOT NULL,
                opp_paragon TEXT NOT NULL,
                turn_order TEXT NOT NULL,
                result TEXT NOT NULL,
                my_mmr INT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_all_records(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM records ORDER BY id")
        records = cursor.fetchall()
        
        return records

    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        return records
    
    def insert_record(self, record):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO records (my_paragon, opp_paragon, turn_order, result, my_mmr, date) VALUES (?, ?, ?, ?, ?, ?)", record)
        self.conn.commit()
    
    def update_record(self, record, id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE records SET my_paragon=?, opp_paragon=?, turn_order=?, result=?, my_mmr=?, date=? WHERE id=?", record + (id,))
        self.conn.commit()
    
    def delete_record(self, ids):
        cursor = self.conn.cursor()
        for id in ids:
            cursor.execute("DELETE FROM records WHERE id=?", (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()