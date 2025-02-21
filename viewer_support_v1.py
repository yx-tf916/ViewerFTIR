import os

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import viewer

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

_debug = True  # False to eliminate debug printing from callback functions.

# viewer_support.py

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from viewer import Toplevel1

# Global variable to store the loaded spectra data
spectra_data = {}
app = None
file_paths = []
background_spectrum = None
background_file = None
primary_spectrum = None
primary_file = None
update_pending = False
displayed_data = None
isSinglePlot = False
singleFilename = None

def set_as_background():
    global background_spectrum, background_file
    selected_indices = app.Listbox1.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "No items selected to set as background.")
        return

    # Set the first selected item as the background
    index = selected_indices[0]
    file_name = app.Listbox1.get(index)

    if file_name in spectra_data: 
        background_spectrum = spectra_data[file_name]
        background_file = file_name

        app.Listbox1.delete(index)
        app.Listbox1.insert(index, f"{file_name} -")
    else:
        messagebox.showerror("Error", f"No data found for '{file_name}'")

def unset_as_background():
    global background_spectrum, background_file
    if background_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{background_file} -")
        app.Listbox1.delete(index)
        app.Listbox1.insert(index, background_file)
        
        background_spectrum = None
        background_file = None
    else:
        messagebox.showerror("Error", "No background is currently set.")

def set_as_primary():
    global primary_spectrum, primary_file
    selected_indices = app.Listbox1.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "No items selected to set as primary.")
        return

    index = selected_indices[0]
    file_name = app.Listbox1.get(index)

    if file_name in spectra_data: 
        primary_spectrum = spectra_data[file_name]
        primary_file = file_name

        app.Listbox1.delete(index)
        app.Listbox1.insert(index, f"{file_name} +")
    else:
        messagebox.showerror("Error", f"No data found for '{file_name}'")

def unset_as_primary():
    global primary_spectrum, primary_file
    if primary_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{primary_file} +")
        app.Listbox1.delete(index)
        app.Listbox1.insert(index, primary_file)
        
        primary_spectrum = None
        primary_file = None
    else:
        messagebox.showerror("Error", "No primary spectrum is currently set.")

def subtract():
    global primary_spectrum, primary_file, background_spectrum, background_file, displayed_data, isSinglePlot, app

    app.TScale1.set(0)
    app.TScale2.set(1)
    app.TScale3.set(0.5)
    
    if primary_spectrum is None or background_spectrum is None:
        messagebox.showerror("Error", "Both primary and background spectra must be set for subtraction.")
        return

    primary_name = primary_file if primary_file[-2:] != " +" else primary_file[:-2]
    background_name = background_file if background_file[-2:] != " -" else background_file[:-2]

    if primary_name == background_name:
        messagebox.showerror("Error", "Primary and background spectra cannot be the same.")
        return

    fig, ax = plt.subplots()
    try:
        subtracted_data = primary_spectrum.copy()
        subtracted_data["Epsilon"] -= background_spectrum["Epsilon"]

        displayed_data = subtracted_data  # Store the subtracted data for zooming
        isSinglePlot = True
        
        # print(displayed_data)
        
        ax.plot(subtracted_data["Wavenumber (cm-1)"], subtracted_data["Epsilon"], label=f"{primary_name} - {background_name}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to subtract spectra: {e}")
        return

    ax.set_xlabel("Wavenumber (cm-1)")
    ax.set_ylabel("Epsilon")
    ax.set_title("Subtracted Spectrum")
    ax.legend()

    # Clear the previous plot
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    plt.close(fig)

def get_spectra():
    global spectra_data, file_paths, displayed_data
    file_paths = filedialog.askopenfilenames(filetypes=[#("Text files", "*.txt"),
                                                        ("CSV files", "*.csv")])  # Allow multiple file selections
    if file_paths:
        spectra_data = {}  # Reset spectra_data dictionary
        for file_path in file_paths:  # Iterate through each selected file
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                # Find the line starting with "Version"
                start_index = None
                for i, line in enumerate(lines):
                    if line.startswith("Version"):
                        start_index = i + 1
                        break
                
                if start_index is None:
                    messagebox.showerror("Error", f"No table found in '{os.path.basename(file_path)}'")
                    continue
                
                # Extract the table data
                table_data = []
                for line in lines[start_index:]:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 2:
                            table_data.append(parts)
                
                if not table_data: 
                    messagebox.showerror("Error", f"No valid table data found in '{os.path.basename(file_path)}'")
                    continue
                
                # Convert to DataFrame
                data = pd.DataFrame(table_data, columns=["Wavenumber (cm-1)", "Epsilon"])
                data["Wavenumber (cm-1)"] = pd.to_numeric(data["Wavenumber (cm-1)"])
                data["Epsilon"] = pd.to_numeric(data["Epsilon"])
                
                spectra_data[os.path.basename(file_path)] = data  # Store the DataFrame using the file name as the key
                app.Listbox1.insert(tk.END, os.path.basename(file_path))  # Add file name to listbox
                # displayed_data = spectra_data

                # Enable the sliders after loading the spectra data
                app.TScale1.configure(state=tk.NORMAL)
                app.TScale1.set(0)
                app.TScale2.configure(state=tk.NORMAL)
                app.TScale2.set(1)
                app.TScale3.configure(state = tk.NORMAL)
                app.TScale3.set(0.5)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file '{os.path.basename(file_path)}': {e}")
        # messagebox.showinfo("Success", "Files loaded successfully")
    else:
        spectra_data = {}  # Reset spectra_data if no files are selected

