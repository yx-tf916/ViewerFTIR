import os
import numpy as np

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
import matplotlib.ticker as ticker

_debug = True  # False to eliminate debug printing from callback functions.

# viewer_support.py

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from viewer import Toplevel1

# Global variable to store the loaded spectra data
spectra_data = {} # dictionary
app = None
file_paths = []

background_spectrum = None
background_file = None
primary_spectrum = None
primary_file = None

# this is the data to display in the canvas, it could be a single spectrum
# or a collection of spectra
displayed_data = None 

isSinglePlot = False
singleFilename = None

current_anchor = None
anchors = []

# Add global variables for figure and axes
fig = None
ax = None

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
                
                # Extract the table data for this file
                table_data = []
                for line in lines[start_index:]:
                    line = line.strip()
                    if line:
                        parts = line.split(',') # define the delimiter here
                        if len(parts) == 2: # note that this is a two-column table
                            table_data.append(parts)
                
                if not table_data: 
                    messagebox.showerror("Error", f"No valid table data found in '{os.path.basename(file_path)}'")
                    continue
                
                # Convert to DataFrame
                data = pd.DataFrame(table_data, columns=["Wavenumber", "Absorbance"])
                data["Wavenumber"] = pd.to_numeric(data["Wavenumber"])
                data["Absorbance"] = pd.to_numeric(data["Absorbance"])

                # Store the DataFrame using the file name as the key
                spectra_data[os.path.basename(file_path)] = data  
                app.Listbox1.insert(tk.END, os.path.basename(file_path))  # Add file name to listbox
                # displayed_data = spectra_data

                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file '{os.path.basename(file_path)}': {e}")
        # messagebox.showinfo("Success", "Files loaded successfully")
    else:
        spectra_data = {}  # Reset spectra_data if no files are selected


def on_listbox_double_click(event):
    global app, displayed_data, isSinglePlot, singleFileName, fig, ax

    displayed_data = {}

    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        file_name = event.widget.get(index)
        
        if file_name in spectra_data:   
            data = spectra_data[file_name]

            # Update the displayed data
            isSinglePlot = True
            displayed_data = {file_name: data}
            singleFileName = file_name
            
            # Clear previous data in Treeview
            for item in app.tree.get_children():
                app.tree.delete(item)

            # Insert new data into Treeview
            for _, row in data.iterrows():
                app.tree.insert("", "end", values=(row["Wavenumber"], row["Absorbance"]))

            update_plot_range()
        else:
            messagebox.showerror("Error", f"No data found for '{file_name}'")        

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

        app.Listbox1.itemconfig(index, {'fg': "red"})
        # app.Listbox1.delete(index)
        # app.Listbox1.insert(index, f"{file_name} -")
    else:
        messagebox.showerror("Error", f"No data found for '{file_name}'")

def unset_as_background():
    global background_spectrum, background_file
    if background_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{background_file}")
        app.Listbox1.itemconfig(index, {"fg": "black"})
        # app.Listbox1.delete(index)
        # app.Listbox1.insert(index, background_file)
        
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

        app.Listbox1.itemconfig(index, {"fg": "blue"})
        # app.Listbox1.delete(index)
        # app.Listbox1.insert(index, f"{file_name} +")
    else:
        messagebox.showerror("Error", f"No data found for '{file_name}'")

def unset_as_primary():
    global primary_spectrum, primary_file
    if primary_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{primary_file}")
        app.Listbox1.itemconfig(index, {"fg": "black"})
        # app.Listbox1.delete(index)
        # app.Listbox1.insert(index, primary_file)
        
        primary_spectrum = None
        primary_file = None
    else:
        messagebox.showerror("Error", "No primary spectrum is currently set.")

