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
                data = pd.DataFrame(table_data, columns=["Wavenumber (cm-1)", "Epsilon"])
                data["Wavenumber (cm-1)"] = pd.to_numeric(data["Wavenumber (cm-1)"])
                data["Epsilon"] = pd.to_numeric(data["Epsilon"])

                # Store the DataFrame using the file name as the key
                spectra_data[os.path.basename(file_path)] = data  
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


def on_listbox_double_click(event):
    global app, displayed_data, isSinglePlot, singleFileName, fig, ax

    displayed_data = {}

    # app.TScale1.set(0)
    # app.TScale2.set(1)
    
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
            # fig, ax = plt.subplots()
            # Reuse the figure and axes
            if fig is None or ax is None:
                fig, ax = plt.subplots()
            else:
                ax.clear()
            
            ax.scatter(data["Wavenumber (cm-1)"],
                       data["Epsilon"],
                       label=file_name,
                       s = 2)
            ax.set_xlabel("Wavenumber (cm-1)")
            ax.set_ylabel("Epsilon")
            ax.set_title("FTIR Spectra")
            ax.legend()
            ax.invert_xaxis()

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

    app.TScale1.set(0)
    app.TScale2.set(1)
    app.TScale3.set(0.5)
    
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
        subtracted_data["Epsilon"] -= background_spectrum["Epsilon"]

        displayed_data = subtracted_data  # Store the subtracted data for zooming
        isSinglePlot = True
        
        ax.scatter(subtracted_data["Wavenumber (cm-1)"],
                   subtracted_data["Epsilon"],
                   label=f"{primary_name} - {background_name}",
                   s = 2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to subtract spectra: {e}")
        return

    ax.set_xlabel("Wavenumber (cm-1)")
    ax.set_ylabel("Epsilon")
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
    # messagebox.showinfo("Success", "Background subtraction completed for all spectra.")

    

def plot():
    global spectra_data, displayed_data, isSinglePlot, app, fig, ax

    remove_anchors()
    
    # reset the positions of the sliding bars
    app.TScale1.set(0)
    app.TScale2.set(1)
    app.TScale3.set(0.5)

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
            ax.scatter(data["Wavenumber (cm-1)"],
                       data["Epsilon"],
                       label=file_name,
                       s = 2)
        else:
            messagebox.showerror("Error", f"No data found for '{file_name}'")

    ax.set_xlabel("Wavenumber (cm-1)")
    ax.set_ylabel("Epsilon")
    ax.set_title("FTIR Spectra")
    ax.legend()
    ax.invert_xaxis()

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
    



            
def clear_plot():
    for widget in app.Canvas1.winfo_children():
        widget.destroy()

    # Clear the selection in Listbox1
    app.Listbox1.selection_clear(0, tk.END)

def update_plot_range(event=None):
    global displayed_data, isSinglePlot, current_anchor, fig, ax
    
    if displayed_data is not None:
        left_limit = app.TScale1.get()
        right_limit = app.TScale2.get()
        anchor_position = app.TScale3.get()

        if left_limit >= right_limit:
            return  # Stop updating the plot if the second slider is not to the right of the first slider

        # Determine the data range
        if not isSinglePlot:
            min_wavenumber = min(data["Wavenumber (cm-1)"].min() for data in spectra_data.values())
            max_wavenumber = max(data["Wavenumber (cm-1)"].max() for data in spectra_data.values())
        else:
            min_wavenumber = displayed_data["Wavenumber (cm-1)"].min()
            max_wavenumber = displayed_data["Wavenumber (cm-1)"].max()

        # Update TScale3 range
        app.TScale3.configure(from_=min_wavenumber, to=max_wavenumber)
        anchor_position = app.TScale3.get()
        
        # Reuse the figure and axes
        if fig is None or ax is None:
            fig, ax = plt.subplots()
        else:
            ax.clear()
        # fig, ax = plt.subplots()

        if not isSinglePlot: 
            for file_name, data in spectra_data.items():
                min_wavenumber = data["Wavenumber (cm-1)"].min()
                max_wavenumber = data["Wavenumber (cm-1)"].max()
                lower_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * left_limit
                upper_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * right_limit
                filtered_data = data[(data["Wavenumber (cm-1)"] >= lower_bound) & (data["Wavenumber (cm-1)"] <= upper_bound)]
                ax.scatter(filtered_data["Wavenumber (cm-1)"],
                           filtered_data["Epsilon"],
                           label=file_name,
                           s = 2)
        else:
            min_wavenumber = displayed_data["Wavenumber (cm-1)"].min()
            max_wavenumber = displayed_data["Wavenumber (cm-1)"].max()
            lower_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * left_limit
            upper_bound = min_wavenumber + (max_wavenumber - min_wavenumber) * right_limit
            filtered_data = displayed_data[(displayed_data["Wavenumber (cm-1)"] >= lower_bound) & (displayed_data["Wavenumber (cm-1)"] <= upper_bound)]
            ax.scatter(filtered_data["Wavenumber (cm-1)"],
                       filtered_data["Epsilon"],
                       label = app.Listbox1.get(app.Listbox1.curselection()[0]),
                       s = 2)

        # # Draw the current anchor line
        # if current_anchor is not None:
        #     ax.axvline(x=current_anchor, color='red', linestyle='--')
        # Draw all anchor lines
        for anchor in anchors:
            ax.axvline(x=anchor, color='red', linestyle='--')

        # Draw the temporary anchor line
        if len(anchors) > 0: 
            ax.axvline(x=anchor_position, color='blue', linestyle='--')

       # Draw the linear background if there are two anchors
        if len(anchors) == 2:
            anchor1, anchor2 = sorted(anchors)
            data = displayed_data[(displayed_data["Wavenumber (cm-1)"] >= anchor1) & (displayed_data["Wavenumber (cm-1)"] <= anchor2)]
            if not data.empty:
                x1, y1 = data.iloc[0]
                x2, y2 = data.iloc[-1]
                ax.plot([x1, x2], [y1, y2], color='green', linestyle='--', label='Linear Background')     

        ax.set_xlabel("Wavenumber (cm-1)")
        ax.set_ylabel("Epsilon")
        ax.set_title("Zoomed Spectra")
        ax.legend()
        ax.invert_xaxis()

        for widget in app.Canvas1.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=app.Canvas1)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        plt.close(fig)
    else:
        print("> Cannot find displayed data!")    
    
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
        # Get the selected item from the Listbox
        selected_index = app.Listbox1.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected to save.")
            return
        
        file_name = app.Listbox1.get(selected_index[0])
        
        # Get the corresponding DataFrame from spectra_data
        if file_name not in spectra_data: 
            messagebox.showerror("Error", f"No data found for '{file_name}'")
            return
        
        data = spectra_data[file_name]
        
        # # Ask the user for a save location
        # save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        # if save_path:
        #     # Save the DataFrame to a CSV file
        #     data.to_csv(save_path, index=False)
        #     messagebox.showinfo("Success", f"Data saved successfully to '{save_path}'")

        # Generate the save path with "Export_" prepended to the file name
        save_path = os.path.join(os.getcwd(), f"Exported_{file_name}")
        
        # Save the DataFrame to a CSV file
        data.to_csv(save_path, index=False)
        messagebox.showinfo("Success", f"Data saved successfully to '{save_path}'")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save  {e}")

