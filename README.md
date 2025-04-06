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
"streamlit run titanic.py"


The app will open in your browser. You can:
- Upload CSV or Excel files.
- Choose the file and the number of rows to display.
- Ask questions about the dataset.
- View visualizations, such as a histogram of "Age" and bar plots of "Survived" by "Sex."
- View and reuse past questions and answers.
- Provide feedback on the answers.



## Structure
1. titanic.py: Main Python file with the logic for uploading files, querying OpenAI, displaying results, and handling data visualizations.
2. key.env: Store your OpenAI API key securely (not included in the repo and is specified in .gitignore, add it manually).
3. train.csv, test.csv: Example Titanic dataset CSV files to use with the app.