def subtract():
    global primary_spectrum, primary_file, background_spectrum, background_file, displayed_data, isSinglePlot, app, fig, ax

    # app.TScale1.set(0)
    # app.TScale2.set(6000)
    # app.TScale3.set(0.5)
    
    if primary_spectrum is None or background_spectrum is None:
        messagebox.showerror("Error", "Both primary and background spectra must be set for subtraction.")
        return

    primary_name = primary_file #if primary_file[-2:] != " +" else primary_file[:-2]
    background_name = background_file #if background_file[-2:] != " -" else background_file[:-2]

    if primary_name == background_name:
        messagebox.showerror("Error", "Primary and background spectra cannot be the same.")
        return

    fig, ax = plt.subplots()
    try:
        subtracted_data = primary_spectrum.copy()
        subtracted_data["Absorbance"] -= background_spectrum["Absorbance"]

        displayed_data = subtracted_data  # Store the subtracted data for zooming
        isSinglePlot = True
        
        ax.scatter(subtracted_data["Wavenumber"],
                   subtracted_data["Absorbance"],
                   label=f"{primary_name} - {background_name}",
                   s = 2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to subtract spectra: {e}")
        return

    ax.set_xlabel("Wavenumber")
    ax.set_ylabel("Absorbance")
    ax.set_title("Subtracted Spectrum")
    ax.legend()
    # Reverse the x-axis
    ax.invert_xaxis()

    # Clear the previous plot
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    plt.close(fig)


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
                    net_data["Absorbance"] -= background_spectrum["Absorbance"]
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
    # messagebox.showinfo("Success", "Background subtraction completed for all spectra.")

    

def plot():
    global spectra_data, displayed_data, isSinglePlot, app, fig, ax

    remove_anchors()
    displayed_data = {}
    
    if not spectra_data:
        messagebox.showerror("Error", "No spectra data loaded to plot.")
        return

    # Get selected items from the Listbox
    selected_indices = app.Listbox1.curselection()
    selected_files = [app.Listbox1.get(i) for i in selected_indices]
    if not selected_files:
        messagebox.showerror("Error", "No items selected in the listbox.")
        return

    # Always use a dictionary for displayed_data
    displayed_data = {file: spectra_data[file] for file in selected_files if file in spectra_data}
    # Check if displayed_data has valid structure
    if not all("Wavenumber" in data.columns and "Absorbance" in data.columns for data in displayed_data.values()):
        messagebox.showerror("Error", "Invalid data structure in selected files.")
        return
    print(selected_indices)
    
    left_limit = float(app.TScale1.get())
    right_limit = float(app.TScale2.get())
    print(left_limit)
    print(right_limit)

    if left_limit >= right_limit:
        messagebox.showerror("Error", "The second slider must be to the right of the first slider")
        return  # Stop updating the plot if the second slider is not to the right of the first slider

    update_plot_range()    

    canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    isSinglePlot = False

    # Close the figure to free up memory
    plt.close(fig)

    # print("> plot(): isSinglePlot = ", isSinglePlot)
    



            
def clear_plot():
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    # Clear the selection in Listbox1
    app.Listbox1.selection_clear(0, tk.END)

def set_zoom_lower_limit(event = None):
    try:
        # Get the value from the Entry1 widget
        new_limit = float(app.Entry1.get())

        if app.TScale1.configure("from")[4] <= new_limit < app.TScale2.get(): 
            app.TScale1.set(new_limit)
            app.TScale3.configure(from_ = new_limit)
            update_plot_range()
        else:
            raise ValueError("Limit out of range")
    except ValueError as e:
        messagebox.showerror("Invalid Input", "Please enter a valid number between 0 and 6000.")

def set_zoom_upper_limit(event = None):
    try:
        # Get the value from the Entry1_1 widget
        new_limit = float(app.Entry1_1.get())

        if app.TScale1.get() <= new_limit < app.TScale2.configure("to")[4]: 
            app.TScale2.set(new_limit)
            app.TScale3.configure(to = new_limit)
            update_plot_range()
        else:
            raise ValueError("Limit out of range")
    except ValueError as e:
        messagebox.showerror("Invalid Input", "Please enter a valid number between 0 and 6000.")

def set_left_anchor(event = None):
    try:
        # Get the value from the Entry1_1 widget
        anchor_pos = float(app.Entry1_2.get())

        if app.TScale1.get() <= anchor_pos < app.TScale2.get(): 
            # app.TScale3.set(anchor_pos)
            # app.TScale3.configure(to = anchor_pos)
            add_anchor(anchor_pos)
            update_plot_range()
        else:
            raise ValueError("Limit out of range")
    except ValueError as e:
        messagebox.showerror("Invalid Input", "Please enter a valid number within the current zoom range.")

def set_right_anchor(event = None):
    try:
        # Get the value from the Entry1_1 widget
        anchor_pos = float(app.Entry1_2_1.get())

        if app.TScale1.get() <= anchor_pos < app.TScale2.get(): 
            # app.TScale3.set(anchor_pos)
            # app.TScale3.configure(to = anchor_pos)
            add_anchor(anchor_pos)
            update_plot_range()
        else:
            raise ValueError("Limit out of range")
    except ValueError as e:
        messagebox.showerror("Invalid Input", "Please enter a valid number within the current zoom range.")

    
    
def update_plot_range(event=None):
    global displayed_data, isSinglePlot, current_anchor, fig, ax

    if displayed_data: 
        left_limit = app.TScale1.get()
        right_limit = app.TScale2.get()
        # anchor_position = app.TScale3.get()

        if left_limit >= right_limit:
            return  # Stop updating the plot if the second slider is not to the right of the first slider

        # Reuse the figure and axes
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        else:
            ax.clear()

        # Handle displayed_data as a dictionary of DataFrames
        min_wavenumber = min(data["Wavenumber"].min() for data in displayed_data.values())
        max_wavenumber = max(data["Wavenumber"].max() for data in displayed_data.values())

        for file_name, data in displayed_data.items():
            lower_bound = left_limit
            upper_bound = right_limit
            filtered_data = data[(data["Wavenumber"] >= lower_bound) & (data["Wavenumber"] <= upper_bound)]
            ax.scatter(filtered_data["Wavenumber"],
                       filtered_data["Absorbance"],
                       label=file_name,
                       s=2)

        # Draw all anchor lines
        for anchor in anchors:
            ax.axvline(x=anchor, color='red', linestyle='--')

        # # Draw the temporary anchor line
        # if len(anchors) > 0: 
        #     ax.axvline(x=anchor_position, color='blue', linestyle='--')

        # Draw the linear background if there are two anchors
        if len(anchors) == 2:
            anchor1, anchor2 = sorted(anchors)
            filtered_data = pd.concat(displayed_data.values())
            filtered_data = filtered_data[(filtered_data["Wavenumber"] >= anchor1) & (filtered_data["Wavenumber"] <= anchor2)]
            if not filtered_data.empty:
                x1, y1 = filtered_data.iloc[0]
                x2, y2 = filtered_data.iloc[-1]
                ax.plot([x1, x2], [y1, y2], color='green', linestyle='--', label='Linear Background')     

        ax.set_xlabel("Wavenumber")
        ax.set_ylabel("Absorbance")
        ax.set_title("Zoomed Spectra")
        ax.legend()
        ax.invert_xaxis()

        # Set x-axis ticks frequency
        ax.xaxis.set_major_locator(ticker.MultipleLocator(50))
        ax.tick_params(axis='x', labelrotation=45)
        # Adjust layout to prevent clipping
        fig.tight_layout()

        for widget in app.Canvas1.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.close(fig)


        
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
        index = app.Listbox1.get(0, tk.END).index(f"{primary_file}")
        app.Listbox1.itemconfig(index, {'fg': "black"})
        # app.Listbox1.delete(index)
        # app.Listbox1.insert(index, primary_file)
        primary_spectrum = None
        primary_file = None

    # Clear background selection
    if background_spectrum is not None:
        index = app.Listbox1.get(0, tk.END).index(f"{background_file}")
        app.Listbox1.itemconfig(index, {'fg': "black"})
        # app.Listbox1.delete(index)
        # app.Listbox1.insert(index, background_file)
        background_spectrum = None
        background_file = None

    # Clear displayed data
    displayed_data = None
        
    # Clear the plot
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    messagebox.showinfo("Success", "Cancelled all background subtractions.")


def export():
    try:
        # Get the selected items from the Listbox
        selected_indices = app.Listbox1.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "No items selected to save.")
            return
        
        for index in selected_indices:
            file_name = app.Listbox1.get(index)
            
            # Get the corresponding DataFrame from spectra_data
            if file_name not in spectra_data: 
                messagebox.showerror("Error", f"No data found for '{file_name}'")
                return
            
            data = spectra_data[file_name]
            
            # Generate the save path with "Exported_" prepended to the file name
            save_path = os.path.join(os.getcwd(), f"Exported_{file_name}")
            
            # Save the DataFrame to a CSV file
            data.to_csv(save_path, index=False, header = False)
            messagebox.showinfo("Success", f"Data saved successfully to '{save_path}'")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {e}")


        
