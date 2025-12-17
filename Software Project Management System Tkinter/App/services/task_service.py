from app.database.connection import DatabaseConnection


class TaskService:

    @staticmethod
    def create_task(title, status, project_id, assigned_to):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, status, project_id, assigned_to) VALUES (%s,%s,%s,%s)",
            (title, status, project_id, assigned_to)
        )
        conn.commit()

    @staticmethod
    def get_tasks(project_id):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks WHERE project_id=%s", (project_id,))
        return cursor.fetchall()

    @staticmethod
    def update_task(task_id, status):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status=%s WHERE id=%s",
            (status, task_id)
        )
        conn.commit()

    @staticmethod
    def delete_task(task_id):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
