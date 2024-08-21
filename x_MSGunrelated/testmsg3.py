import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from docx import Document

# Hardcoded Excel file path
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

# Function to handle the search and replacement
def process_input():
    word_path = word_entry.get()
    save_path = save_entry.get()
    search_value = input_entry.get()

    if not word_path or not save_path or not search_value:
        messagebox.showwarning("Input Error", "Please provide the Word file, save location, and search value.")
        return

    column_name = 'Company Name'

    # Find the last row where the value appears
    last_row_data = find_last_row(column_name, search_value)
    
    if last_row_data is not None:
        columns = list(last_row_data.index)
        try:
            doc = Document(word_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Word document. Please check the file path.\nError: {str(e)}")
            return
        
        successfully_replaced = []
        not_replaced = []
        
        for value in columns:
            was_replaced = False
            for paragraph in doc.paragraphs:
                if f"__{value}__" in paragraph.text:
                    replace_value = last_row_data[f"{value}"]
                    paragraph.text = paragraph.text.replace(f"__{value}__", replace_value)
                    successfully_replaced.append(value)
                    was_replaced = True
                    break  # Exit loop after finding and replacing in the first matching paragraph

            if not was_replaced:
                not_replaced.append(value)

        # Save the filled document
        try:
            doc.save(save_path)
            messagebox.showinfo("Success", f"Document saved successfully at: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save Word document.\nError: {str(e)}")
            return

        # Display success and failure results in a list format
        show_results(successfully_replaced, not_replaced)

    else:
        messagebox.showwarning("Not Found", f"The value '{search_value}' was not found in column '{column_name}'.")

# Function to show the results in two columns
def show_results(successfully_replaced, not_replaced):
    results_window = tk.Toplevel(root)
    results_window.title("Import Results")

    tk.Label(results_window, text="Successfully Imported", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, padx=10, pady=10)
    tk.Label(results_window, text="Not Imported", font=('Helvetica', 12, 'bold')).grid(row=0, column=1, padx=10, pady=10)
    
    for i, value in enumerate(successfully_replaced):
        tk.Label(results_window, text=value).grid(row=i+1, column=0, padx=10, pady=5)
    
    for i, value in enumerate(not_replaced):
        tk.Label(results_window, text=value).grid(row=i+1, column=1, padx=10, pady=5)

# Function to browse for the input Word file
def browse_word():
    filename = filedialog.askopenfilename(filetypes=[("Word files", "*.docx"), ("All files", "*.*")])
    word_entry.delete(0, tk.END)
    word_entry.insert(0, filename)

# Function to browse for the save location
def browse_save_location():
    filename = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word files", "*.docx"), ("All files", "*.*")])
    save_entry.delete(0, tk.END)
    save_entry.insert(0, filename)

# GUI Setup
root = tk.Tk()
root.title("Excel to Word Replacement Tool")

tk.Label(root, text="Select the input Word file:").pack(pady=5)
word_frame = tk.Frame(root)
word_frame.pack(pady=5)
word_entry = tk.Entry(word_frame, width=40)
word_entry.pack(side=tk.LEFT, padx=5)
word_browse_btn = tk.Button(word_frame, text="Browse", command=browse_word)
word_browse_btn.pack(side=tk.LEFT)

tk.Label(root, text="Select the save location:").pack(pady=5)
save_frame = tk.Frame(root)
save_frame.pack(pady=5)
save_entry = tk.Entry(save_frame, width=40)
save_entry.pack(side=tk.LEFT, padx=5)
save_browse_btn = tk.Button(save_frame, text="Browse", command=browse_save_location)
save_browse_btn.pack(side=tk.LEFT)

tk.Label(root, text="Enter the Company Name to search for:").pack(pady=10)
input_entry = tk.Entry(root, width=30)
input_entry.pack(pady=5)

process_button = tk.Button(root, text="Process", command=process_input)
process_button.pack(pady=20)

root.mainloop()
