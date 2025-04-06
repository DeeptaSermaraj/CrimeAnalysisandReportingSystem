CREATE DATABASE CrimeAnalysis;
USE CrimeAnalysis;

CREATE TABLE Victims (
    VictimID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    ContactInformation VARCHAR(255)
);

CREATE TABLE Suspects (
    SuspectID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    ContactInformation VARCHAR(255)
);

CREATE TABLE LawEnforcementAgencies (
    AgencyID INT PRIMARY KEY AUTO_INCREMENT,
    AgencyName VARCHAR(100),
    Jurisdiction VARCHAR(100),
    ContactInformation VARCHAR(255)
);

CREATE TABLE Officers (
    OfficerID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    BadgeNumber VARCHAR(100) UNIQUE,
    `Rank` VARCHAR(50),  -- Used backticks to avoid keyword conflict
    ContactInformation VARCHAR(255),
    AgencyID INT,
    FOREIGN KEY (AgencyID) REFERENCES LawEnforcementAgencies(AgencyID)
);

CREATE TABLE Incidents (
    IncidentID INT PRIMARY KEY AUTO_INCREMENT,
    IncidentType VARCHAR(100),
    IncidentDate DATE,
    Location VARCHAR(255),
    Description TEXT,
    Status VARCHAR(50),
    VictimID INT,
    SuspectID INT,
    FOREIGN KEY (VictimID) REFERENCES Victims(VictimID),
    FOREIGN KEY (SuspectID) REFERENCES Suspects(SuspectID)
);

CREATE TABLE Evidence (
    EvidenceID INT PRIMARY KEY AUTO_INCREMENT,
    Description TEXT,
    LocationFound VARCHAR(255),
    IncidentID INT,
    FOREIGN KEY (IncidentID) REFERENCES Incidents(IncidentID)
);

CREATE TABLE Reports (
    ReportID INT PRIMARY KEY AUTO_INCREMENT,
    IncidentID INT,
    ReportingOfficer INT,
    ReportDate DATE,
    ReportDetails TEXT,
    Status VARCHAR(50),
    FOREIGN KEY (IncidentID) REFERENCES Incidents(IncidentID),
    FOREIGN KEY (ReportingOfficer) REFERENCES Officers(OfficerID)
);

INSERT INTO LawEnforcementAgencies (AgencyName, Jurisdiction, ContactInformation) VALUES
('Mumbai Police', 'Mumbai, India', 'mumbaipolice@gov.in'),
('Los Angeles PD', 'Los Angeles, USA', 'lapd@gov.us'),
('Scotland Yard', 'London, UK', 'scotlandyard@gov.uk'),
('New York PD', 'New York, USA', 'nypd@gov.us'),
('Interpol', 'International', 'interpol@gov.int'),
('Delhi Police', 'Delhi, India', 'delhipolice@gov.in'),
('Sydney Police', 'Sydney, Australia', 'sydpolice@gov.au'),
('Toronto Police', 'Toronto, Canada', 'torontopolice@gov.ca'),
('Dubai Police', 'Dubai, UAE', 'dubaipolice@gov.ae'),
('Tokyo Metropolitan Police', 'Tokyo, Japan', 'tokyopolice@gov.jp');

INSERT INTO Officers (FirstName, LastName, BadgeNumber, `Rank`, ContactInformation, AgencyID) VALUES
('Sheriff', 'Woody', 'TX1001', 'Sergeant', 'woody@lapd.com', 2),
('Buzz', 'Lightyear', 'TX1002', 'Lieutenant', 'buzz@nycpd.com', 4),
('Donald', 'Duck', 'TX1003', 'Detective', 'donald@scotlandyard.com', 3),
('Mickey', 'Mouse', 'TX1004', 'Captain', 'mickey@mumbaipolice.com', 1),
('Tom', 'Cat', 'TX1005', 'Inspector', 'tom@sydpolice.com', 7),
('Jerry', 'Mouse', 'TX1006', 'Constable', 'jerry@delhipolice.com', 6),
('SpongeBob', 'SquarePants', 'TX1007', 'Sergeant', 'spongebob@torontopolice.com', 8),
('Patrick', 'Star', 'TX1008', 'Lieutenant', 'patrick@dubaipolice.com', 9),
('Bugs', 'Bunny', 'TX1009', 'Detective', 'bugs@tokyopolice.com', 10),
('Daffy', 'Duck', 'TX1010', 'Commissioner', 'daffy@interpol.com', 5);

INSERT INTO Victims (FirstName, LastName, DateOfBirth, Gender, ContactInformation) VALUES
('Shah Rukh', 'Khan', '1965-11-02', 'Male', 'srk@bollywood.com'),
('Salman', 'Khan', '1965-12-27', 'Male', 'salmankhan@bollywood.com'),
('Amitabh', 'Bachchan', '1942-10-11', 'Male', 'amitabh@bollywood.com'),
('Aishwarya', 'Rai', '1973-11-01', 'Female', 'aish@bollywood.com'),
('Priyanka', 'Chopra', '1982-07-18', 'Female', 'priyanka@bollywood.com'),
('Deepika', 'Padukone', '1986-01-05', 'Female', 'deepika@bollywood.com'),
('Ranveer', 'Singh', '1985-07-06', 'Male', 'ranveer@bollywood.com'),
('Hrithik', 'Roshan', '1974-01-10', 'Male', 'hrithik@bollywood.com'),
('Alia', 'Bhatt', '1993-03-15', 'Female', 'alia@bollywood.com'),
('Kareena', 'Kapoor', '1980-09-21', 'Female', 'kareena@bollywood.com');

