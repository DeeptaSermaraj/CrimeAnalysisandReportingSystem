import random
import mysql.connector
import hashlib

logged_in_user = None

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="CrimeAnalysis"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    print("\n--- Officer Sign-Up ---\n")
    officer_name = input("Enter your Officer Name: ")
    agency_name = input("Enter your Agency Name: ")
    batch_number = input("Enter your Batch Number: ")
    password = input("Set your password: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE OfficerName = %s", (officer_name,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("\nOfficer already exists! Please log in.\n")
        conn.close()
        return login()

    hashed_password = hash_password(password)

    cursor.execute(""" 
        INSERT INTO Users (OfficerName, AgencyName, BatchNumber, Password)
        VALUES (%s, %s, %s, %s)
    """, (officer_name, agency_name, batch_number, hashed_password))
    conn.commit()
    conn.close()

    print("\nSign-up successful! You can now log in.\n")
    login()

def login():
    global logged_in_user
    print("\n--- Officer Login ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your password: ")

    allowed_officers = [
        ('Sheriff', 'TX1001', 'woody@lapd.com'),
        ('Buzz', 'TX1002', 'buzz@nycpd.com'),
        ('Donald', 'TX1003', 'donald@scotlandyard.com'),
        ('Mickey', 'TX1004', 'mickey@mumbaipolice.com'),
        ('Tom', 'TX1005', 'tom@sydpolice.com'),
        ('Jerry', 'TX1006', 'jerry@delhipolice.com'),
        ('SpongeBob', 'TX1007', 'spongebob@torontopolice.com'),
        ('Patrick', 'TX1008', 'patrick@dubaipolice.com'),
        ('Bugs', 'TX1009', 'bugs@tokyopolice.com'),
        ('Daffy', 'TX1010', 'daffy@interpol.com')
    ]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if user:
        officer_name, agency_name, _ = user[1], user[2], user[4]
        logged_in_user = user
        print(f"\nWelcome back, Officer {officer_name} from {agency_name}!\n")
        conn.close()
        main_menu()
    else:
        print("\nInvalid Batch Number or password. Please try again.\n")
        conn.close()
        start()


def create_incident():
    global logged_in_user
    print("\n--- Login needed ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your Password: ")

    allowed_batch_numbers = ['TX1002', 'TX1004', 'TX1008', 'TX1010']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if user:
        if batch_number in allowed_batch_numbers:
            logged_in_user = user
            print(f"\nWelcome Officer {user[1]}! Access granted to create incident.\n")

            print("\n--- Create New Incident ---\n")
            incident_type = input("Incident Type                 : ")
            incident_date = input("Incident Date (YYYY-MM-DD)    : ")
            location = input("Location                      : ")
            description = input("Description                   : ")
            status = input("Status                        : ")
            victim_id = input("Victim ID                     : ")
            suspect_id = input("Suspect ID                    : ")

            query = """
            INSERT INTO Incidents (IncidentType, IncidentDate, Location, Description, Status, VictimID, SuspectID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (incident_type, incident_date, location, description, status, victim_id, suspect_id))
            conn.commit()
            print("\n Incident created successfully!\n")
        else:
            print("\n Access denied! You are not authorized to create incidents.\n")
    else:
        print("\n Invalid Batch Number or Password.\n")

    conn.close()
    main_menu()


def update_incident_status():
    print("\n--- Login needed ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your Password: ")

    allowed_batch_numbers = ['TX1002', 'TX1004', 'TX1008', 'TX1010']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if user:
        if batch_number in allowed_batch_numbers:
            print(f"\nWelcome Officer {user[1]}! Access granted to update incident status.\n")

            print("\n--- Update Incident Status ---\n")
            incident_id = input("Incident ID to Update     : ")
            new_status = input("New Status                : ")

            query = """
            UPDATE Incidents
            SET Status = %s
            WHERE IncidentID = %s
            """
            cursor.execute(query, (new_status, incident_id))
            conn.commit()
            print("\n Incident status updated successfully!\n")
        else:
            print("\n Access denied! You are not authorized to update incident status.\n")
    else:
        print("\n Invalid Batch Number or Password.\n")

    conn.close()
    main_menu()


def list_incidents_by_date_range():
    print("\n--- List Incidents by Date Range ---\n")

    start_date = input("Start Date (YYYY-MM-DD)   : ")
    end_date   = input("End Date (YYYY-MM-DD)     : ")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT IncidentID, IncidentType, IncidentDate, Location, Status
    FROM Incidents
    WHERE IncidentDate BETWEEN %s AND %s
    """
    cursor.execute(query, (start_date, end_date))
    incidents = cursor.fetchall()

    if incidents:
        print("\n--- Incidents Between Date Range ---\n")
        for incident in incidents:
            print(f"ID: {incident[0]} | Type: {incident[1]} | Date: {incident[2]} | Location: {incident[3]} | Status: {incident[4]}")
    else:
        print("\nNo incidents found within that date range.\n")

    conn.close()
    main_menu()


def search_incidents():
    print("\n--- Search Incidents ---\n")

    search_criteria = input("Search by (Type / Location / Status) : ")

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT IncidentID, IncidentType, IncidentDate, Location, Status
    FROM Incidents
    WHERE IncidentType LIKE %s OR Location LIKE %s OR Status LIKE %s
    """
    cursor.execute(query, (
        f"%{search_criteria}%",
        f"%{search_criteria}%",
        f"%{search_criteria}%"
    ))
    incidents = cursor.fetchall()

    if incidents:
        print("\n--- Search Results ---\n")
        for incident in incidents:
            print(f"ID: {incident[0]} | Type: {incident[1]} | Date: {incident[2]} | Location: {incident[3]} | Status: {incident[4]}")
    else:
        print("\nNo incidents found matching your criteria.\n")

    conn.close()
    main_menu()


def generate_incident_report():
    print("\n--- Login needed ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your Password: ")

    allowed_batch_numbers = ['TX1002', 'TX1004', 'TX1008', 'TX1010']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if user and batch_number in allowed_batch_numbers:
        print(f"\nWelcome Officer {user[1]}! Access granted to generate incident reports.\n")

        print("\n--- Generate Incident Report ---\n")
        incident_id = input("Enter the Incident ID for the report: ")

        incident_query = """
            SELECT IncidentType, IncidentDate, Location, Description, Status, VictimID, SuspectID
            FROM Incidents
            WHERE IncidentID = %s
        """
        cursor.execute(incident_query, (incident_id,))
        incident = cursor.fetchone()

        if not incident:
            print("\nNo incident found with that ID.\n")
            conn.close()
            main_menu()
            return

        incident_type, date, location, description, status, victim_id, suspect_id = incident

        victim = None
        if victim_id:
            cursor.execute("""
                SELECT FirstName, LastName, DateOfBirth, Gender, ContactInformation
                FROM Victims
                WHERE VictimID = %s
            """, (victim_id,))
            victim = cursor.fetchone()

        suspect = None
        if suspect_id:
            cursor.execute("""
                SELECT FirstName, LastName, DateOfBirth, Gender, ContactInformation
                FROM Suspects
                WHERE SuspectID = %s
            """, (suspect_id,))
            suspect = cursor.fetchone()

        cursor.execute("""
            SELECT EvidenceID, Description, LocationFound
            FROM Evidence
            WHERE IncidentID = %s
        """, (incident_id,))
        evidences = cursor.fetchall()

        print("\n========== INCIDENT REPORT ==========\n")
        print(f"Incident ID        : {incident_id}")
        print(f"Type               : {incident_type}")
        print(f"Date               : {date}")
        print(f"Location           : {location}")
        print(f"Status             : {status}")
        print("\n--- Incident Summary ---")
        print(f"{description}")

        if victim:
            print("\n--- Victim Information ---")
            print(f"Name           : {victim[0]} {victim[1]}")
            print(f"Date of Birth  : {victim[2]}")
            print(f"Gender         : {victim[3]}")
            print(f"Contact        : {victim[4]}")
        else:
            print("\nNo victim details available.")

        if suspect:
            print("\n--- Suspect Information ---")
            print(f"Name           : {suspect[0]} {suspect[1]}")
            print(f"Date of Birth  : {suspect[2]}")
            print(f"Gender         : {suspect[3]}")
            print(f"Contact        : {suspect[4]}")
        else:
            print("\nNo suspect details available.")

        if evidences:
            print("\n--- Evidence Collected ---")
            for evidence in evidences:
                print(f"\nEvidence ID  : {evidence[0]}")
                print(f"Description    : {evidence[1]}")
                print(f"Location Found : {evidence[2]}")
        else:
            print("\nNo evidence found for this incident.")

        print("\n\n========== INCIDENT REPORT SUMMARY ==========\n")
        print(f"On {date}, a {incident_type.lower()} occurred at {location}.")
        if victim:
            print(f"The victim involved was {victim[0]} {victim[1]}, a {victim[3].lower()} born on {victim[2]}.")
        if suspect:
            print(f"The suspect identified was {suspect[0]} {suspect[1]}, a {suspect[3].lower()} born on {suspect[2]}.")
        print(f"Status of the case: {status}.")
        if evidences:
            print(f"A total of {len(evidences)} piece(s) of evidence were collected from the scene.")
        else:
            print("No evidence was collected for this incident.")
        print(f"Incident Description: {description}")
        print("\n==============================================\n")

    else:
        print("\n Access denied! You are not authorized to generate incident report.\n")

    conn.close()
    main_menu()


def create_case():
    print("\n--- Login needed ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your Password: ")

    allowed_batch_numbers = ['TX1002', 'TX1004', 'TX1008', 'TX1010']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if user and batch_number in allowed_batch_numbers:
        print(f"\nWelcome Officer {user[1]}! Access granted to create a case.\n")

        print("\n--- Create New Case ---\n")
        case_title = input("Enter the case title              : ")
        case_status = input("Enter the case status            : ")
        open_date = input("Enter the open date (YYYY-MM-DD)   : ")
        close_date = input("Enter the close date (YYYY-MM-DD) : ")
        assigned_officer = input("Enter the assigned officer        : ")
        incident_id = input("Enter the incident ID             : ")

        query = """
        INSERT INTO Cases (CaseTitle, CaseStatus, OpenDate, CloseDate, AssignedOfficer, IncidentID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (case_title, case_status, open_date, close_date, assigned_officer, incident_id))
        conn.commit()
        conn.close()

        print("\n Case created successfully!\n")

    else:
        print("\n Access denied! You are not authorized to create case.\n")
        conn.close()

    main_menu()


def get_case_details():
    print("\n--- Login needed ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your Password: ")

    allowed_batch_numbers = ['TX1002', 'TX1004', 'TX1008', 'TX1010']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if not (user and batch_number in allowed_batch_numbers):
        print("\n Access denied! You are not authorized to get case details.\n")
        conn.close()
        main_menu()
        return

    print(f"\nWelcome Officer {user[1]}! Access granted to case details.\n")

    print("\n--- Case Details ---\n")
    case_id = input("Enter the Case ID to get details: ")

    cursor.execute("""
        SELECT CaseTitle, CaseStatus, OpenDate, CloseDate, AssignedOfficer, IncidentID
        FROM Cases
        WHERE CaseID = %s
    """, (case_id,))
    case = cursor.fetchone()

    if not case:
        print("\nNo case found with that ID.\n")
        conn.close()
        main_menu()
        return

    title, status, open_date, close_date, officer_id, incident_id = case

    cursor.execute("""
        SELECT IncidentType, IncidentDate, Location, Description, Status, VictimID, SuspectID
        FROM Incidents
        WHERE IncidentID = %s
    """, (incident_id,))
    incident = cursor.fetchone()

    if not incident:
        print("\nIncident linked to this case was not found.\n")
        conn.close()
        main_menu()
        return

    incident_type, incident_date, location, incident_desc, incident_status, victim_id, suspect_id = incident

    victim = None
    if victim_id:
        cursor.execute("""
            SELECT FirstName, LastName, DateOfBirth, Gender, ContactInformation
            FROM Victims
            WHERE VictimID = %s
        """, (victim_id,))
        victim = cursor.fetchone()

    suspect = None
    if suspect_id:
        cursor.execute("""
            SELECT FirstName, LastName, DateOfBirth, Gender, ContactInformation
            FROM Suspects
            WHERE SuspectID = %s
        """, (suspect_id,))
        suspect = cursor.fetchone()

    cursor.execute("""
        SELECT EvidenceID, Description, LocationFound
        FROM Evidence
        WHERE IncidentID = %s
    """, (incident_id,))
    evidences = cursor.fetchall()

    officer = None
    agency = None
    if officer_id:
        cursor.execute("""
            SELECT FirstName, LastName, `Rank`, BadgeNumber, ContactInformation, AgencyID
            FROM Officers
            WHERE OfficerID = %s
        """, (officer_id,))
        officer = cursor.fetchone()

        if officer and officer[5]:
            cursor.execute("""
                SELECT AgencyName, Jurisdiction, ContactInformation
                FROM LawEnforcementAgencies
                WHERE AgencyID = %s
            """, (officer[5],))
            agency = cursor.fetchone()

    print("\n========== CASE REPORT ==========\n")
    print(f"Case ID          : {case_id}")
    print(f"Title            : {title}")
    print(f"Status           : {status}")
    print(f"Open Date        : {open_date}")
    print(f"Close Date       : {close_date if close_date else 'Still Open'}")

    if officer:
        print(f"Assigned Officer : {officer[0]} {officer[1]}")
        print(f"Rank             : {officer[2]}")
        print(f"Badge Number     : {officer[3]}")
        print(f"Contact          : {officer[4]}")
        if agency:
            print(f"Agency           : {agency[0]}")
            print(f"Jurisdiction     : {agency[1]}")
            print(f"Agency Contact   : {agency[2]}")
    else:
        print("\nNo officer assigned to this case.")

    print(f"\n--- Linked Incident Details ---")
    print(f"Incident ID     : {incident_id}")
    print(f"Type            : {incident_type}")
    print(f"Date            : {incident_date}")
    print(f"Location        : {location}")
    print(f"Status          : {incident_status}")
    print(f"Description     : {incident_desc}")

    if victim:
        print("\n--- Victim Information ---")
        print(f"Name            : {victim[0]} {victim[1]}")
        print(f"Date of Birth   : {victim[2]}")
        print(f"Gender          : {victim[3]}")
        print(f"Contact         : {victim[4]}")
    else:
        print("\nNo victim details available.")

    if suspect:
        print("\n--- Suspect Information ---")
        print(f"Name            : {suspect[0]} {suspect[1]}")
        print(f"Date of Birth   : {suspect[2]}")
        print(f"Gender          : {suspect[3]}")
        print(f"Contact         : {suspect[4]}")
    else:
        print("\nNo suspect details available.")

    if evidences:
        print("\n--- Evidence Collected ---")
        for evidence in evidences:
            print(f"\nEvidence ID     : {evidence[0]}")
            print(f"Description     : {evidence[1]}")
            print(f"Location Found  : {evidence[2]}")
    else:
        print("\nNo evidence found for this incident.")

    print("\n\n========== CASE SUMMARY ==========\n")
    print(f"The case titled '{title}' was opened on {open_date} and is currently marked as '{status}'.")
    if close_date:
        print(f"It was officially closed on {close_date}.")
    if officer:
        print(
            f"The case is being handled by Officer {officer[0]} {officer[1]}, ranked '{officer[2]}', with badge number '{officer[3]}'.")
    if agency:
        print(f"The assigned officer is from {agency[0]}, which has jurisdiction over {agency[1]}.")
    print(f"The case is associated with an incident that occurred on {incident_date} at {location}.")
    print(f"The incident is classified as '{incident_type}' and is currently '{incident_status}'.")
    if victim:
        print(f"The victim in the case is {victim[0]} {victim[1]}, a {victim[3].lower()} born on {victim[2]}.")
    if suspect:
        print(f"The suspect is {suspect[0]} {suspect[1]}, a {suspect[3].lower()} born on {suspect[2]}.")
    if evidences:
        print(f"A total of {len(evidences)} piece(s) of evidence have been collected and documented.")
    else:
        print("There is no evidence recorded for this case.")
    print(f"Incident Description: {incident_desc}")

    print("\n==================================\n")

    conn.close()
    main_menu()

def update_case():
    print("\n--- Login needed ---\n")
    batch_number = input("Enter your Batch Number: ")
    password = input("Enter your Password: ")

    allowed_batch_numbers = ['TX1002', 'TX1004', 'TX1008', 'TX1010']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE BatchNumber = %s AND Password = %s",
                   (batch_number, hash_password(password)))
    user = cursor.fetchone()

    if user:
        if batch_number in allowed_batch_numbers:
            print(f"\nWelcome Officer {user[1]}! Access granted to update case.\n")

            print("\n--- Update Case ---\n")
            case_id = input("Enter the Case ID to update          : ")
            case_title = input("Enter new case title              : ")
            case_status = input("Enter new case status            : ")
            open_date = input("Enter new open date (YYYY-MM-DD)   : ")
            close_date = input("Enter new close date (YYYY-MM-DD) : ")
            assigned_officer = input("Enter new assigned officer  : ")
            incident_id = input("Enter new incident ID            : ")

            query = """
            UPDATE Cases
            SET CaseTitle = %s, CaseStatus = %s, OpenDate = %s, CloseDate = %s, AssignedOfficer = %s, IncidentID = %s
            WHERE CaseID = %s
            """
            cursor.execute(query, (case_title, case_status, open_date, close_date, assigned_officer, incident_id, case_id))
            conn.commit()

            print("\nCase updated successfully!\n")
        else:
            print("\nAccess denied! You are not authorized to update case.\n")
    else:
        print("\nInvalid Batch Number or Password.\n")

    conn.close()
    main_menu()


def list_all_cases():
    print("\n--- All Registered Cases ---\n")
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT CaseID, CaseTitle, CaseStatus, OpenDate, CloseDate, AssignedOfficer, IncidentID
    FROM Cases
    """
    cursor.execute(query)
    cases = cursor.fetchall()

    if cases:
        for case in cases:
            print(f"""
Case ID          : {case[0]}
Title            : {case[1]}
Status           : {case[2]}
Open Date        : {case[3]}
Close Date       : {case[4]}
Assigned Officer : {case[5]}
Incident ID      : {case[6]}
-----------------------------""")
    else:
        print("No cases found.")

    conn.close()
    main_menu()


def view_details():
    print("\n--- View Details ---")
    print("1. List All Victims")
    print("2. List All Suspects")
    print("3. List All Law Enforcement Agencies")
    print("4. List All Officers")
    print("5. List All Evidence")
    print("6. List All Incidents")
    print("7. View Victim Details")
    print("8. View Suspect Details")
    print("9. View Officer Details")
    print("10. Back to Main Menu")

    choice = input("Enter your choice: ")

    if choice == "1":
        list_all_victims()
    elif choice == "2":
        list_all_suspects()
    elif choice == "3":
        list_all_agencies()
    elif choice == "4":
        list_all_officers()
    elif choice == "5":
        list_all_evidence()
    elif choice == "6":
        list_all_incidents()
    elif choice == "7":
        view_victim_details()
    elif choice == "8":
        view_suspect_details()
    elif choice == "9":
        view_officer_details()
    elif choice == "10":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        view_details()


def list_all_incidents():
    print("\n--- List of All Incidents ---")
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT * FROM Incidents"
    cursor.execute(query)
    incidents = cursor.fetchall()

    if incidents:
        for incident in incidents:
            print(f"""
Incident ID   : {incident[0]}
Type          : {incident[1]}
Date          : {incident[2]}
Location      : {incident[3]}
Description   : {incident[4]}
Status        : {incident[5]}
Victim ID     : {incident[6]}
Suspect ID    : {incident[7]}
-----------------------------""")
    else:
        print("No incidents found.")

    conn.close()
    view_details()


def list_all_victims():
    print("\n--- List of All Victims ---")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Victims")
    victims = cursor.fetchall()

    for victim in victims:
        print(f"""
Victim ID          : {victim[0]}
First Name         : {victim[1]}
Last Name          : {victim[2]}
Date of Birth      : {victim[3]}
Gender             : {victim[4]}
Contact Information: {victim[5]}
-----------------------------""")

    conn.close()
    view_details()

def list_all_suspects():
    print("\n--- List of All Suspects ---")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Suspects")
    suspects = cursor.fetchall()

    for suspect in suspects:
        print(f"""
Suspect ID         : {suspect[0]}
First Name         : {suspect[1]}
Last Name          : {suspect[2]}
Date of Birth      : {suspect[3]}
Gender             : {suspect[4]}
Contact Information: {suspect[5]}
-----------------------------""")

    conn.close()
    view_details()

def list_all_agencies():
    print("\n--- List of All Law Enforcement Agencies ---")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM LawEnforcementAgencies")
    agencies = cursor.fetchall()

    for agency in agencies:
        print(f"""
Agency ID          : {agency[0]}
Agency Name        : {agency[1]}
Jurisdiction       : {agency[2]}
Contact Information: {agency[3]}
-----------------------------""")

    conn.close()
    view_details()

def list_all_officers():
    print("\n--- List of All Officers ---")
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT Officers.OfficerID, Officers.FirstName, Officers.LastName, Officers.Rank, 
           LawEnforcementAgencies.AgencyName
    FROM Officers
    JOIN LawEnforcementAgencies ON Officers.AgencyID = LawEnforcementAgencies.AgencyID
    """

    cursor.execute(query)
    officers = cursor.fetchall()

    for officer in officers:
        print(f"""
Officer ID : {officer[0]}
Name       : {officer[1]} {officer[2]}
Rank       : {officer[3]}
Agency     : {officer[4]}
-----------------------------""")

    conn.close()
    view_details()

def list_all_evidence():
    print("\n--- List of All Evidence ---")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Evidence")
    evidence = cursor.fetchall()

    for item in evidence:
        print(f"""
Evidence ID     : {item[0]}
Description     : {item[1]}
Location Found  : {item[2]}
Incident ID     : {item[3]}
-----------------------------""")

    conn.close()
    view_details()


def view_victim_details():
    victim_id = input("Enter Victim ID or Victim Name (First or Last): ")
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT VictimID, FirstName, LastName, DateOfBirth, Gender, ContactInformation
    FROM Victims
    WHERE VictimID = %s OR FirstName LIKE %s OR LastName LIKE %s
    """
    cursor.execute(query, (victim_id, f"%{victim_id}%", f"%{victim_id}%"))
    victim = cursor.fetchone()

    if victim:
        print("\n--- Victim Details ---")
        print(f"Victim ID: {victim[0]}")
        print(f"Name: {victim[1]} {victim[2]}")
        print(f"Date of Birth: {victim[3]}")
        print(f"Gender: {victim[4]}")
        print(f"Contact Information: {victim[5]}")
    else:
        print("\nNo victim found with that ID or name.")
    conn.close()
    view_details()

def view_suspect_details():
    suspect_id = input("Enter Suspect ID or Suspect Name (First or Last): ")
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT SuspectID, FirstName, LastName, DateOfBirth, Gender, ContactInformation
    FROM Suspects
    WHERE SuspectID = %s OR FirstName LIKE %s OR LastName LIKE %s
    """
    cursor.execute(query, (suspect_id, f"%{suspect_id}%", f"%{suspect_id}%"))
    suspect = cursor.fetchone()

    if suspect:
        print("\n--- Suspect Details ---")
        print(f"Suspect ID: {suspect[0]}")
        print(f"Name: {suspect[1]} {suspect[2]}")
        print(f"Date of Birth: {suspect[3]}")
        print(f"Gender: {suspect[4]}")
        print(f"Contact Information: {suspect[5]}")
    else:
        print("\nNo suspect found with that ID or name.")
    conn.close()
    view_details()

def view_officer_details():
    officer_id = input("Enter Officer ID or Officer Name (First or Last): ")
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT Officers.OfficerID, Officers.FirstName, Officers.LastName, Officers.Rank, LawEnforcementAgencies.AgencyName
    FROM Officers
    LEFT JOIN LawEnforcementAgencies ON Officers.AgencyID = LawEnforcementAgencies.AgencyID
    WHERE Officers.OfficerID = %s OR Officers.FirstName LIKE %s OR Officers.LastName LIKE %s
    """
    cursor.execute(query, (officer_id, f"%{officer_id}%", f"%{officer_id}%"))
    officer = cursor.fetchone()

    if officer:
        print("\n--- Officer Details ---")
        print(f"Officer ID: {officer[0]}")
        print(f"Name: {officer[1]} {officer[2]}")
        print(f"Rank: {officer[3]}")
        print(f"Agency: {officer[4]}")
    else:
        print("\nNo officer found with that ID or name.")
    conn.close()
    view_details()
    main_menu()


def main_menu():
    global logged_in_user

    if logged_in_user is None:
        print("You need to log in first.")
        start()
        return

    print("\n--- Crime Reporting System Officers Control Panel ---")
    print("1. Create a New Incident")
    print("2. Update Incident Status")
    print("3. List Incidents by Date Range")
    print("4. Search Incidents")
    print("5. Generate Incident Report")
    print("6. Create a New Case")
    print("7. Get Case Details")
    print("8. Update Case")
    print("9. List All Cases")
    print("10. View Details")
    print("11. Log Out")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_incident()
    elif choice == "2":
        update_incident_status()
    elif choice == "3":
        list_incidents_by_date_range()
    elif choice == "4":
        search_incidents()
    elif choice == "5":
        generate_incident_report()
    elif choice == "6":
        create_case()
    elif choice == "7":
        get_case_details()
    elif choice == "8":
        update_case()
    elif choice == "9":
        list_all_cases()
    elif choice == "10":
        view_details()
    elif choice == "11":
        print("Logging out...")
        logged_in_user = None
        start()
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def start():
    print("\n--- Welcome to the Crime Reporting System ---")

    print("1. Log In")
    print("2. Sign Up")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        login()
    elif choice == "2":
        sign_up()
    elif choice == "3":
        print("Thank you for using the system. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")
        start()


if __name__ == "__main__":
    start()
