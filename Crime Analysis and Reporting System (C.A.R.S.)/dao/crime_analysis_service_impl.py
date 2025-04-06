from dao.icrime_analysis_service import ICrimeAnalysisService
from util.db_connection import DBConnection

class CrimeAnalysisServiceImpl(ICrimeAnalysisService):
    def __init__(self):
        self.connection = DBConnection.get_connection()

    def create_incident(self, incident):

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Incident (incident_id, incident_type, description, date, location, status) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (incident.incident_id, incident.incident_type, incident.description, incident.date, incident.location, incident.status)
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating incident: {e}")
            return False

    def update_incident_status(self, status, incident_id):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Incident SET status = %s WHERE incident_id = %s"
            cursor.execute(query, (status, incident_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating incident status: {e}")
            return False

    def get_incidents_in_date_range(self, start_date, end_date):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Incident WHERE date BETWEEN %s AND %s"
            cursor.execute(query, (start_date, end_date))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching incidents in date range: {e}")
            return []

    def search_incidents(self, incident_type):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Incident WHERE incident_type = %s"
            cursor.execute(query, (incident_type,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error searching incidents: {e}")
            return []

    def generate_incident_report(self, incident):

        return {
            "incident_id": incident.incident_id,
            "summary": f"Report for incident {incident.incident_id} - {incident.description}"
        }

    def create_case(self, case_description, incidents):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO Cases (description) VALUES (%s)"
            cursor.execute(query, (case_description,))
            case_id = cursor.lastrowid

            for incident in incidents:
                link_query = "INSERT INTO Case_Incident (case_id, incident_id) VALUES (%s, %s)"
                cursor.execute(link_query, (case_id, incident.incident_id))

            self.connection.commit()
            return {"case_id": case_id, "description": case_description}
        except Exception as e:
            print(f"Error creating case: {e}")
            return None

    def get_case_details(self, case_id):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Cases WHERE case_id = %s"
            cursor.execute(query, (case_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching case details: {e}")
            return None

    def update_case_details(self, case_obj):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Cases SET description = %s WHERE case_id = %s"
            cursor.execute(query, (case_obj.description, case_obj.case_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating case: {e}")
            return False

    def get_all_cases(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM Cases"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all cases: {e}")
            return []