INSERT INTO Suspects (FirstName, LastName, DateOfBirth, Gender, ContactInformation) VALUES
('Johnny', 'Depp', '1963-06-09', 'Male', 'johnny@hollywood.com'),
('Leonardo', 'DiCaprio', '1974-11-11', 'Male', 'leo@hollywood.com'),
('Angelina', 'Jolie', '1975-06-04', 'Female', 'angelina@hollywood.com'),
('Brad', 'Pitt', '1963-12-18', 'Male', 'brad@hollywood.com'),
('Tom', 'Cruise', '1962-07-03', 'Male', 'tom@hollywood.com'),
('Selena', 'Gomez', '1992-07-22', 'Female', 'selena@hollywood.com'),
('Robert', 'Downey Jr.', '1965-04-04', 'Male', 'rdj@hollywood.com'),
('Scarlett', 'Johansson', '1984-11-22', 'Female', 'scarlett@hollywood.com'),
('Chris', 'Evans', '1981-06-13', 'Male', 'chris@hollywood.com'),
('Will', 'Smith', '1968-09-25', 'Male', 'will@hollywood.com');

INSERT INTO Incidents (IncidentType, IncidentDate, Location, Description, Status, VictimID, SuspectID) VALUES
('Robbery', '2024-01-05', 'Mumbai, India', 'Shah Rukh Khan was robbed at a film set.', 'Under Investigation', 1, 1),
('Homicide', '2024-02-10', 'Delhi, India', 'Aamir Khan was found dead in a hotel room.', 'Closed', 2, 2),
('Theft', '2024-03-15', 'Chennai, India', 'Deepika Padukone reported her jewelry stolen.', 'Open', 3, 3),
('Kidnapping', '2024-04-20', 'Hyderabad, India', 'Hrithik Roshan was kidnapped and later found.', 'Closed', 4, 4),
('Assault', '2024-05-25', 'Pune, India', 'Salman Khan was assaulted at an event.', 'Under Investigation', 5, 5),
('Burglary', '2024-06-30', 'Kolkata, India', 'Alia Bhatt’s house was broken into.', 'Open', 6, 6),
('Fraud', '2024-07-05', 'Bangalore, India', 'Ranbir Kapoor was scammed in a real estate deal.', 'Under Investigation', 7, 7),
('Murder', '2024-08-10', 'Jaipur, India', 'Kareena Kapoor found dead in her apartment.', 'Closed', 8, 8),
('Cyber Crime', '2024-09-15', 'Lucknow, India', 'Ranveer Singh’s social media was hacked.', 'Open', 9, 9),
('Drug Possession', '2024-10-20', 'Ahmedabad, India', 'Ajay Devgn caught with illegal substances.', 'Under Investigation', 10, 10);

INSERT INTO Officers (FirstName, LastName, BadgeNumber, `Rank`, ContactInformation, AgencyID) VALUES
('Tom', 'Cat', 'TC001', 'Inspector', 'tom@police.com', 1),
('Jerry', 'Mouse', 'JM002', 'Detective', 'jerry@police.com', 2),
('Mickey', 'Mouse', 'MM003', 'Sergeant', 'mickey@police.com', 3),
('Donald', 'Duck', 'DD004', 'Chief', 'donald@police.com', 4),
('Scooby', 'Doo', 'SD005', 'Lieutenant', 'scooby@police.com', 5),
('Bugs', 'Bunny', 'BB006', 'Commissioner', 'bugs@police.com', 6),
('Daffy', 'Duck', 'DF007', 'Detective', 'daffy@police.com', 7),
('Popeye', 'Sailor', 'PS008', 'Officer', 'popeye@police.com', 8),
('Shaggy', 'Rogers', 'SR009', 'Sergeant', 'shaggy@police.com', 9),
('SpongeBob', 'SquarePants', 'SP010', 'Constable', 'spongebob@police.com', 10);

INSERT INTO Evidence (Description, LocationFound, IncidentID) VALUES
('A stolen diamond ring', 'Mumbai Jewelry Store', 1),
('A bloody knife', 'Hotel Room, Delhi', 2),
('A missing laptop', 'Chennai House', 3),
('Fingerprints on a bottle', 'Hyderabad Park', 4),
('CCTV footage of the assault', 'Pune Event Hall', 5),
('A broken window', 'Alia Bhatt’s house, Kolkata', 6),
('Fake property documents', 'Real Estate Office, Bangalore', 7),
('A gun found near the scene', 'Jaipur Apartment', 8),
('Hacked social media account', 'Bangalore Office', 9),
('Illegal drugs found in car', 'Ahmedabad Highway', 10);

INSERT INTO Reports (IncidentID, ReportingOfficer, ReportDate, ReportDetails, Status) VALUES
(1, 1, '2024-01-06', 'Initial investigation started. CCTV footage being reviewed.', 'Under Investigation'),
(2, 2, '2024-02-11', 'Autopsy completed. Case closed as confirmed homicide.', 'Closed'),
(3, 3, '2024-03-16', 'Theft reported. No suspects identified yet.', 'Open'),
(4, 4, '2024-04-21', 'Victim found safe. Kidnappers in custody.', 'Closed'),
(5, 5, '2024-05-26', 'Suspect identified from event footage. Arrest pending.', 'Under Investigation'),
(6, 6, '2024-07-01', 'Entry through window confirmed. Forensics underway.', 'Open'),
(7, 7, '2024-07-06', 'Fraudulent documents submitted. Case under review.', 'Under Investigation'),
(8, 8, '2024-08-11', 'Victim’s death ruled as murder. Investigation complete.', 'Closed'),
(9, 9, '2024-09-16', 'Hacking traced to overseas server. Cyber team alerted.', 'Open'),
(10, 10, '2024-10-21', 'Drugs found in suspect’s vehicle. Lab results awaited.', 'Under Investigation');















