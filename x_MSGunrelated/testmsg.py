import pandas as pd
from docx import Document

# Load Excel data
excel_file = r"C:\Users\rybot\OneDrive\Desktop\Test Form to Word.xlsx"
df = pd.read_excel(excel_file)

# Function to find the last row where a value appears in a specific column
def find_last_row(column_name, search_value):
    matching_rows = df[df[column_name] == search_value]
    if not matching_rows.empty:
        last_row_index = matching_rows.index[-1]
        return df.loc[last_row_index]
    else:
        return None  # Return None if the value is not found

# Input the column name and the value to search for
column_name = 'Company Name'
search_value = input("Enter the value to search for: ")

# Find the last row where the value appears
last_row_data = find_last_row(column_name, search_value)

if last_row_data is not None:

    columns = ['Company Name','What do you do','Did you Know','Are you Guilty']
    
    doc = Document(r"C:\Users\rybot\OneDrive\Desktop\Test company data form.docx")

    for paragraph in doc.paragraphs:
        for value in columns:
            replace_value = last_row_data[f"{value}"]
            if f"__{value}__" in paragraph.text:
                paragraph.text = paragraph.text.replace(f"__{value}__", replace_value)


    # Save the filled document
    doc.save(r"C:\Users\rybot\OneDrive\Desktop\Test company data form2.docx")

    print(f"Document saved successfully with data from the last occurrence of '{search_value}' in column '{column_name}'.")
else:
    print(f"The value '{search_value}' was not found in column '{column_name}'.")
