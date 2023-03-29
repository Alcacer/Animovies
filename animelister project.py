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
        sidebutton0.grid(row=0, pady=1, padx=5)
        sidebutton1 = Button(sidebar, text="Anime", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("anime"))
        sidebutton1.grid(row=1, pady=1, padx=5)
        sidebutton2 = Button(sidebar, text="Movies", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("movies"))
        sidebutton2.grid(row=2, pady=1, padx=5)
        sidebutton3 = Button(sidebar, text="Series", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("series"))
        sidebutton3.grid(row=3, pady=1, padx=5)
        sidebutton4 = Button(sidebar, text="Cartoons", bg="gray", relief=SUNKEN, width=9, height=7,
                             command=lambda: self.show_page("cartoons"))
        sidebutton4.grid(row=4, pady=1, padx=5)

        #Creating the different frames; The Frames class takes the arguments of the parent, category, and the file path of the image.
        self.frames = {"home": Home(body), "anime": Frames(body, "Anime", "images\\Naruto.png"), 
                        "movies": Frames(body, "Movies", "images\\jumanji.png"),
                        "series": Frames(body, "Series", "images\\money-heist.png"), 
                        "cartoons": Frames(body, "Cartoons", "images\\Lion king.png"), 
                        "view": View(body)}

        self.make_frame("home")
        self.show_page("home")  # Raises the Home page to the top.
        
        # Places all the frames in the exact location over each other.
        for x in ("anime", "movies", "series", "cartoons", "view"):
            thread = Thread(target=self.make_frame, args=(x,))
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
            listbox.insert(END, f"{number})  {i[1]} [{i[2]}]")
            number += 1


class Home(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        image = Image.open("images\\GOT.png")
        self.copy = image.copy()
        self.main = ImageTk.PhotoImage(image)


        self.canvas = Canvas(self, width=1050)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas.bind("<Configure>", self.resize)

        # Adding the background image and texts to the Canvas.
        self.canvas_image = self.canvas.create_image(0, 0, image=self.main, anchor=NW)

        self.canvas_text1 = self.canvas.create_text(510, 150, text="""    Welcome to
AniMovie Lister""", font=("Castellar", 50, "italic"), fill="#FFCD00")

        self.canvas_text2 = self.canvas.create_text(560, 370, text="""Welcome to AniMovie Lister. Store the names of your favorite Anime, Movies,
Series and Cartoons or new interesting ones that you want to make sure you watch.
Simply click on one of the tabs on the Sidebar to get started. 
For more help, click on the Help menu on the menu bar.""", fill="#FFCD00", font=("times new roman", 20, "italic"))

    def resize(self, event):
        
        width = event.width
        height = event.height
        

    # Resize the image to fill the canvas
        self.canvas.itemconfig(self.canvas_image, image=self.main.subsample(min(width/self.main.width(), height/self.main.height())))


class Frames(Frame):
    def __init__(self, parent, category, image_path):
        Frame.__init__(self, parent, bg="gray")
        image = Image.open(image_path)
        self.copy = image.copy()
        self.image = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas.bind("<Configure>", self.resize)
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
        button.bind("<Return>", self.add)
        self.canvas_entry = self.canvas.create_window(520, 401, window=entry)
        self.canvas_button = self.canvas.create_window(490, 450, window=button)

    def resize(self, event):
        if event.width > 1080:
            new_width = event.width
        else:
            new_width = 1080
        if event.height > 600:
            new_height = event.height
        else:
            new_height = 600

        if new_width > 1200:
            x1, x2, x3, x4, x5 = 610, 640, 420, 650, 640
        else:
            x1, x2, x3, x4, x5 = 500, 500, 300, 530, 500
        image = self.copy.resize((new_width, new_height))
        self.image = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.canvas_image, image=self.image)
        self.canvas.coords(self.canvas_text1, x1, 100)
        self.canvas.coords(self.canvas_text2, x2, 250)
        self.canvas.coords(self.canvas_text3, x3, 400)
        self.canvas.coords(self.canvas_entry, x4, 401)
        self.canvas.coords(self.canvas_button, x5, 450)

    def add(self, event):
        entry = self.entry_var.get()  # Gets the content of the Entry box typed in by the user.
        if len(entry) > 2:
            messagebox.showinfo("Added Successfully", f"{entry.title()} has been added successfully.")
            insert(entry.title(), self.category)
        self.entry_var.set("")
        

