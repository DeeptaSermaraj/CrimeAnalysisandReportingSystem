class Incident:
    def __init__(self, incident_id, incident_type, description, date, status):
        self.__incident_id = incident_id
        self.__incident_type = incident_type
        self.__description = description
        self.__date = date
        self.__status = status


    def get_incident_id(self):
        return self.__incident_id

    def get_incident_type(self):
        return self.__incident_type

    def get_description(self):
        return self.__description

    def get_date(self):
        return self.__date

    def get_status(self):
        return self.__status


    def set_status(self, status):
        self.__status = status
