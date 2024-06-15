
# Cover Letter generator
<p align="center">
  <img src="https://github.com/SkowKyubu/CoverLetterGenerator/assets/120100522/536455d9-73bc-4162-82c7-73b0d42a6157" alt="letter">
</p>

Generate personalized cover letters instantly by filling out a simple form with details of the job you’re applying for. Receive your cover letter in PDF and DOCX (for additional customization) formats within seconds.

- Introduction
- Presentation of your skills and background, who you are, and why you are applying
- A paragraph discussing your international internship experiences
- A paragraph expressing your interest in the specific job offer
- Conclusion
The program can generate letters in both English and French and allows for adaptation based on the type of contract, specifically V.I.E contracts.

## How to Use
### 1. Set Up Your Environment

Make sure you have Python installed on your computer. Then, install the required dependencies:

```
pip install -r requirements.txt
```

### 2. Obtain Your OpenAI API Key

To generate paragraphs related to your interest in the mission and the company, you will need an OpenAI API key. Sign up on [OpenAI's website](https://openai.com/index/openai-api/) and obtain your API key.

### 3. Prepare Your `content.json` File and `template.docx`.
Open and customize the `content.json` file to match your profile. This file should include sections such as introduction, skills and background, international internship experiences, interest in the job offer, and conclusion. Use the current content as an example. You can modify the signature image in the `template.docx` file with your own one.

### 4. Run `main.py`
You can now run this script and you will be asked for information about the company and the mission you are applying for.
- After your first usage, you can comment the function `update_personal_info()` to avoid having to enter your personal information each time you use the program.


## Note:
- The model uses `gpt-4o`, which costs $0.01 USD per 1K tokens. The prompt used to generate the personalized paragraph (including the description) should be around 800 tokens. Therefore, the cost of each generated letter will be less than $0.01 USD. However, you can change the [ChatGPT model](https://openai.com/api/pricing/) used by adjusting the parameter in the `get_completion()` function in the `utils.py` script.