class View(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        global listbox
        image = Image.open("Images\\John Wick.png")
        self.copy = image.copy()
        self.main = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=TRUE)
        self.canvas.bind("<Configure>", self.rescale)

        self.canvas.create_image(0, 0, image=self.main, anchor=NW)
        self.canvas_text1 = self.canvas.create_text(500, 50, text="View", font=("Castellar", 50, "italic"),
                                                    fill="yellow")
        self.canvas_text2 = self.canvas.create_text(500, 150,
                                                    text="View your saved videos and delete the ones you've \nwatched "
                                                         "by clicking and hitting the Delete button. Also, \n"
                                                         "search for a specific video by typing into the search box.",
                                                    font=("times new roman", 22, "italic", "bold"), fill="yellow")
        self.entryvar = StringVar()
        entry = ttk.Entry(self, textvariable=self.entryvar, width=46, font=("Arial", 12, "bold"))
        entry.bind("<Return>", self.search_box)
        button = ttk.Button(self, text="Search", command=lambda: self.search_box(""))
        listbox = Listbox(self, width=60, height=12, font=("comic sans ms", 13, "italic"))
        scroll = ttk.Scrollbar(self)
        listbox.configure(yscrollcommand=scroll.set)
        scroll.configure(command=listbox.yview)
        del_button = ttk.Button(self, text="Delete", width=25, command=self.delete_item)

        self.canvas_entry = self.canvas.create_window(400, 231, window=entry)
        self.canvas_button = self.canvas.create_window(650, 230, window=button)
        self.canvas_listbox = self.canvas.create_window(450, 420, window=listbox)
        self.canvas_scrollbar = self.canvas.create_window(742, 420, window=scroll, height=300)
        self.del_button = self.canvas.create_window(430, 530, window=del_button)

    def search_box(self, event):
        if len(self.entryvar.get()) > 0:
            listbox.delete(0, END)
            number = 1
            for x in search(self.entryvar.get().title()):
                listbox.insert(END, f"{number})  {x[1]} [{x[2]}]")
                number += 1
            if listbox.index(END) == 0:
                messagebox.showinfo("No Search Results", f"Sorry, Couldn't find what you were looking for.")
            self.entryvar.set("")

    def rescale(self, event):
        if event.width > 1200:
            x1, x2, x3, x4, x5, x6, x7 = 650, 650, 550, 800, 600, 902, 580
            y1, y2, y3, y4, y5, y6, y7 = 90, 190, 271, 270, 460, 460, 630
        else:
            x1, x2, x3, x4, x5, x6, x7 = 500, 500, 400, 650, 450, 742, 430
            y1, y2, y3, y4, y5, y6, y7 = 50, 130, 206, 205, 380, 380, 550
        self.canvas.coords(self.canvas_text1, x1, y1)
        self.canvas.coords(self.canvas_text2, x2, y2)
        self.canvas.coords(self.canvas_entry, x3, y3)  # Changes the coordinates of the widgets when resized.
        self.canvas.coords(self.canvas_button, x4, y4)
        self.canvas.coords(self.canvas_listbox, x5, y5)
        self.canvas.coords(self.canvas_scrollbar, x6, y6)
        self.canvas.coords(self.del_button, x7, y7)

    def delete_item(self):
        try:
            index = listbox.curselection()[0]  # Gets the active row in the listbox
            selected_row = listbox.get(index)  # Gets the content of the active row
            name = []
            for x in selected_row[4:]:
                if x == "[":
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
app.iconbitmap("images\\favicon.ico")
app.mainloop()
