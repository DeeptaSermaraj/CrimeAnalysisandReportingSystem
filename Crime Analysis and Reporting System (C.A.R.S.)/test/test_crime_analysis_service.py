import unittest
from entity.incident import Incident
from entity.status import Status
from dao.crime_analysis_service_impl import CrimeAnalysisServiceImpl
from c.myexceptions.incident_number_not_found_exception import IncidentNumberNotFoundException

class TestCrimeAnalysisService(unittest.TestCase):
    def setUp(self):
        self.service = CrimeAnalysisServiceImpl()
        self.test_incident = Incident(incident_id=1, description="Test", date="2025-04-01", status="Open")
        self.service.createIncident(self.test_incident)

    def test_create_incident(self):
        new_incident = Incident(incident_id=2, description="Another", date="2025-04-02", status="Open")
        result = self.service.createIncident(new_incident)
        self.assertTrue(result)

    def test_update_incident_status_valid(self):
        status = Status("Closed")
        result = self.service.updateIncidentStatus(status, 1)
        self.assertTrue(result)
        self.assertEqual(self.service.incidents[1].status, "Closed")

    def test_update_incident_status_invalid_id(self):
        with self.assertRaises(IncidentNumberNotFoundException):
            self.service.updateIncidentStatus(Status("Closed"), 999)

if __name__ == '__main__':
    unittest.main()
