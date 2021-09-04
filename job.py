from pyodbc import Cursor


class JobService:
    cursor: Cursor = None

    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def get_job(self, id):
        self.cursor.execute("SELECT ID, NAME FROM JOB WHERE ID = ?", id)
        row = self.cursor.fetchone()
        if row:
            job = {
                "id": row.ID,
                "name": row.NAME
            }
        else:
            job = {}
        return job

    def get_job_by_name(self, name):
        self.cursor.execute("SELECT ID, NAME FROM JOB WHERE NAME = ?", name)
        row = self.cursor.fetchone()
        if row:
            job = {
                "id": row.ID,
                "name": row.NAME
            }
        else:
            job = {}
        return job

    def save_job(self, name):
        self.cursor.execute("{CALL sp_saveJob(?)}", name)
        self.cursor.commit()
        return self.get_job_by_name(name)
