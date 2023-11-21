import os
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from TFTP121_Client import TFTP121_Client

class TFTP121(object):
    def __init__(self, root):
        self.host = tkinter.StringVar(root)
        self.browse_value = tkinter.StringVar()

        self.server = tkinter.LabelFrame(root, text="Destination IP Address")
        self.block = tkinter.LabelFrame(root, text="Block Size (Bytes)")
        self.locally_selected = tkinter.LabelFrame(root, text="Locally Selected File")
        self.new_filename = tkinter.LabelFrame(root, text="New Filename")

        # Set the background color of the root window
        root.configure(bg='white')

        # Set the background color of the frames
        self.server.configure(bg='white')
        self.block.configure(bg='white')
        self.locally_selected.configure(bg='white')
        self.new_filename.configure(bg='white')

        # Entry fields
        self._host = tkinter.Entry(self.server, takefocus=1, width=50)  
        self.local_file = tkinter.Entry(self.locally_selected, width=50, textvariable=self.browse_value, highlightbackground="light gray") 
        self.updated_filename = tkinter.Entry(self.new_filename, width=50, highlightbackground="light gray")  

        # Block size dropdown menu
        self.block_size = tkinter.StringVar(root)
        block_size_choices = ["512 (Default)", "1024", "1428", "2048", "4096", "8192"]
        self.block_size.set(block_size_choices[0])  # Set the default value

        self.block_size_dropdown = OptionMenu(self.block, self.block_size, *block_size_choices)
        self.block_size_dropdown.config(width=15)  # Adjusted the width of the dropdown menu

        # Buttons
        self.write = tkinter.Button(root, text="Upload", padx=15, pady=8, command=self.upload)  
        self.browse = tkinter.Button(self.locally_selected, text="Browse", command=self.browse)

        # Layout
        self.server.grid(in_=root, column=1, row=1, columnspan=1, rowspan=1, sticky="news", padx=10, pady=10)  
        self.block.grid(in_=root, column=1, row=2, columnspan=1, rowspan=1, sticky="news", padx=10, pady=10)  
        self.locally_selected.grid(in_=root, column=1, row=3, columnspan=1, rowspan=1, sticky="news", padx=10, pady=10)
        self.new_filename.grid(in_=root, column=1, row=4, columnspan=1, rowspan=1, sticky="news", padx=10, pady=10)  

        self._host.grid(in_=self.server, column=1, row=1, columnspan=1, padx=10, pady=10, rowspan=1, sticky="ew")  
        self.block_size_dropdown.grid(in_=self.block, column=1, row=1, columnspan=1, padx=10, pady=10, rowspan=1, sticky="ew")  
        self.local_file.grid(in_=self.locally_selected, column=1, row=1, padx=10, pady=10, columnspan=1, rowspan=1, sticky="ew")  
        self.updated_filename.grid(in_=self.new_filename, column=1, row=1, columnspan=1, padx=10, pady=10, rowspan=1, sticky="ew")  

        self.write.grid(in_=root, column=1, row=5, pady=10, sticky="n")  
        self.browse.grid(in_=self.locally_selected, column=2, row=1, padx=10, pady=10, columnspan=1, rowspan=1, sticky="e")  

        root.grid_rowconfigure(1, weight=0, minsize=40, pad=0)
        root.grid_rowconfigure(2, weight=0, minsize=40, pad=0)
        root.grid_rowconfigure(3, weight=0, minsize=40, pad=0)
        root.grid_rowconfigure(4, weight=0, minsize=40, pad=0)
        root.grid_rowconfigure(5, weight=0, minsize=40, pad=0)
        root.grid_columnconfigure(1, weight=1)  # Adjust column configuration to take remaining space

        self.server.grid_rowconfigure(1, weight=1)  
        self.server.grid_columnconfigure(1, weight=1)  
        self.block.grid_rowconfigure(1, weight=1)  
        self.block.grid_columnconfigure(1, weight=1)  
        self.locally_selected.grid_rowconfigure(1, weight=1)  
        self.locally_selected.grid_columnconfigure(1, weight=1)  
        self.new_filename.grid_rowconfigure(1, weight=1)  
        self.new_filename.grid_columnconfigure(1, weight=1) 

    def upload(self):
        when_uploading = TFTP121_Client(self._host.get(), 69)
        file_name = self.local_file.get()
        updated_filename = self.updated_filename.get()
        blkSize = self.block_size.get().split()[0]  # Extract the block size value without the text

        if not os.path.isfile(file_name):
            raise Exception('File %s does not exist!' % file_name)
        else:
            if when_uploading.upload(int(blkSize), file_name, os.path.basename(file_name) if len(updated_filename) <= 0 else updated_filename):
                print('File transferred successfully.')

    def browse(self):
        self.browse_value.set(askopenfilename())

def main():
    app = Tk()
    window = TFTP121(app)
    app.title('TFTP File Upload')  # change
    app.resizable(width=FALSE, height=FALSE)

    try:
        run()
    except NameError:
        pass

    app.protocol('WM_DELETE_WINDOW', app.quit)
    app.mainloop()

if __name__ == '__main__':
    main()
