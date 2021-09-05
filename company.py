from pyodbc import Cursor


class CompanyService:

    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def get_company_by_name(self, name):
        self.cursor.execute("SELECT ID, NAME FROM COMPANY WHERE NAME = ?", name)
        row = self.cursor.fetchone()
        if row:
            company = {
                "id": row.ID,
                "name": row.NAME
            }
        else:
            company = {}
        return company

    def save_company(self, name):
        self.cursor.execute("{CALL sp_saveCompany(?)}", name)
        self.cursor.commit()
        return self.get_company_by_name(name)