def add_anchor():
    global anchors
    new_anchor = app.TScale3.get()
    
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
    data = displayed_data[(displayed_data["Wavenumber (cm-1)"] >= anchor1) & (displayed_data["Wavenumber (cm-1)"] <= anchor2)]

    if data.empty:
        messagebox.showerror("Error", "No data points found between the anchors.")
        return

    x1, y1 = data.iloc[0]
    x2, y2 = data.iloc[-1]

    # Calculate the linear background
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    data["Background"] = slope * data["Wavenumber (cm-1)"] + intercept

    # Calculate the area under the curve relative to the linear background
    data["Corrected Epsilon"] = data["Epsilon"] - data["Background"]
    area = np.trapz(data["Corrected Epsilon"], data["Wavenumber (cm-1)"])

    # result_text = f"Integrated area: {area}"
    result_text = f"{area}"
    
    # Display the result in Text1
    app.Text1.delete("1.0", tk.END)  # Clear the text box
    app.Text1.insert(tk.END, result_text)

    # Copy the result to the clipboard
    app.top.clipboard_clear()
    app.top.clipboard_append(result_text)
    app.top.update()  # Now it stays on the clipboard after the window is closed
    
    # messagebox.showinfo("Integration Result", f"Integrated area: {area}")

    update_plot_range()





    

def main():
    global root, app
    root = tk.Tk()
    app = Toplevel1(root)
    root.mainloop()
