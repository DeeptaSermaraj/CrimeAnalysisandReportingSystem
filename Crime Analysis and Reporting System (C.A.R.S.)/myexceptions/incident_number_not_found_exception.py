class IncidentNumberNotFoundException(Exception):
    def __init__(self, incident_id):
        super().__init__(f"Incident with ID {incident_id} not found in the database.")
