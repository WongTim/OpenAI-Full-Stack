# OpenAI Titanic Dataset Query App
This is a simple web application built with Streamlit that allows users to upload CSV or Excel files (such as the Titanic dataset), ask questions about the data, and receive AI-generated answers using OpenAI's GPT-3.5-turbo model. The app also stores a history of prompts, allowing users to re-use previous questions and answers. Additionally, users can provide feedback on the answers they receive.



## Features
- Upload CSV/Excel files: Upload one or more files for analysis.
- Data Querying: Ask questions about the data and get AI-generated answers.
- Prompt History: View and reuse past prompts and answers.
- Data Visualization: View histograms and bar plots for columns like "Age" and "Survived" from the Titanic dataset.
- User Feedback: Rate the usefulness of the AI's answers and provide feedback.



## To run the program
Paste this command into the command prompt:
`streamlit run titanic.py`


The app will open in your browser. You can:
- Upload CSV or Excel files.
- Choose the file and the number of rows to display.
- Ask questions about the dataset.
- View visualizations, such as a histogram of "Age" and bar plots of "Survived" by "Sex."
- View and reuse past questions and answers.
- Provide feedback on the answers.



## Structure
1. `titanic.py`: Main Python file with the logic for uploading files, querying OpenAI, displaying results, and handling data visualizations.
2. `key.env`: Store your OpenAI API key securely (not included in the repo and is specified in .gitignore, add it manually).
3. `train.csv`, test.csv: Example Titanic dataset CSV files to use with the app.


## Known Issue: "Ask Question" Feature Not Working Properly

# Problem:
The "Ask Question" feature is currently encountering an issue due to recent changes in the OpenAI API. Specifically, the openai.Completion method is no longer supported in versions of the `OpenAI Python package >=1.0.0`. As a result, querying the dataset through the app generates an error.


# Cause:
- The OpenAI API has transitioned to a new interface where openai.Completion is deprecated. 
- The current OpenAI Python package version (1.0.0 and above) is incompatible with the existing code that uses openai.Completion.


# Solution:
There are two potential solutions to resolve this issue:
1. Upgrade the Code to Support `OpenAI API 1.0.0+`:
2. Update the code to use the new openai.ChatCompletion method instead of openai.Completion. A detailed migration guide is available to assist with these changes.


# Use the Previous Version of OpenAI (Temporary Solution):
If updating the code is not feasible immediately, you can downgrade the OpenAI package to version 0.28, which supports the openai.Completion method. To install this version, run: `pip install openai==0.28`

This will allow the "Ask Question" feature to function as expected without requiring immediate code changes.