# def plot():
#     global spectra_data, file_paths, displayed_data
#     selected_indices = app.Listbox1.curselection()  # Get selected indices
#     if selected_indices:
#         left_limit = app.TScale1.get()
#         right_limit = app.TScale2.get()

#         if left_limit >= right_limit:
#             messagebox.showerror("Error", "The second slider must be to the right of the first slider")
#             return  # Stop updating the plot if the second slider is not to the right of the first slider
        
#         fig, ax = plt.subplots()
        
#         for index in selected_indices:
#             file_name = app.Listbox1.get(index)
            
#             if file_name in spectra_data: 
#                 data = spectra_data[file_name]
#                 displayed_data = data
#                 ax.plot(data["Wavenumber (cm-1)"], data["Epsilon"], label=file_name)
#             else:
#                 messagebox.showerror("Error", f"No data found for '{file_name}'")

#         ax.set_xlabel("Wavenumber (cm-1)")
#         ax.set_ylabel("Epsilon")
#         ax.set_title("FTIR Spectra")
#         ax.legend()

#         # Clear the previous plot
#         for widget in app.Canvas1.winfo_children():
#             widget.destroy()

#         canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
#         canvas.draw()
#         canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#         # Close the figure to free up memory
#         plt.close(fig)
#     else:
#         messagebox.showerror("Error", "No spectra data selected to plot. Please highlight items in the listbox.")

def plot():
    global spectra_data, displayed_data, isSinglePlot, app

    app.TScale1.set(0)
    app.TScale2.set(1)
    app.TScale3.set(0.5)


    # print("> plot() - called")

    if not spectra_data: 
        messagebox.showerror("Error", "No spectra data loaded to plot.")
        return

    displayed_data = spectra_data  # Store all spectra data for zooming
    
    left_limit = app.TScale1.get()
    right_limit = app.TScale2.get()

    if left_limit >= right_limit:
        messagebox.showerror("Error", "The second slider must be to the right of the first slider")
        return  # Stop updating the plot if the second slider is not to the right of the first slider

    fig, ax = plt.subplots()

    for file_name in app.Listbox1.get(0, tk.END):
        if file_name in spectra_data: 
            data = spectra_data[file_name]
            # displayed_data = data
            ax.plot(data["Wavenumber (cm-1)"], data["Epsilon"], label=file_name)
        else:
            messagebox.showerror("Error", f"No data found for '{file_name}'")

    ax.set_xlabel("Wavenumber (cm-1)")
    ax.set_ylabel("Epsilon")
    ax.set_title("FTIR Spectra")
    ax.legend()

    # Clear the previous plot
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    isSinglePlot = False

    # Close the figure to free up memory
    plt.close(fig)

    # print("> plot(): isSinglePlot = ", isSinglePlot)
    

def on_listbox_double_click(event):
    global app, displayed_data, isSinglePlot, singleFileName

    app.TScale1.set(0)
    app.TScale2.set(1)
    app.TScale3.set(0.5)
    
    
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        file_name = event.widget.get(index)
        
        if file_name in spectra_data:  
            data = spectra_data[file_name]
            
            # Clear previous data in Treeview
            for item in app.tree.get_children():
                app.tree.delete(item)

            # Insert new data into Treeview
            for _, row in data.iterrows():
                app.tree.insert("", "end", values=(row["Wavenumber (cm-1)"], row["Epsilon"]))
            
            # Plot the data
            fig, ax = plt.subplots()
            ax.plot(data["Wavenumber (cm-1)"], data["Epsilon"], label=file_name)
            ax.set_xlabel("Wavenumber (cm-1)")
            ax.set_ylabel("Epsilon")
            ax.set_title("FTIR Spectra")
            ax.legend()

            # Clear the previous plot
            for widget in app.Canvas1.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # Close the figure to free up memory
            plt.close(fig)

            # Update the displayed data
            isSinglePlot = True
            displayed_data = data
            singleFileName = file_name
            # print("> on_listbox_double_click(): \n", displayed_data)
        else:
            messagebox.showerror("Error", f"No data found for '{file_name}'")


            
def clear_plot():
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    # Clear the selection in Listbox1
    app.Listbox1.selection_clear(0, tk.END)

