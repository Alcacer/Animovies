from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from threading import Thread
from webbrowser import open_new
from backend import *


class AniMovieLister(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Adding the Menu bar
        menu = Menu(self)
        self.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(label="File", menu=file)

        view = Menu(self)
        view.add_command(label="View All", command=self.view_all_menu)
        view.add_separator()
        view.add_command(label="View Anime", command=lambda: self.view_menu("Anime"))
        view.add_separator()
        view.add_command(label="View Movies", command=lambda: self.view_menu("Movies"))
        view.add_separator()
        view.add_command(label="View Series", command=lambda: self.view_menu("Series"))
        view.add_separator()
        view.add_command(label="View Cartoons", command=lambda: self.view_menu("Cartoons"))
        menu.add_cascade(label="View", menu=view)

        help_menu = Menu(self, tearoff=0)
        contact = Menu(self, tearoff=0)
        contact.add_command(label="Linkedin",
                            command=lambda: open_new("https://www.linkedin.com/in/alcacer/"))
        contact.add_separator()
        contact.add_command(label="Github", command=lambda: open_new("https://github.com/Alcacer/"))
        help_menu.add_cascade(label="Contact", menu=contact)
        menu.add_cascade(label="Help & Enquiry", menu=help_menu)

        sidebar = Frame(self, width=100, bg="black")
        sidebar.pack(side=LEFT, fill=Y)

        body = Frame(self, bg="black")
        body.pack(side=RIGHT, fill=BOTH, expand=TRUE)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.body = body

        # Adding the tabs to the Sidebar
        sidebutton0 = Button(sidebar, text="Home", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("home"))
        sidebutton0.grid(row=0, pady=3, padx=5)
        sidebutton1 = Button(sidebar, text="Anime", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("anime"))
        sidebutton1.grid(row=1, pady=2, padx=5)
        sidebutton2 = Button(sidebar, text="Movies", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("movies"))
        sidebutton2.grid(row=2, pady=2, padx=5)
        sidebutton3 = Button(sidebar, text="Series", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("series"))
        sidebutton3.grid(row=3, pady=2, padx=5)
        sidebutton4 = Button(sidebar, text="Cartoons", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("cartoons"))
        sidebutton4.grid(row=4, pady=2, padx=5)

        #Creating the different frames; The Frames class takes the arguments of the parent, category, and the file path of the image.
        self.frames = {"home": Home(body), "anime": Frames(body, "Anime", "images\\Naruto.png"), 
                        "movies": Frames(body, "Movies", "images\\jumanji.png"),
                        "series": Frames(body, "Series", "images\\money-heist.png"), 
                        "cartoons": Frames(body, "Cartoons", "images\\Lion king.png"), 
                        "view": View(body)}

        self.make_frame("home")
        self.show_page("home")  # Raises the Home page to the top.
        
        # Threads are employed to concurrently load the other frames in the background.
        for x in ("anime", "movies", "series", "cartoons", "view"):
            thread = Thread(target=self.make_frame, args=(x,)) #Remember the args argument takes a tuple, hence the comma.
            thread.start()
    
    def make_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.grid(row=0, sticky=NSEW)

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def view_menu(self, category):
        global listbox
        listbox.delete(0, END)
        self.show_page("view")
        listbox.insert(END, f"      {category}      ")
        number = 1
        for i in view(category): #This view function is from the backend.py file.
            listbox.insert(END, f"{number})  {i[1]} ")
            number += 1

    def view_all_menu(self):
        global listbox
        listbox.delete(0, END)
        self.show_page("view")
        number = 1
        for i in view_all():
            listbox.insert(END, f"{number})  {i[1]} {{{i[2]}}}")
            number += 1


class Home(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        image = Image.open("images\\GOT.png")
        self.main = ImageTk.PhotoImage(image)


        self.canvas = Canvas(self, width=1050)
        self.canvas.pack(fill=BOTH, expand=TRUE)

        # Adding the background image and texts to the Canvas.
        self.canvas_image = self.canvas.create_image(0, 0, image=self.main, anchor=NW)

        self.canvas_text1 = self.canvas.create_text(510, 150, text="""    Welcome to
AniMovie Lister""", font=("Castellar", 50, "italic"), fill="#FFCD00")

        self.canvas_text2 = self.canvas.create_text(560, 370, text="""Welcome to AniMovie Lister. Store the names of your favorite Anime, Movies,
Series and Cartoons or new interesting ones that you want to make sure you watch.
Simply click on one of the tabs on the Sidebar to get started. 
For more help, click on the Help menu on the menu bar.""", fill="#FFCD00", font=("times new roman", 20, "italic"))


class Frames(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.category = category
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas_image = self.canvas.create_image(0, 0, image=self.image, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(500, 100, text=f"{category}", font=("Castellar", 50, "italic"),
                                                    fill="#FFFD00")
        self.canvas_text2 = self.canvas.create_text(500, 250,
                                                    text=f"Type in the name of the {category.lower()} you wish to save \nand hit "
                                                         "the Add button. "
                                                         f"\nTo view your saved {category.lower()}, click on the View menu\non the "
                                                         f"menu bar and select 'View {category}'.",
                                                    font=("times new roman", 22, "italic", "bold"), fill="#FFFD00")
        self.canvas_text3 = self.canvas.create_text(290, 400, text=f"Name of the {category}:  ",
                                                    font=("times new roman", 16, "italic", "bold"),
                                                    fill="#FFFD00")
        self.entry_var = StringVar()
        entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        button = ttk.Button(self, text=f"Add {category}", width=25, command=lambda: self.add(""))
        entry.bind("<Return>", self.add)
        button.bind("<Return>", self.add)
        self.canvas_entry = self.canvas.create_window(535, 401, window=entry)
        self.canvas_button = self.canvas.create_window(490, 450, window=button)

    def add(self, event):
        entry = self.entry_var.get()  # Gets the content of the Entry box typed in by the user.
        if len(entry.strip()) > 2:
            messagebox.showinfo("Added Successfully", f"{entry.title()} has been added successfully.")
            insert(entry.title(), self.category)
        elif len(entry.strip()) < 1:
            pass
        else :
            messagebox.showinfo("Must be more than 2 characters","The entered characters are too short.")
        self.entry_var.set("")
        

class View(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        global listbox
        image = Image.open("Images\\John Wick.png")
        self.main = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)

        self.canvas.create_image(0, 0, image=self.main, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(400, 50, text="View", font=("Castellar", 40, "italic"),
                                                    fill="yellow")
        self.canvas_text2 = self.canvas.create_text(400, 130,
                                                    text="View your saved videos and delete the ones you've \nwatched "
                                                         "by clicking and hitting the Delete button. Also, \n"
                                                         "search for a specific video by typing into the search box.",
                                                    font=("times new roman", 18, "italic", "bold"), fill="yellow")
        self.entryvar = StringVar()
        entry = ttk.Entry(self, textvariable=self.entryvar, width=40, font=("Helvetica", 12, "italic"))
        entry.bind("<Return>", self.search_box)
        search_button = ttk.Button(self, text="Search", command=lambda: self.search_box(""))
        search_button.bind("<Return>", self.search_box)
        listbox = Listbox(self, width=40, height=12, font=("comic sans ms", 13, "italic"))
        scroll = ttk.Scrollbar(self)
        listbox.configure(yscrollcommand=scroll.set)
        scroll.configure(command=listbox.yview)
        del_button = ttk.Button(self, text="Delete", width=25, command=self.delete_item)

        self.canvas_entry = self.canvas.create_window(350, 215, window=entry)
        self.canvas_button = self.canvas.create_window(572, 215, window=search_button)
        self.canvas_listbox = self.canvas.create_window(380, 390, window=listbox)
        self.canvas_scrollbar = self.canvas.create_window(591, 390, window=scroll, height=305)
        self.del_button = self.canvas.create_window(380, 560, window=del_button)

    def search_box(self, event):
        if len(self.entryvar.get().strip()) > 0:
            listbox.delete(0, END)
            number = 1
            for x in search(self.entryvar.get().title().strip()):
                listbox.insert(END, f"{number})  {x[1]}   {{{x[2]}}}")
                number += 1
            if listbox.index(END) == 0:
                messagebox.showinfo("No Search Results", f"Sorry, Couldn't find what you were looking for.")
            self.entryvar.set("")

    def delete_item(self):
        try:
            index = listbox.curselection()[0]  # Gets the active row in the listbox
            selected_row = listbox.get(index)  # Gets the content of the active row
            name = []
            for x in selected_row[4:]:
                if x == "{":
                    break
                else:
                    name.append(x)
            full_name = "".join(name[:-1])
            int(selected_row[0])  # To make sure nobody tries to delete the Headers(Anime, Movies, etc).
            ask = messagebox.askyesno("Delete?", f"Are you sure you want to delete {full_name}?")
            if ask:
                delete(full_name)
                messagebox.showinfo("Deleted!", f"{full_name} has been deleted")
                listbox.delete(index)
        except IndexError:
            pass
        except ValueError:
            pass


app = AniMovieLister()
app.title("AniMovie Lister")
app.iconbitmap("Images\\app.ico")
app.maxsize(1160,605)
app.minsize(1160,605)
app.mainloop()
