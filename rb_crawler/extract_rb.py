import requests
from parsel import Selector

from build.gen.bakdata.corporate.v1.corporate_pb2 import Corporate, Status, Officer
from rb_producer import RbProducer

justiz_id = {"be": "F1103R"}
black_list = [369803]


class ExtractRb:
    def __init__(self, start_rb_id: int, land: str):
        self.rb_id = start_rb_id
        self.land = land
        self.producer = RbProducer()

    def extract(self):
        # while True:
        for self.rb_id in [367482, 454067, 503622, 600425]:
            if self.rb_id in black_list:
                self.rb_id = self.rb_id + 1
                continue
            print(f"Sending Request for: {self.rb_id}")
            get = requests.get(
                f"https://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?rb_id={self.rb_id}&land_abk={self.land}"
            ).text
            selector = Selector(text=get)
            corporate = Corporate()
            company_code = self.extract_company_aktenzeichen(selector)
            event_date = selector.xpath("/html/body/font/table/tr[4]/td/text()").get()
            corporate.event_date = event_date
            print(f"Date of event: {event_date}")
            corporate.id = f"{justiz_id[self.land]}_{company_code.replace(' ', '')[:-1]}"
            event_type = selector.xpath("/html/body/font/table/tr[3]/td/text()").get()
            raw_text: str = selector.xpath("/html/body/font/table/tr[6]/td/text()").get()

            if event_type == "Neueintragungen":
                self.handle_new_entries(corporate, raw_text, company_code)
                pass
            elif event_type == "Veränderungen":
                self.handle_changes(corporate, raw_text)
                pass
            elif event_type == "Löschungen":
                self.handle_deletes(corporate)
                pass
            self.rb_id = self.rb_id + 1
            print(corporate)
            print(f"-------------------------------------------------------------------------------")

    def handle_new_entries(self, corporate: Corporate, raw_text: str, company_code: str) -> Corporate:
        general_info: list = raw_text.split(";")
        if len(general_info) > 4:
            corporate.event_type = "newEntry"
            corporate.name = self.extract_company_name(raw_text, company_code)
            print(f"new company found: {corporate.id}")
            print(f"company name is: {corporate.name}")

            corporate.address = self.extract_address(raw_text)
            print(f"address is: {corporate.address}")
            company_description_capital = (
                general_info[3].replace("Gegenstand: ", "").split("Stamm- bzw. Grundkapital: ")
            )

            if len(company_description_capital) == 2:
                corporate.description = company_description_capital[0]
                corporate.capital = company_description_capital[1]
            else:
                corporate.description = company_description_capital[0]

            list_officers = self.extract_officers(raw_text)
            corporate.officers.extend(list_officers)
            corporate.status = Status.STATUS_ACTIVE
        else:
            print(f"Skipping company with reference: {self.rb_id}")

        self.producer.produce_to_topic(corporate=corporate)

    def handle_changes(self, corporate: Corporate, raw_text: str):
        print(f"Changes are made to company: {corporate.id}")
        corporate.status = Status.Status.STATUS_ACTIVE

        if "Sitz / Zweigniederlassung: Geschäftsanschrift: " in raw_text:
            corporate.event_type = "update::changeAddress"
            corporate.address = self.extract_address(raw_text)

            self.producer.produce_to_topic(corporate=corporate)

        if "Nicht mehr Geschäftsführer: " in raw_text:
            corporate.event_type = "update::officerRemoval"
            removed_officer = raw_text.split("Nicht mehr Geschäftsführer: ")[1]
            officer_index = removed_officer.split(" ")[0]
            # 1. Müller, Hannelore ---Split by ,---> ["1. Müller", " Hannelore; <rest_of_the_text>"]
            officer_name = removed_officer.split(",")
            removed_officer = Officer()
            removed_officer.index = int(officer_index[:-1])
            removed_officer.status = Status.STATUS_INACTIVE
            removed_officer.first_name = officer_name[1].split(";")[0]
            removed_officer.last_name = officer_name[0].replace(officer_index, "")[1:]
            corporate.officers.append(removed_officer)

            # TODO Handle situations when a new officer is also announced
            # new_officer = officer_name[1].split(';')
            # if len(new_officer) > 2:
            #     self.extract_officers()
            # print(new_officer)

            self.producer.produce_to_topic(corporate=corporate)
        pass

    def handle_deletes(self, corporate: Corporate):
        print(f"Company {corporate.id} is inactive")
        corporate.status = Status.STATUS_INACTIVE
        self.producer.produce_to_topic(corporate=corporate)

    @staticmethod
    def extract_company_aktenzeichen(sel):
        return ((sel.xpath("/html/body/font/table/tr[1]/td/nobr/u/text()").get()).split(": ")[1])[:-1]

    @staticmethod
    def extract_company_name(raw_text, company_code):
        company_name_address = raw_text.split(",")
        return company_name_address[0].replace(f"{company_code}: ", "")

    @staticmethod
    def extract_address(raw_text):
        company_name_address = raw_text.split(",")
        company_address = f"{company_name_address[2]},{company_name_address[3].split('.')[0]}"[1:]
        return company_address

    @staticmethod
    def extract_officers(raw_text: str) -> list:
        list_officers = []
        index = 1
        for full_officer_info in raw_text.split("Geschäftsführer: ")[1:]:
            full_officer_info: str = (full_officer_info.split(";")[0]).split("\n")[1]
            officer_info_list: list = full_officer_info.split(", ")
            officer = Officer()
            officer.index = index
            officer.status = Status.STATUS_ACTIVE
            officer.first_name = officer_info_list[1]
            officer.last_name = officer_info_list[0]
            officer.birthday = officer_info_list[2][1:]
            officer.birth_location = officer_info_list[3]
            index = index + 1
            list_officers.append(officer)
        return list_officers
