class Case:
    def __init__(self, case_id, case_description, incidents):
        self.__case_id = case_id
        self.__case_description = case_description
        self.__incidents = incidents


    def get_case_id(self):
        return self.__case_id

    def get_case_description(self):
        return self.__case_description

    def get_incidents(self):
        return self.__incidents


    def set_case_description(self, case_description):
        self.__case_description = case_description

    def add_incident(self, incident):
        self.__incidents.append(incident)
