from coverletter import *
from utils import *

# Update your personal information if needed - you can uncomment this line after your first usage
update_personal_info()

# Update the company information
update_company_info()

# Create a CoverLetter instance with the desired language ('en' for English, 'fr' for French)
cover_letter = CoverLetter(language='en')

# Generate and write the cover letter
cover_letter.write_letter()
