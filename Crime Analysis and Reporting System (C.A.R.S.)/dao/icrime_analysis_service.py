from abc import ABC, abstractmethod
from entity.incident import Incident
from entity.status import Status
from entity.case import Case

class ICrimeAnalysisService(ABC):

    @abstractmethod
    def create_incident(self, incident: Incident) -> bool:
        """Create a new incident"""
        pass

    @abstractmethod
    def update_incident_status(self, status: Status, incident_id: int) -> bool:
        """Update the status of an incident"""
        pass

    @abstractmethod
    def get_incidents_in_date_range(self, start_date: str, end_date: str):
        """Get a list of incidents within a date range"""
        pass

    @abstractmethod
    def search_incidents(self, incident_type: str):
        """Search for incidents based on various criteria"""
        pass

    @abstractmethod
    def generate_incident_report(self, incident: Incident):
        """Generate an incident report"""
        pass

    @abstractmethod
    def create_case(self, case_description: str, incidents: list):
        """Create a new case and associate it with incidents"""
        pass

    @abstractmethod
    def get_case_details(self, case_id: int) -> Case:
        """Get details of a specific case"""
        pass

    @abstractmethod
    def update_case_details(self, case: Case) -> bool:
        """Update case details"""
        pass

    @abstractmethod
    def get_all_cases(self):
        """Get a list of all cases"""
        pass
