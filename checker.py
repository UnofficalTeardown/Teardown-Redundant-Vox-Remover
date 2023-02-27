import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import tkinter.font as TkFont

def find_redundant_vox_files(xml_filepath, mod_folderpath):
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    

    xml_vox_files = set()
    for elem in root.iter():
        for k, v in elem.attrib.items():
            if k == "brush" or k == "file":
                if v.startswith("MOD/"):
                    filename = v.split("/")[-1]
                    if filename.endswith(".vox"):
                        xml_vox_files.add(filename)


    redundant_files = []
    for dirpath, dirnames, filenames in os.walk(mod_folderpath):
        for filename in filenames:
            if filename.endswith(".vox"):
                if filename not in xml_vox_files:
                    redundant_files.append(os.path.join(dirpath, filename))

    return redundant_files

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        

        self.xml_label = tk.Label(master, text="XML File:")
        self.xml_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.xml_entry = tk.Entry(master, width=50)
        self.xml_entry.grid(row=0, column=1, padx=10, pady=10)

        self.xml_button = tk.Button(master, text="Browse", command=self.get_xml_file)
        self.xml_button.grid(row=0, column=2, padx=10, pady=10)

        self.mod_label = tk.Label(master, text="Mod Folder:")
        self.mod_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.mod_entry = tk.Entry(master, width=50)
        self.mod_entry.grid(row=1, column=1, padx=10, pady=10)

        self.mod_button = tk.Button(master, text="Browse", command=self.get_mod_folder)
        self.mod_button.grid(row=1, column=2, padx=10, pady=10)

        self.find_button = tk.Button(master, text="Find Redundant Files", command=self.find_redundant_files)
        self.find_button.grid(row=2, column=1, padx=10, pady=10)


        self.find_button = tk.Button(master, text="Remove All Redundant Files", command=self.remove_redundant_files, fg="red")
        self.find_button.grid(row=2, column=0, padx=10, pady=10)

        self.find_button = tk.Button(master, text="Clear List", command=self.clear_all, fg="#ff9933")
        self.find_button.grid(row=2, column=2, padx=10, pady=10)


        self.aboutText = tk.Label(master, text="Created By Eli\nelir#0001\n\nDeleted Files are moved\n to 'TD_Redundant'.")
        self.aboutText.grid(row=7, column=0, padx=10, pady=10)

        self.aboutText = tk.Text(master,height=10,width=45)
        self.aboutText.grid(row=7, column=1, padx=10, pady=10)
        self.aboutText.insert(tk.END,"No Software Warranty. User acknowledges and\nagrees that the use of the Software is at\nUser’s sole risk. The Software and related\ndocumentation are provided “AS IS” and\nwithout any warranty of any kind and Author\nEXPRESSLY DISCLAIMS ALL WARRANTIES, EXPRESS\nOR IMPLIED, INCLUDING, BUT NOT LIMITED TO,\nTHE IMPLIED WARRANTIES OF MERCHANTABILITY AND\nFITNESS FOR A PARTICULAR PURPOSE.")
        self.aboutText.config(state=tk.DISABLED)
        #self.wText = tk.Label( root, text="No Software Warranty. User acknowledges and agrees that the use of the Software is at User’s sole risk. The Software and related documentation are provided “AS IS” and without any warranty of any kind and Author EXPRESSLY DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.")
        #self.wText.grid(row=8, column=0, padx=10, pady=10)
        


        self.listframe = tk.Frame(master)
        self.listframe.grid(row=3, rowspan=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.listframe.grid_propagate(False)


        self.canvas = tk.Canvas(self.listframe,width=600,height=400)
        self.canvas.pack(side="left", fill="both", expand=True)


        self.scrollbar = tk.Scrollbar(self.listframe, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")


        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        self.listbox_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.listbox_frame, anchor="nw")


        self.listbox = tk.Listbox(self.listbox_frame, width=100, height=800)
        self.listbox.pack(side="left", fill="both", expand=True)


        self.listbox.bind("<Configure>", lambda e: self.canvas.itemconfig(self.listbox_frame, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-1 * (event.delta // 120), "units"))



    def get_xml_file(self):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select XML File",
                                              filetypes=(("XML Files", "*.xml"), ("All Files", "*.*")))
        self.xml_entry.delete(0, tk.END)
        self.xml_entry.insert(0, filepath)

    def get_mod_folder(self):
        folderpath = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Mod Folder")
        self.mod_entry.delete(0, tk.END)
        self.mod_entry.insert(0, folderpath)

    redundant_files = []

    def find_redundant_files(self):
        # Get the file paths
        xml_filepath = self.xml_entry.get()
        mod_folderpath = self.mod_entry.get()

        if xml_filepath == "" or mod_folderpath == "":
            tk.messagebox.showerror(title="TD Redundant Checker Error", message="Error 02: XML Filepath or Mod Folderpath was left empty")
        else:

            # Find the redundant files
            self.redundant_files = find_redundant_vox_files(xml_filepath, mod_folderpath)

            # Update the listbox
            self.listbox.delete(0, tk.END)
            for filepath in self.redundant_files:
                item = tk.Frame(self.listbox)
                item.pack(side="top", fill="both")
                item.filename = filepath
                textPrefix = "MOD"
                textLocalPath = filepath.replace(self.mod_entry.get(), "")
                textLocalPathLocal = textLocalPath.replace(os.path.basename(filepath), "")
                textLocalPathItemName = os.path.basename(filepath)
                filename_label = tk.Text(item,width=50,height=2)
                filename_label.pack(side="left", padx=15, pady=2)

                default_font = TkFont.nametofont("TkDefaultFont") 
                bold_font = TkFont.Font(**default_font.configure())
                bold_font.configure(weight="bold")
                filename_label.tag_configure("bold", font=bold_font)
                
            


                filename_label.insert(tk.END,textPrefix)
                filename_label.insert(tk.END,textLocalPathLocal.replace("\\","/"))
                filename_label.insert(tk.END,textLocalPathItemName.replace("\\","/"),"bold")


                filename_label.config(state=tk.DISABLED)
                filename_label.bind("<1>", lambda event: filename_label.focus_set())
                

                tpfl = "1." + str(len(textPrefix))
                lpl = "1." + str(len(textPrefix) + len(textLocalPathLocal))
                lpl2 = "1." + str(len(textPrefix) + len(textLocalPathLocal))
                lpln = "1." + str(len(textPrefix) + len(textLocalPathLocal) + len(textLocalPathItemName))


                filename_label.tag_add("start", "1.0", tpfl)
                filename_label.tag_config("start", background="#ff9933",foreground="black")

                filename_label.tag_add("second", tpfl, lpl)
                filename_label.tag_config("second", background="#99ccff",foreground="black")

                filename_label.tag_add("third", lpl2, lpln)
                filename_label.tag_config("third", background="#00cc66",foreground="black")




                show_button = tk.Button(item, text="Show", command=lambda x=filepath: self.show_file(x))
                show_button.pack(side="left", padx=15, pady=2)
                delete_button = tk.Button(item, text="Delete", fg="red", command=lambda x=filepath, item=item: self.delete_file(x,item))
                delete_button.pack(side="left", padx=15, pady=2)

    def remove_redundant_files(self):

        for filepath in self.redundant_files:
            isExist = os.path.exists(self.mod_entry.get() + "/TD_REDUNDANT/")
            if not isExist:
                os.makedirs(self.mod_entry.get() + "/TD_REDUNDANT/")
            os.rename(filepath, self.mod_entry.get() + "/TD_REDUNDANT/" + os.path.basename(filepath))
        tk.messagebox.showinfo(title="Delete All", message="All redundant files have been deleted!")
        self.listbox.destroy()
        self.listbox = tk.Listbox(self.listbox_frame, width=100, height=800)
        self.listbox.pack(side="left", fill="both", expand=True)


       

    def show_file(self, filepath):
        os.startfile(filepath)

    def delete_file(self, filepath, item):
        isExist = os.path.exists(self.mod_entry.get() + "/TD_REDUNDANT/")
        if not isExist:
            os.makedirs(self.mod_entry.get() + "/TD_REDUNDANT/")
        os.rename(filepath, self.mod_entry.get() + "/TD_REDUNDANT/" + os.path.basename(filepath))
        item.destroy()
        self.list_items.remove(item)

    def clear_all(self):
        self.redundant_files = []
        self.xml_entry.delete(0, tk.END)
        self.mod_entry.delete(0, tk.END)
        self.listbox.destroy()
        self.listbox = tk.Listbox(self.listbox_frame, width=100, height=800)
        self.listbox.pack(side="left", fill="both", expand=True)
        


root = tk.Tk()
root.wm_title('TD Redundant Checker')
root.geometry("635x750")
root.resizable(False,False)
app = Application(master=root)

app.mainloop()