def add_anchor(pos):
    global anchors
    new_anchor = pos #xapp.TScale3.get()
    
    if len(anchors) < 2:
        anchors.append(new_anchor)
    else:
        # If there are already two anchors, replace the first one with the new one
        anchors = [anchors[1], new_anchor]
    
    update_plot_range()

    
def remove_anchors():
    global current_anchor, anchors
    current_anchor = None
    anchors = []
    update_plot_range()    

def integrate_peak():
    global displayed_data, anchors
    
    if len(anchors) != 2:
        messagebox.showerror("Error", "Please set exactly two anchors for integration.")
        return

    anchor1, anchor2 = sorted(anchors)
    
    # Combine all data from displayed_data within the anchor range
    combined_data = pd.concat(
        data[(data["Wavenumber"] >= anchor1) & (data["Wavenumber"] <= anchor2)]
        for data in displayed_data.values()
    )

    if combined_data.empty:
        messagebox.showerror("Error", "No data points found between the anchors.")
        return

    x1, y1 = combined_data.iloc[0]
    x2, y2 = combined_data.iloc[-1]

    # Calculate the linear background
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    combined_data["Background"] = slope * combined_data["Wavenumber"] + intercept

    # Calculate the area under the curve relative to the linear background
    combined_data["Corrected Absorbance"] = combined_data["Absorbance"] - combined_data["Background"]
    area = np.trapz(combined_data["Corrected Absorbance"], combined_data["Wavenumber"])

    result_text = f"{area}"
    
    # Display the result in Text1
    app.Text1.delete("1.0", tk.END)  # Clear the text box
    app.Text1.insert(tk.END, result_text)

    # Copy the result to the clipboard
    app.top.clipboard_clear()
    app.top.clipboard_append(result_text)
    app.top.update()  # Now it stays on the clipboard after the window is closed
    
    update_plot_range()
    

def main():
    global root, app
    root = tk.Tk()
    app = Toplevel1(root)
    root.mainloop()
