from pyodbc import Cursor

class JobService:

    cursor: Cursor = None

    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def get_job(self, id):
        self.cursor.execute("SELECT ID, NAME FROM JOB WHERE ID = ?", id)
        row = self.cursor.fetchone()
        job = {
            "id": row.ID,
            "name": row.NAME
        }
        return job