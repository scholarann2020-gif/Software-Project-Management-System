from app.Database.connection import DatabaseConnection


class ProjectService:

    @staticmethod
    def create_project(name, description, status, user_id):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (name, description, status, created_by) VALUES (%s,%s,%s,%s)",
            (name, description, status, user_id)
        )
        conn.commit()

    @staticmethod
    def get_projects():
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects")
        return cursor.fetchall()

    @staticmethod
    def update_project(project_id, status):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE projects SET status=%s WHERE id=%s",
            (status, project_id)
        )
        conn.commit()

    @staticmethod
    def delete_project(project_id):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id=%s", (project_id,))
        conn.commit()
