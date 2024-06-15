import os
import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
import locale
from utils import *


class CoverLetter:
    def __init__(self, language='fr', json_file="content.json", template_file="template.docx"):
        self.__language = language
        self.__json_file = json_file
        self.__template_file = template_file
        self.__content = self._get_content()
        self._set_company_info()
        self._set_job_info()
        self._set_personal_info()
        if self.__language == 'fr':
            # Set the locale to French for month names
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        # Load openAI client
        self.__client_openai = connexion_openai(self.__content['api_chatgpt'])

    def _get_content(self):
        """Load and return the content from a JSON file."""
        try:
            with open(self.__json_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            raise ValueError("Error: Could not read company information from the JSON file.")

    def _set_company_info(self):
        """Set company-related information from the content."""
        company_info = self.__content.get('company_info', {})
        location = company_info.get('location', {})
        job = company_info.get('job', {})
        self.__company_name = company_info.get('name', 'Unknown')
        self.__company_sector = company_info.get('sector', 'Unknown')
        self.__company_country = location.get('country', 'Unknown')
        self.__company_city = location.get('city', 'Unknown')
        self.__contract_type = job.get('contract_type', 'Unknown')
        self.__job_name = job.get('name', 'Unknown')
        self.__job_reference = job.get('reference', 'Unknown')
        self.__job_description = job.get('description', 'No description available')

    def _set_personal_info(self):
        """Set personal information from the content."""
        personal_info = self.__content.get('personal_info', {})
        self.__personal_first_name = personal_info.get('first_name', 'Unknown')
        self.__personal_last_name = personal_info.get('last_name', 'Unknown')
        self.__personal_phone_number = personal_info.get('phone_number', {}).get(self.__language, 'Unknown')
        self.__personal_address = personal_info.get('address', {}).get(self.__language, 'Unknown')
        self.__personal_city = personal_info.get('city', 'Unknown')
        self.__personal_country = personal_info.get('country', 'Unknown')
        self.__personal_postal_code = personal_info.get('postal_code', 'Unknown')
        self.__personal_email = personal_info.get('email', 'Unknown')

    def _set_job_info(self):
        """Set job-related information from the content."""
        job = self.__content.get('company_info', {}).get('job', {})
        self.__job_name = job.get('name', 'Unknown')
        self.__contract_type = job.get('contract_type', 'Unknown')
        self.__job_description = job.get('description', 'No description available')

    def _get_date_location(self, city='Niort', country='France'):
        """Return the current date and location formatted based on the language."""
        now = datetime.datetime.now()
        if self.__language == 'fr':
            # French date format:
            date_str = now.strftime('%A %d %B %Y').capitalize()
        else:
            # English (default) date format: April 23rd, 2024
            day = now.strftime('%d').lstrip('0')
            suffix = 'th' if 11 <= int(day) <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(int(day) % 10, 'th')
            date_str = now.strftime(f'%B {day}{suffix}, %Y')

        return f'{date_str}, {city}, {country}'

    def _get_object_letter(self):
        """Return the object line of the cover letter based on the language and contract type."""
        contract = 'VIE ' if self.__contract_type == 'VIE' else ''
        if self.__language == 'fr':
            return f'Objet : Candidature pour le poste {contract}de {self.__job_name} chez {self.__company_name}'
        return f'Object: Application for the {self.__job_name} {contract}position at {self.__company_name}'

    def _get_greetings(self):
        """Return the greeting line of the cover letter based on the language."""
        return 'Madame, monsieur' if self.__language == 'fr' else 'Dear hiring manager'

    def _get_end_politeness(self):
        """Return the end politeness line of the cover letter based on the language."""
        return 'Cordialement,' if self.__language == 'fr' else 'Warm regards,'

    def _get_introduction(self):
        """Return the introduction paragraph of the cover letter based on the language and contract type."""
        introduction = self.__content['introduction'][self.__language]
        if self.__contract_type == 'VIE':
            vie_info = self.__content['introduction']['VIE'][self.__language]
            introduction += ' ' + vie_info
        introduction = introduction.replace("{{company_name}}", self.__company_name)
        introduction = introduction.replace("{{company_sector}}", self.__company_sector)
        return introduction

    def _get_presentation(self):
        """Return the presentation paragraph of the cover letter based on the language and contract type."""
        presentation = self.__content['presentation']['data science'][self.__language]
        return presentation.replace("{{company_name}}", self.__company_name)

    def _get_international_experience(self):
        """Return the international experience paragraph of the cover letter based on the language and contract type."""
        international_experience = self.__content['international_experience'][self.__language]
        if self.__contract_type == 'VIE':
            international_experience = self.__content['international_experience']['VIE'][self.__language]
        international_experience = international_experience.replace("{{company_country}}", self.__company_country)
        international_experience = international_experience.replace("{{company_name}}", self.__company_name)
        return international_experience

    def _get_company_interest(self):
        """Return the company interest paragraph"""
        company_interest = self.__content['company_interest'][self.__language]
        if self.__contract_type == 'VIE':
            company_interest = self.__content['company_interest']['VIE'][self.__language]

        company_interest = company_interest.replace("{{company_name}}", self.__company_name)
        company_interest = company_interest.replace("{{job_name}}", self.__job_name)
        company_interest = company_interest.replace("{{company_country}}", self.__company_country)
        company_interest = company_interest.replace("{{company_sector}", self.__company_sector)
        prompt = company_interest + self.__content['company_info']['job']['description']
        output = get_completion(prompt=prompt, client=self.__client_openai)
        return output

    def _get_conclusion(self):
        """Return the conclusion paragraph of the cover letter based on the language and contract type."""
        conclusion = self.__content['conclusion'][self.__language]
        return conclusion.replace("{{company_name}}", self.__company_name)

    def _get_context(self):
        """Return the context dictionary for rendering the cover letter template."""
        return {
            "personal_first_name": self.__personal_first_name,
            "personal_last_name": self.__personal_last_name,
            "personal_phone_number": self.__personal_phone_number,
            "personal_address": self.__personal_address,
            "personal_city": self.__personal_city,
            "personal_country": self.__personal_country,
            "personal_postal_code": self.__personal_postal_code,
            "personal_email": self.__personal_email,
            "date_location": self._get_date_location(),
            "object_letter": self._get_object_letter(),
            "greetings": self._get_greetings(),
            "introduction": self._get_introduction(),
            "presentation": self._get_presentation(),
            "international_experience": self._get_international_experience(),
            "company_interest": self._get_company_interest(),
            "conclusion": self._get_conclusion(),
            "end_politeness": self._get_end_politeness()
        }

    def __message_VIE(self):
        message = self.__content['VIE_message'][self.__language]
        message = message.replace("{{job_name}}", self.__job_name)
        message = message.replace("{{company_name}}", self.__company_name)
        message = message.replace("{{company_city}}", self.__company_city)
        message = message.replace("{{reference}}", self.__job_reference)
        message = message.replace("{{personal_first_name}}", self.__personal_first_name)
        message = message.replace("{{personal_last_name}}", self.__personal_last_name)
        return message

    def write_letter(self, output_dir='coverletter'):
        """Create the cover letter document and save it to the specified directory."""
        context = self._get_context()
        doc = DocxTemplate(self.__template_file)
        doc.render(context)

        # Get the current date
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime("%y%m%d")

        # Create directories if they don't exist
        docx_dir = os.path.join(output_dir, 'docx')
        pdf_dir = os.path.join(output_dir, 'pdf')
        os.makedirs(docx_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)

        # File paths
        docx_filename = os.path.join(docx_dir,
                                     f'CoverLetter_{formatted_date}_{self.__company_name}_{self.__job_name}.docx')
        pdf_filename = os.path.join(pdf_dir,
                                    f'CoverLetter_{formatted_date}_{self.__company_name}_{self.__job_name}.pdf')

        # Save the docx file
        print(f"{Bcolors.BOLD}{Bcolors.UNDERLINE}Saving cover letter: {Bcolors.ENDC}: ")
        doc.save(docx_filename)

        # Convert to PDF
        convert(docx_filename, pdf_filename)

        # Print message for VIE
        if self.__contract_type == "VIE":
            print(f"\n{Bcolors.BOLD}{Bcolors.UNDERLINE}VIE message: {Bcolors.ENDC}: ")
            print(self.__message_VIE())
        return docx_filename, pdf_filename

    def display(self):
        """Display information about the cover letter."""
        print(f"Cover letter created for company: {self.__company_name}")
        print(f"Job name: {self.__job_name}")
        print(f"Location: {self.__company_city}, {self.__company_country}")
        print(f"Contract type: {self.__contract_type}")
        print(f"Job description: {self.__job_description}")
        print(f"Language: {self.__language}")
