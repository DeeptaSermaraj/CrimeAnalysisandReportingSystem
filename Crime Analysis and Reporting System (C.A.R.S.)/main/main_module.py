from dao.crime_analysis_service_impl import CrimeAnalysisServiceImpl
from entity.incident import Incident
from datetime import datetime
from myexceptions.incident_number_not_found_exception import IncidentNumberNotFoundException


def main():
    service = CrimeAnalysisServiceImpl()

    try:
        print("\n Creating a sample incident...")
        incident = Incident(
            incident_id=1,
            incident_type="Robbery",
            description="Robbery at SBI bank in Delhi",
            date=datetime.strptime("2024-02-15", "%Y-%m-%d"),
            status="Open"
        )

        created = service.create_incident(incident)
        print("Incident created!" if created else "Failed to create incident.")

        print("\n Fetching all cases...")
        cases = service.get_all_cases()

        if cases:
            for case in cases:
                print(f" Case ID: {case.case_id}, Description: {case.case_description}")
        else:
            print("No cases found.")

    except IncidentNumberNotFoundException as e:
        print(f"Error: {e}")

    except Exception as e:
        print("An unexpected error occurred:", e)


if __name__ == "__main__":
    main()