def update_plot_range(event=None):
    global displayed_data, isSinglePlot

    # print("> update_plot_range(): isSinglePlot: ", isSinglePlot)
    
    if displayed_data is not None:
        left_limit = app.TScale1.get()
        right_limit = app.TScale2.get()

        if left_limit >= right_limit:
            return  # Stop updating the plot if the second slider is not to the right of the first slider

        fig, ax = plt.subplots()

        if not isSinglePlot: 
            # Iterate over all spectra data to plot each one
            for file_name, data in spectra_data.items():
                min_wavenumber = data["Wavenumber (cm-1)"].min()
                max_wavenumber = data["Wavenumber (cm-1)"].max()
                lower_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * left_limit
                upper_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * right_limit
                filtered_data = data[(data["Wavenumber (cm-1)"] >= lower_bound) & (data["Wavenumber (cm-1)"] <= upper_bound)]
            
                ax.plot(filtered_data["Wavenumber (cm-1)"], filtered_data["Epsilon"], label=file_name)
        else:
            # Filter data based on slider values
            min_wavenumber = displayed_data["Wavenumber (cm-1)"].min()
            max_wavenumber = displayed_data["Wavenumber (cm-1)"].max()
            lower_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * left_limit
            upper_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * right_limit
            filtered_data = displayed_data[(displayed_data["Wavenumber (cm-1)"] >= lower_bound) & (displayed_data["Wavenumber (cm-1)"] <= upper_bound)]
            ax.plot(filtered_data["Wavenumber (cm-1)"], filtered_data["Epsilon"]) #, label=singleFileName)
            
            
        ax.set_xlabel("Wavenumber (cm-1)")
        ax.set_ylabel("Epsilon")
        ax.set_title("Zoomed Spectra")
        ax.legend()

        # Clear the previous plot
        for widget in app.Canvas1.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.close(fig)
    else:
        print("> Cannot find displayed data!")
    
# def update_plot_range(event=None):
#     global displayed_data
#     if displayed_data is not None:
#         left_limit = app.TScale1.get()
#         right_limit = app.TScale2.get()

#         if left_limit >= right_limit:
#             return  # Stop updating the plot if the second slider is not to the right of the first slider

#         fig, ax = plt.subplots()
        
#         # Filter data based on slider values
#         min_wavenumber = displayed_data["Wavenumber (cm-1)"].min()
#         max_wavenumber = displayed_data["Wavenumber (cm-1)"].max()
#         lower_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * left_limit
#         upper_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * right_limit
#         filtered_data = displayed_data[(displayed_data["Wavenumber (cm-1)"] >= lower_bound) & (displayed_data["Wavenumber (cm-1)"] <= upper_bound)]
        
#         ax.plot(filtered_data["Wavenumber (cm-1)"], filtered_data["Epsilon"], label="Displayed Data")
#         ax.set_xlabel("Wavenumber (cm-1)")
#         ax.set_ylabel("Epsilon")
#         ax.set_title("Zoomed Spectrum")
#         ax.legend()

#         # Clear the previous plot
#         for widget in app.Canvas1.winfo_children():
#             widget.destroy()

#         canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
#         canvas.draw()
#         canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#         plt.close(fig)
#     else:
#         print("> cannot find displayed data!")
    
def remove_selected():
    global spectra_data
    # Get selected items to remove
    selected_indices = app.Listbox1.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "No items selected to remove.")
        return

    # Remove items from the end to avoid reindexing issues
    for index in reversed(selected_indices):
        file_name = app.Listbox1.get(index)
        app.Listbox1.delete(index)
        if file_name in spectra_data: 
            del spectra_data[file_name]  # Remove the corresponding data

def cancel_subtraction():
    global primary_spectrum, primary_file, background_spectrum, background_file
    
    # Clear primary selection
    if primary_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{primary_file} +")
        app.Listbox1.delete(index)
        app.Listbox1.insert(index, primary_file)
        primary_spectrum = None
        primary_file = None

    # Clear background selection
    if background_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{background_file} -")
        app.Listbox1.delete(index)
        app.Listbox1.insert(index, background_file)
        background_spectrum = None
        background_file = None

    # Clear displayed data
    displayed_data = None
        
    # Clear the plot
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    messagebox.showinfo("Success", "Cancelled all background subtractions.")


def subtract_background_from_all():
    global spectra_data, background_spectrum, background_file

    if background_spectrum is None:
        messagebox.showerror("Error", "No background spectrum designated.")
        return

    net_spectra_data = {}

    for file_name in app.Listbox1.get(0, tk.END):
        if file_name != background_file:
            if file_name in spectra_data: 
                data = spectra_data[file_name]
                try:
                    net_data = data.copy()
                    net_data["Epsilon"] -= background_spectrum["Epsilon"]
                    net_file_name = f"Net_{file_name}"
                    net_spectra_data[net_file_name] = net_data

                    # Insert the new net spectrum into the Listbox
                    app.Listbox1.insert(tk.END, net_file_name)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to subtract background from '{file_name}': {e}")
            # else:
            #     messagebox.showerror("Error", f"No data found for '{file_name}'")

    # Update the spectra_data with the net spectra data
    spectra_data.update(net_spectra_data)
    messagebox.showinfo("Success", "Background subtraction completed for all spectra.")
    

def main():
    global root, app
    root = tk.Tk()
    app = Toplevel1(root)
    root.mainloop()
