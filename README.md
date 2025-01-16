# Darwin

![alt text](https://i.imgur.com/O8vZHPM.png)

> This project was built as part of the Data-Driven VC Hackathon organized by [Red River West](https://redriverwest.com) & [Bivwak! by BNP Paribas](https://bivwak.bnpparibas/)

![Darwin](https://i.imgur.com/roAY5dr.png)

The human brain works by analogy. Therefore, we decided that the best way to help VCs understand a given company is by generating a market map of its competitive landscape.

## Introducing Darwin

Darwin visualizes the competitive environment of a company. Say goodbye to endless, unreadable Excel sheets and risky comparisons. From the first meeting, Darwin creates a tree map that displays the company's competitors based on their attractiveness:

- The more attractive the company, the greener it appears
- Less attractive companies are shown in red
- Companies are displayed in segments, with the closest competitors grouped in the same category

By comparing the target company with its peers and across categories, VCs can instantly grasp the target's position and function. Clicking on a specific company provides the VC with insights into its strengths and weaknesses, along with a key question to break the ice during the first meeting.

## Prerequisites

Before you begin, ensure you have the following installed on your computer:

1. **Python 3.11.6**
   - Download from [Python's official website](https://www.python.org/downloads/release/python-3116/)
   - During installation, make sure to check "Add Python to PATH"

2. **API Keys**
   You'll need the following API keys (all free to start):
   - [OpenAI API Key](https://platform.openai.com/api-keys)
   - [PredictLeads API Key](https://predictleads.com/api-docs)
   - [SimilarWeb REST API Key](https://www.similarweb.com/corp/developer/apis/)
   - [Harmonic API Key](https://harmonic.ai/api-docs)

## Installation Guide

1. **Download the Project**
   Choose one of these methods:

   Option A: Download ZIP
   - Click the green "Code" button above
   - Select "Download ZIP"
   - Extract the ZIP file to a location on your computer

   Option B: Clone with Git
   - Open Terminal (Mac) or Command Prompt (Windows)
   - Navigate to where you want to store the project
   - Run: `git clone https://github.com/yourusername/darwin.git`

2. **Set Up Environment Variables**
   - Locate the file named `.env.example` in the project folder
   - Make a copy of this file and rename it to `.env`
   - Open the `.env` file with any text editor (like Notepad)
   - Replace the placeholder values with your API keys:
     ```
     OPENAI_API_KEY=your_openai_key_here
     PREDICT_LEAD_AUTH_KEY=your_predictlead_key_here
     PREDICT_LEAD_AUTH_TOKEN=your_predictlead_token_here
     SIMILARWEB_API_KEY=your_similarweb_key_here
     HARMONIC_API_KEY=your_harmonic_key_here
     ```

3. **Install Required Software**
   - Open Terminal (Mac) or Command Prompt (Windows)
   - Navigate to the project folder:
     ```bash
     # On Windows
     cd path\to\your\extracted\folder

     # On Mac/Linux
     cd path/to/your/extracted/folder
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

## Running Darwin

1. **Start the Application**
   ```bash
   python app.py
   ```

2. **Access the Interface**
   - Open your web browser
   - Go to: http://127.0.0.1:5000/
   - You should see the Darwin interface

## Troubleshooting

Common issues and solutions:

1. **"Python not found" error**
   - Make sure Python is installed correctly
   - Try running `python --version` to verify installation

2. **"pip not found" error**
   - Try using `python -m pip` instead of just `pip`

3. **API Key errors**
   - Double-check that your `.env` file is in the correct location
   - Verify that all API keys are copied correctly with no extra spaces

4. **Installation errors**
   - Try updating pip: `python -m pip install --upgrade pip`
   - If on Windows, try running Command Prompt as Administrator


## How It Works

1. Enter the URL of the target company
2. Using this URL, we leverage the [Harmonic](https://harmonic.ai/) API to identify the most comparable companies
3. Among these comparable companies, we often find numerous outliers. To filter them out:
   - We enrich these companies using data from [Similarweb](https://www.similarweb.com/) and [PredictLeads](https://predictleads.com/)
   - GPT then helps us qualify these companies as either relevant or outliers
4. Once outliers are identified, we enhance the relevant companies with three key questions:
   - What are this company's strengths?
   - What are its weaknesses?
   - What question would you ask as a potential investor?
5. The investor receives a tree map displaying the company within its competitive ecosystem