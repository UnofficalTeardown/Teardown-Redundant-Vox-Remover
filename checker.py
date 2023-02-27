import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import tkinter.font as TkFont
import math






def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

instance_vox_files = set()




def find_redundant_vox_files(xml_filepath, mod_folderpath):
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    xml_vox_files = set()

    
    


    for elem in root.iter():
        for k, v in elem.attrib.items():
            if k == "brush" or k == "file" or k == "script":
                if v.startswith("MOD/"):
                    filename = v.split("/")[-1]
                    if filename.endswith(".vox") or filename.endswith(".lua"):
                        xml_vox_files.add(filename)
                    elif v.endswith(".xml"):
                        xml_vox_files.add(filename)
                        

                        instance_xml_path = os.path.join(os.path.dirname(xml_filepath), v.replace("MOD/", ""))
                        if os.path.exists(instance_xml_path):
                            instance_xml = ET.parse(instance_xml_path)
                            instance_root = instance_xml.getroot()
                            for instance_elem in instance_root.iter():
                                for instance_k, instance_v in instance_elem.attrib.items():
                                    if instance_k == "brush" or instance_k == "file" or instance_k == "script":
                                        if instance_v.startswith("MOD/"):
                                            instance_filename = instance_v.split("/")[-1]
                                            if instance_filename.endswith(".vox") or instance_filename.endswith(".lua"):
                                                xml_vox_files.add(instance_filename)
                                                instance_vox_files.add(instance_filename)
                    

    redundant_files = []
    for dirpath, dirnames, filenames in os.walk(mod_folderpath):
        for filename in filenames:
            if filename.endswith(".vox") or filename.endswith(".lua") or filename.endswith(".xml"):
                if filename not in xml_vox_files and filename != "main.xml" and filename != os.path.basename(xml_filepath):
                    redundant_files.append(os.path.join(dirpath, filename))

    return redundant_files

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.WastedSize = 0
        self.masterCount = 0

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

        self.count = tk.Label(master, text="0 Files\nWasted Space 0Mb", anchor="w", width=20)
        self.count.grid(row=3, column=0, padx=0, pady=0)
 
        self.aboutText = tk.Label(master, text="Created By Eli\nelir#0001\n\nDeleted Files are moved\n to 'TD_Redundant'.")
        self.aboutText.grid(row=8, column=0, padx=10, pady=10)

        self.aboutText = tk.Text(master,height=10,width=45)
        self.aboutText.grid(row=8, column=1, padx=10, pady=10)
        self.aboutText.insert(tk.END,"No Software Warranty. User acknowledges and\nagrees that the use of the Software is at\nUser’s sole risk. The Software and related\ndocumentation are provided “AS IS” and\nwithout any warranty of any kind and Author\nEXPRESSLY DISCLAIMS ALL WARRANTIES, EXPRESS\nOR IMPLIED, INCLUDING, BUT NOT LIMITED TO,\nTHE IMPLIED WARRANTIES OF MERCHANTABILITY AND\nFITNESS FOR A PARTICULAR PURPOSE.")
        self.aboutText.config(state=tk.DISABLED)

        


        self.listframe = tk.Frame(master)
        self.listframe.grid(row=4, rowspan=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
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

        xml_filepath = self.xml_entry.get()
        mod_folderpath = self.mod_entry.get()

        if xml_filepath == "" or mod_folderpath == "":
            tk.messagebox.showerror(title="TD Redundant Checker Error", message="Error 02: XML Filepath or Mod Folderpath was left empty")
        else:


            self.redundant_files = find_redundant_vox_files(xml_filepath, mod_folderpath)


            self.listbox.delete(0, tk.END)

            for filepath in self.redundant_files:

                
                self.WastedSize = self.WastedSize + os.path.getsize(filepath)

                self.masterCount = self.masterCount + 1
                self.count.configure(text=str(self.masterCount) + " Files" + "\nWasted Space " + convert_size(self.WastedSize) + "", anchor="w", width=20)

                if filepath in instance_vox_files:
                    frominst = True
                else:
                    frominst = False

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
                filename_label.tag_configure("boldright", font=bold_font, justify='right')
                
            


                filename_label.insert(tk.END,textPrefix)
                filename_label.insert(tk.END,textLocalPathLocal.replace("\\","/"))
                filename_label.insert(tk.END,textLocalPathItemName.replace("\\","/"),"bold")

                filename_label.tag_configure("SCRIPT",  background="#FFF",foreground="#ff9c33")
                filename_label.tag_configure("XML",  background="#FFF",foreground="#3377ff")
                filename_label.tag_configure("VOX",  background="#FFF",foreground="#ff33a3")



                if textLocalPathItemName.endswith('.lua'):
                    filename_label.insert(tk.END,"\nSCRIPT","SCRIPT")
                if textLocalPathItemName.endswith('.xml'):
                    filename_label.insert(tk.END,"\nXML INSTANCE","XML")
                if frominst == True:
                    filename_label.insert(tk.END,"\nVOXFILE FROM INSTANCE","VOX")
                elif textLocalPathItemName.endswith('.vox'):
                    filename_label.insert(tk.END,"\nVOXFILE","VOX")
                filename_label.insert(tk.END,"   " + convert_size(os.path.getsize(filepath)),"\tboldright")




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
        self.masterCount = 0
        instance_vox_files.clear()
        self.WastedSize = 0
        self.count.configure(text=str(self.masterCount) + " Files" + "\nWasted Space " + convert_size(self.WastedSize) + "", anchor="w", width=20)

       

    def show_file(self, filepath):
        os.startfile(filepath)

    def delete_file(self, filepath, item):
        isExist = os.path.exists(self.mod_entry.get() + "/TD_REDUNDANT/")
        if not isExist:
            os.makedirs(self.mod_entry.get() + "/TD_REDUNDANT/")
        self.WastedSize = self.WastedSize - os.path.getsize(filepath)

        os.rename(filepath, self.mod_entry.get() + "/TD_REDUNDANT/" + os.path.basename(filepath))
        self.count.configure(text=str(self.masterCount) + " Files" + "\nWasted Space " + convert_size(self.WastedSize) + "", anchor="w", width=20)
        
        item.destroy()
        self.list_items.remove(item)
        self.masterCount = self.masterCount - 1

    def clear_all(self):
        self.redundant_files = []
        self.listbox.destroy()
        self.listbox = tk.Listbox(self.listbox_frame, width=100, height=800)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.masterCount = 0

        instance_vox_files.clear()
        self.WastedSize = 0
        self.count.configure(text=str(self.masterCount) + " Files" + "\nWasted Space " + convert_size(self.WastedSize) + "", anchor="w", width=20)
        


root = tk.Tk()
root.wm_title('TD Redundant Checker')
root.geometry("635x760")
root.resizable(False,False)
app = Application(master=root)

app.mainloop()
