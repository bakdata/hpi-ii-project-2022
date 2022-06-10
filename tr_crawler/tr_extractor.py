import logging

import requests
from bs4 import BeautifulSoup

from build.gen.student.academic.v1.transparency_pb2 import Transparency, LegalRepresentatives, NamedEmployees, MembershipEntries, Donators, fieldsOfInterest, ClientOrganizations
from tr_producer import TrProducer
from tr_crawler.constant import LOBBY_BASE_URL, MAX_ATTEMPTS

log = logging.getLogger(__name__)

class TrExtractor():
    def __init__(self):
        self.producer = TrProducer()

    def _get_full_results(self) -> dict:
        page = requests.get("https://www.lobbyregister.bundestag.de/suche")
        soup = BeautifulSoup(page.content, "html.parser")

        # This extracts the url to download the JSON from the option in the Empty search (which gives all results) 
        # We could also siply extract the link from JSON (Sämtliche Detailprofile) but this would 
        # a) make it mildly harder to get historic data
        # b) make this exercise far too trivial
        expected_url = soup.find(text="JSON (Suchergebnisliste)").parent['value']

        # This retrieves the Entire Search results JSON
        try:
            log.info(f"Retrieving full index of Lobbyregister")
            full_results = requests.get(f"{LOBBY_BASE_URL}{expected_url}").json()
        except Exception as ex:
            log.error(f"could not retrieve, cause : {ex}")
            full_results = {}
        return full_results

    def _get_events_for_entry(self, url: str) -> list:
        """Gets all historical entries that realte to this entity returns it as a list"""
        log.info(f"getting all events at {url}")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return_list = []
        name = soup.find("h3").contents
        name = name[0]

        for item in soup.find(id="public-versions-entry").find_all('option'):
            sub_url = item.attrs['value']
            log.info(f"getting event for {sub_url}")
            result = requests.get(f"{LOBBY_BASE_URL}{sub_url.replace('suche', 'sucheJson')}")
            attempts = 0
            while result.status_code != 200:
                result = requests.get(f"{LOBBY_BASE_URL}{sub_url.replace('suche', 'sucheJson')}")
                attempts += 1
                if attempts > MAX_ATTEMPTS:
                    log.error(f"for url {url} things have gone wrong ")
                    break
            
            result = result.json()
            #kinda hacky and bad but come on why isnt the name in the JSON?
            result["name"] = name
            return_list.append(result)

            log.info(f"Length of return list {len(return_list)}")
        
        return return_list

    def _extract_protobuf_from_dict(self, event_dict: dict):
        trans = Transparency()

        trans.name = event_dict["name"]

        trans.register_number = event_dict["registerNumber"]
        trans.entry_id = event_dict["registerEntryDetail"]["id"]
        trans.employee_min = event_dict["registerEntryDetail"]["employeeCount"]["from"]
        trans.employee_max = event_dict["registerEntryDetail"]["employeeCount"]["to"]
        trans.refuse_expenses = event_dict["registerEntryDetail"]["refuseFinancialExpensesInformation"]

        if "financialExpensesEuro" in event_dict["registerEntryDetail"].keys():
            trans.expenses_min = event_dict["registerEntryDetail"]["financialExpensesEuro"]["from"]
            trans.expenses_max = event_dict["registerEntryDetail"]["financialExpensesEuro"]["to"]
            trans.fiscal_year = event_dict["registerEntryDetail"]["financialExpensesEuro"]["fiscalYearEnd"]

        trans.refuse_allowance = event_dict["registerEntryDetail"]["refusePublicAllowanceInformation"]
        trans.refuse_donation = event_dict["registerEntryDetail"]["refuseDonationInformation"]

        if "donationInformationRequired" in event_dict["registerEntryDetail"].keys():
            trans.donation_information_required = event_dict["registerEntryDetail"]["donationInformationRequired"]

        trans.firstPublicationDate = event_dict["registerEntryDetail"]["account"]["firstPublicationDate"]
        trans.account_inactive = event_dict["registerEntryDetail"]["account"]["inactive"]

        trans.lobbyistIdentity.identity = event_dict["registerEntryDetail"]["lobbyistIdentity"]["identity"]
        trans.lobbyistIdentity.name = event_dict["registerEntryDetail"]["lobbyistIdentity"]["name"]
        trans.lobbyistIdentity.address.street = event_dict["registerEntryDetail"]["lobbyistIdentity"]["address"]["street"]
        trans.lobbyistIdentity.address.streetNumber = event_dict["registerEntryDetail"]["lobbyistIdentity"]["address"]["streetNumber"]
        trans.lobbyistIdentity.address.zipCode = event_dict["registerEntryDetail"]["lobbyistIdentity"]["address"]["zipCode"]
        trans.lobbyistIdentity.address.city = event_dict["registerEntryDetail"]["lobbyistIdentity"]["address"]["city"]
        trans.lobbyistIdentity.address.country = event_dict["registerEntryDetail"]["lobbyistIdentity"]["address"]["country"]["code"]

        persons_list = []
        if "legalRepresentatives" in event_dict["registerEntryDetail"]["lobbyistIdentity"].keys():
            for person in event_dict["registerEntryDetail"]["lobbyistIdentity"]["legalRepresentatives"]:
                legalRep = LegalRepresentatives()
                legalRep.first_name = (person["commonFirstName"])
                legalRep.last_name = (person["lastName"])
                legalRep.function = (person["function"])
                persons_list.append(legalRep)
            trans.persons.extend(persons_list)

        employees_list = []
        if "namedEmployees" in event_dict["registerEntryDetail"]["lobbyistIdentity"].keys():
            for person in event_dict["registerEntryDetail"]["lobbyistIdentity"]["namedEmployees"]:
                employees = NamedEmployees()
                employees.first_name = (person["commonFirstName"])
                employees.last_name = (person["lastName"])
                employees_list.append(employees)
        trans.employees.extend(employees_list)

        organisations_list = []
        if "membershipEntries" in event_dict["registerEntryDetail"]["lobbyistIdentity"].keys():
            for organisation in event_dict["registerEntryDetail"]["lobbyistIdentity"]["membershipEntries"]:
                organisations = MembershipEntries()
                organisations.name = organisation
                organisations_list.append(organisations)
            trans.organisations.extend(organisations_list)

        companies_list = []
        if "donators" in event_dict["registerEntryDetail"].keys():
            for company in event_dict["registerEntryDetail"]["donators"]:
                companies = Donators()
                companies.name = company["name"]
                companies.fiscal_year = (company["fiscalYearEnd"])
                companies.donation_euro = (company["donationEuro"]["to"])
                companies_list.append(companies)
        trans.companies.extend(companies_list)

        fields_list = []
        if "fieldsOfInterest" in event_dict["registerEntryDetail"].keys():
            for field in event_dict["registerEntryDetail"]["fieldsOfInterest"]:
                fields = fieldsOfInterest()
                fields.name = (field["code"])
                if "fieldOfInterestText" in field.keys():
                    fields.description = (field["fieldOfInterestText"])
                fields_list.append(fields)
            trans.fields.extend(fields_list)

        clients_list = []
        if "clientOrganizations" in event_dict["registerEntryDetail"].keys():
            for client in event_dict["registerEntryDetail"]["clientOrganizations"]:
                clients = ClientOrganizations()
                clients.name = (client["name"])
                clients.adress.street = (client["address"]["street"])
                clients.adress.streetNumber = (client["address"]["streetNumber"])
                clients.adress.zipCode = (client["address"]["zipCode"])
                clients.adress.city = (client["address"]["city"])
                clients.adress.country = (client["address"]["country"]["code"])
                clients_list.append(clients)
            trans.clients.extend(clients_list)


        return trans


    def extract(self):

        full_results = self._get_full_results()

        for item in full_results['results']:
            log.info(f"Getting info for {LOBBY_BASE_URL}/suche/{item['registerNumber']}/{item['id']}")
            events = self._get_events_for_entry(f"{LOBBY_BASE_URL}/suche/{item['registerNumber']}/{item['id']}")

            for event in events:
                log.info(f"Extracting and sending event {event['registerNumber']} {event['registerEntryDetail']['id']} ")
                self.producer.produce_to_topic(self._extract_protobuf_from_dict(event))


    def _debug_extractor(self):

        trans = Transparency()
        transPerson = TransparencyPerson()

        trans.register_number="R999999"
        trans.entry_id=9999
        trans.employee_max=400
        trans.refuse_expenses=False
        trans.expenses_max=40000000

        transPerson.name = "Jochen Jochen"

        trans.persons.extend([transPerson])

        self.producer.produce_to_topic(trans)
