from Tkinter import *
#from main import *
from song_finder import *
import crawler

class GUI(Frame):    
    def __init__(self, master):
        """
        Initial setup of GUI
        ***************No error section starts****************
        """
        Frame.__init__(self, master)
        #self.pack()
        self.grid()
        self.widgets()
        """
        ***************No error section ends******************
        """

    #Function to populate the RHS Listbox with metadata.
    def populate_Song_Metadata(self, relevant_data):
        """
        relevant_data: a dictionary containing (key:value) pairs of metadata.
        """
        self.lbox2.delete(0, END)
        print(relevant_data)
        for key in relevant_data.keys():
            insert_string = key + ': ' + str(relevant_data[key])
            self.lbox2.insert(END, insert_string)        
    
    #Function to generate a list of similar songs.
    def populate_Similar_Songs(self, search):
        """
        This function populates the LHS Listbox with similar songs
        based on the text entered in the search bar.
        search: the text entered in the search bar.
        """
        songs = populateSongs(search)
        self.lbox.delete(0, END)        
        self.lbox.insert(END, songs)
            
    #Function to initiate a search for the song.
    def search(self):
        """
        This function initiates a new search based on the text entered in the search bar.
        """
        search_string = self.search_var.get()
        print(search_string)
        self.populate_Similar_Songs(search_string)
        metadata = initiate_Search(search_string)        
        self.populate_Song_Metadata(metadata)
        initiate_Download(search_string, metadata)       
        

    #Function to trigger on double click of self.lbox
    def onDouble(self, event):
        """
        The event parameter provides the text that has been doubled click.
        This function initiates a new search based on the text selected.
        """
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])        
        self.entry.delete(0, END)
        self.entry.insert(END, value)
                
    #Function to setup the basic layout of the Graphical User Interface
    def widgets(self):
        """
        Loads the heading label, a box to enter the search (entry), a button to search
        and two boxes to display various data (Listbox).
        """
        
        Label(self, text="Song Downloader System", background="#CC0001", font= ("Comic Sans MS",16)).grid(row=0, column=0, padx=20)
        self.search_var = StringVar()
        
        self.entry = Entry(self, textvariable=self.search_var, width=45)
        self.entry.grid()
        
        self.b1=Button(self, text='Search', command=self.search)
        self.b1.grid(row=1, column=1, sticky=W, padx=20, pady=10)
        
        self.lbox = Listbox(self, width=45, height=15)
        self.lbox.grid(row=2, column=0, columnspan=6,sticky=W, padx=20, pady=10)
        self.lbox.bind("<Double-Button-1>", self.onDouble)
        
        self.lbox2 = Listbox(self, width=45, height=15)
        self.lbox2.grid(row=2, column=1, columnspan=6,sticky=W, padx=2000, pady=10)       
         
        
"""
Initial setup of GUI
***************No error section starts****************
"""
r = Tk()
r.geometry("800x600")
r.title("Song Downloader")
s = GUI(r)
s.mainloop()
"""
***************No error section ends******************
"""

