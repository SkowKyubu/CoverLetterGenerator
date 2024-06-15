import json
import easygui as eg
from openai import OpenAI, OpenAIError


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def update_chatgpt_api(api_key, json_file="content.json"):
    """update the api key"""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        data['api_chatgpt'] = api_key

        # Write the updated data back to the JSON file
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"\n{Bcolors.OKGREEN}ChatGPT API key updated successfully.{Bcolors.ENDC}\n")
        return api_key
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("Error: Could not read company information from the JSON file.")
        return None


def update_personal_info(json_file="content.json"):
    """update your personal info"""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        personal_info = data['personal_info']

        # Ask for personal information
        print(f"{Bcolors.BOLD}{Bcolors.UNDERLINE}Fill with your personal information{Bcolors.ENDC}: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        phone_number_fr = input("French phone number (07.XX.XX.XX.XX): ")
        phone_number_en = input("International phone number (+33.X.XX.XX.XX.XX): ")
        address_fr = input("Your address in French (without the city and postal code): ")
        address_en = input("Your address in English (without the city and postal code): ")
        city = input("City: ")
        country = input("Country: ")
        postal_code = input("Postal code: ")
        email = input("Email: ")

        # Update the personal information in the JSON structure
        personal_info['first_name'] = first_name
        personal_info['last_name'] = last_name
        personal_info['phone_number']['fr'] = phone_number_fr
        personal_info['phone_number']['en'] = phone_number_en
        personal_info['address']['fr'] = address_fr
        personal_info['address']['en'] = address_en
        personal_info['city'] = city
        personal_info['country'] = country
        personal_info['postal_code'] = postal_code
        personal_info['email'] = email

        # Write the updated data back to the JSON file
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"\n{Bcolors.OKGREEN}Personal information updated successfully.{Bcolors.ENDC}\n")

    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("Error: Could not read company information from the JSON file.")
        return None


def update_company_info(json_file="content.json"):
    """update company info"""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        company_info = data['company_info']

        # Ask for company information
        print(f"{Bcolors.BOLD}{Bcolors.UNDERLINE}Fill with the company information{Bcolors.ENDC}: ")
        name = input("Name of the company: ")
        sector = input("Sector: ")
        country = input("Country: ")
        city = input("City: ")
        job_name = input("Job name: ")
        contract_type = input("Kind of contract: ")
        reference = input("Job reference: ")
        job_description = eg.textbox(msg="Job description: ")

        # Update the personal information in the JSON structure
        company_info['name'] = name
        company_info['sector'] = sector
        company_info['location']['country'] = country
        company_info['location']['city'] = city
        company_info['job']['name'] = job_name
        company_info['job']['contract_type'] = contract_type
        company_info['job']['reference'] = reference
        company_info['job']['description'] = job_description

        # Write the updated data back to the JSON file
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"\n{Bcolors.OKGREEN}Company information updated successfully.{Bcolors.ENDC}\n")

    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("Error: Could not read company information from the JSON file.")
        return None


def get_content(json_file="C:/Users/artga/Desktop/scrapp_test/content.json"):
    """get the content of the json file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['introduction']['fr']
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("Error: Could not read company information from the JSON file.")
        return None


def test_api(api_key):
    try:
        print(f"Attempting to connect with API key: {api_key[:4]}... (truncated for security)")
        client = OpenAI(api_key=api_key)
        # Perform a simple API call to verify the connection
        client.chat.completions.create(model='gpt-3.5-turbo-0125',
                                       messages=[{"role": "user", "content": "say hello"}],
                                       max_tokens=1)
        print("Successfully connected to OpenAI API.")
        return True
    except ValueError as ve:
        print(f"Configuration error: {ve}")
        return False
    except OpenAIError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        return False
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        return False


def connexion_openai(api_key):
    while not test_api(api_key):
        api_key = input("API key: ")
    update_chatgpt_api(api_key)
    return OpenAI(api_key=api_key)


def get_completion(prompt, model="gpt-4o", client=None):
    if client is None:
        print('Define client')
    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": "You are a recent graduate in data science looking for a job. You need to write a paragraph for a cover letter using a template. Focus on your skills and motivation for the sector you are applying for, and do not invent projects or experience you never did."},
            {"role": "system",
             "content": "You really need to stick to the template I provide, and return only the template without quotes around, nothing more."},
            {"role": "system",
             "content": "Do not invent project to justify interest, talk about your wish to work in the sector"},
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    output = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            output += chunk.choices[0].delta.content
    return output
