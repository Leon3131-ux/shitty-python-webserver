from pyodbc import Cursor


class DepartmentService:
    def __init__(self, cursor: Cursor):
        self.cursor = cursor

    def save_department(self, name, company_id, company_name):
        self.cursor.execute("{CALL sp_saveDepartment(?, ?)}", name, company_id)
        self.cursor.commit()
        return self.get_department_by_name(name, company_name)

    def get_department_by_name(self, name, company_name):
        self.cursor.execute("SELECT department.ID, department.NAME, department.COMPANY_ID FROM DEPARTMENT "
                            "INNER JOIN company ON company.ID = department.COMPANY_ID "
                            "WHERE department.NAME = ? AND company.NAME = ?", name, company_name)

        row = self.cursor.fetchone()
        if row:
            department = {
                "id": row.ID,
                "name": row.NAME,
                "companyId": row.COMPANY_ID
            }
        else:
            department = {}
        return department

