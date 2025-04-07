import streamlit as st
import pandas as pd
import openai
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv




# Load environment variables from .env file
load_dotenv(dotenv_path="key.env")

# Retrieve OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")




# Store prompt history as a session state variable. This is for the previous prompts input by user
if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []


def upload_file():
    # Streamlit function to upload and accept multiple files. Only .xlsx or .csv extensions are accepted
    uploaded_files = st.file_uploader("Upload your CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)
    
    # Initialize the flag for tracking upload attempts
    if 'upload_attempted' not in st.session_state:
        st.session_state.upload_attempted = False

    if uploaded_files:
        st.session_state.upload_attempted = True  # User has attempted to upload
        data_dict = {}
        for uploaded_file in uploaded_files:
            try:
                # read_csv if it's a csv file
                if uploaded_file.name.endswith('.csv'):
                    data_dict[uploaded_file.name] = pd.read_csv(uploaded_file)
                # read_excel if it's an excel file
                elif uploaded_file.name.endswith('.xlsx'):
                    xls = pd.ExcelFile(uploaded_file)
                    sheet_names = xls.sheet_names
                    selected_sheet = st.selectbox(f"Select a sheet from {uploaded_file.name}", sheet_names)
                    data_dict[uploaded_file.name] = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                else:
                    # The function is written to accept only excel and csv files, but this is a last layer check
                    st.error(f"Invalid file type: {uploaded_file.name}. Please upload a valid CSV or Excel file.")
                    return None
            except Exception as e:
                # Display the error on screen 
                st.error(f"Error uploading file {uploaded_file.name}: {e}")
                return None
        return data_dict
    elif st.session_state.upload_attempted:
        # Show warning only if an upload was attempted 
        st.warning("Please upload a valid CSV or Excel file.")
    return None


def handle_large_data(data_string, token_limit=3500):
    """
    Truncates the dataset string if it exceeds the token limit.
    
    Parameters:
    data_string (str): The string representation of the dataset.
    token_limit (int): The maximum number of tokens allowed (default: 3500).
    
    Returns:
    str: The truncated dataset string, if necessary.
    """
    # Check if the data_string length exceeds the token limit
    if len(data_string) > token_limit:
        st.warning("Dataset is too large, truncating it for the query.")
        return data_string[:token_limit]  # Truncate to the token limit
    return data_string




def ask_question(data, question):
    """
    A helper function that takes in a dataset and its related question, and generates a corresponding answer

    Parameters: 
    data: The dataframe of the csv file
    question (str): Text input by the user

    """
    
    # Convert the DataFrame to a string (to pass as part of the prompt)
    data_string = data.to_string()

    # Truncate the data if it's too large to handle OpenAI's token limit. Models gpt3 and 4o have a token limit of 4096
    data_string = handle_large_data(data_string)

    # Create the prompt for OpenAI
    prompt = f"Provide a brief summary based on this dataset:\n\n{data_string[:2000]}\n\nQuestion: {question}"

    try:
        # Send the prompt to OpenAI using the gpt-3.5-turbo model. Thus, the response object would also have a prompt and response dictionary to store the chat
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

        # Extract the assistant's reply
        answer = response["choices"][0]["message"]["content"].strip()
        return answer  # Return the answer to the caller
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return None



def display_and_ask(data_dict):
    if data_dict:  # Check if data_dict is not None
        file_names = list(data_dict.keys())
        selected_file = st.selectbox("Select a file to view", file_names)
        data = data_dict[selected_file]
        
        # Allow the user to specify how many rows to display
        n_rows = st.slider(f"Select number of rows to display from {selected_file}", 1, 100, 10)
        st.write(data.head(n_rows))

        # Allow the user to ask a question about the selected data
        user_question = st.text_input(f"Ask a question about the data from {selected_file}")

        if user_question:
            # Get the answer from OpenAI by calling the helper function
            answer = ask_question(data, user_question)
            st.write(f"**Answer:** {answer}")
            
            # Add the question and answer to prompt history
            st.session_state.prompt_history.append({"file": selected_file, "question": user_question, "answer": answer})

        # Optionally, show the uploaded data for reference
        st.write(f"Here is the dataset you uploaded from {selected_file}:")
        st.write(data.head(n_rows))

        # Show visualizations for data columns
        show_visualizations(data)



# Function to visualize the data in histogram or bar plot using matplotlib
def show_visualizations(data):
    if st.button("Show Histogram of Age (if applicable)"):
        if 'Age' in data.columns:
            data['Age'].dropna().hist()  # Drop NaN values for clean visualization
            plt.title("Age Distribution")
            st.pyplot()
        else:
            st.warning("Age column not found in the dataset.")
    
    if st.button("Show Bar Plot of Survival by Sex (if applicable)"):
        if 'Survived' in data.columns and 'Sex' in data.columns:
            survival_by_sex = data.groupby('Sex')['Survived'].mean()
            survival_by_sex.plot(kind='bar', color=['blue', 'pink'])
            plt.title("Survival Rate by Sex")
            st.pyplot()
        else:
            st.warning("Survived and Sex columns not found in the dataset.")

# Function to display history of prompts and allow re-use
def display_prompt_history(data_dict):
    if st.session_state.prompt_history:
        st.write("### Previous Prompts and Answers:")
        for i, prompt_data in enumerate(st.session_state.prompt_history):
            question = prompt_data["question"]
            answer = prompt_data["answer"]
            file = prompt_data["file"]
            st.write(f"**{i+1}. File**: {file} | **Question**: {question}")
            st.write(f"**Answer**: {answer}")
            
            # Button to reuse prompt
            if st.button(f"Reuse Prompt {i+1}"):
                st.text_input("Reusing Question", value=question)
                answer = ask_question(data_dict[file], question)
                st.write(f"**Answer**: {answer}")


# Feedback Section for evaluating usefulness. It is called upon when you submit the radio button answer
def feedback_section():
    feedback = st.radio("Was this answer helpful?", ["Yes", "No"])
    if feedback == "No":
        feedback_text = st.text_area("Please provide feedback on how we can improve the answer:")
        if feedback_text:
            st.write("Thank you for your feedback!")


def main():
    st.title("OpenAI Full Stack Challenge")

    # Upload file and get its data
    data_dict = upload_file()

    # Check if valid data is available
    if data_dict is not None:
        display_and_ask(data_dict)
        display_prompt_history(data_dict)
        feedback_section()
    elif st.session_state.upload_attempted:
        # Explicitly handle the case where data upload was attempted but invalid
        st.error("No valid data uploaded. Please upload a valid CSV or Excel file.")

# Run the program as a standalone and not an imported module
if __name__ == "__main__":
    main()


