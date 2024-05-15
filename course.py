from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk,messagebox
import sqlite3


class course_class:
    def __init__(self, r):
        self.root = r
        self.root.geometry("1280x600")
        self.root.title("Course")
        self.root.config(bg="#d3d9e2")
        self.root.focus_force() # to make focus forcefully from dashboard

        title = Label(self.root,text="Manage Courses", font="arial 15 bold", bg="#42a5f5", fg="white")
        title.place(x=10, y=10, relwidth=0.985, height=45)


####
        course_name = Label(self.root, text="Course Name :", font="arial 13 ", bg="#fffcf2", bd="1",relief=RIDGE)
        course_name.place(x=10, y=80, width=200, height=55)

        self.course_name_var = StringVar()
        self.course_name_entry = Entry(self.root, textvariable=self.course_name_var, font="arial 13 ", bg="#eee9dc")  # Entry() is used for making input box
        self.course_name_entry.place(x=210, y=80,  width=330, height=55)
 ####

        course_credit = Label(self.root, text="Course Credit :", font="arial 13 ", bg="#fffcf2", bd="1",relief=RIDGE)
        course_credit.place(x=10, y=145, width=200, height=55)

        self.course_credit_var = IntVar()
        self.course_credit_entry = Entry(self.root, textvariable=self.course_credit_var, font="arial 13 ", bg="#eee9dc")  # Entry() is used for making input box
        self.course_credit_entry.place(x=210, y=145,  width=330, height=55)
####

        course_fee = Label(self.root, text="Course Fee :", font="arial 13 ", bg="#fffcf2", bd="1",relief=RIDGE)
        course_fee.place(x=10, y=210, width=200, height=55)

        self.course_fee_var = IntVar()
        self.course_fee_entry = Entry(self.root, textvariable=self.course_fee_var, font="arial 13 ", bg="#eee9dc")  # Entry() is used for making input box
        self.course_fee_entry.place(x=210, y=210,  width=330, height=55)
 ####

        description = Label(self.root, text="Description :", font="arial 13 ", bg="#fffcf2", bd="1",relief=RIDGE)
        description.place(x=10, y=275, width=200, height=100)

        self.description_entry = Text(self.root, font="arial 13 ", bg="#eee9dc")  # Entry() is used for making input box
        self.description_entry.place(x=210, y=275,  width=330, height=100)


# All buttons
        ButtonFrame=Frame(self.root, bg="white")
        ButtonFrame.place(x=10, y=380, width=530, height=70)


        self.add=Button(ButtonFrame,text="Save",font="arial 13 bold",bg="dodgerblue",fg="white",cursor="hand2",command=self.add)
        self.add.place(x=10,y=10,width=163,height=50)

        self.update=Button(ButtonFrame,text="Update",font="arial 13 bold",bg="slateblue",fg="white",cursor="hand2", command=self.update)
        self.update.place(x=183,y=10,width=163,height=50)

        self.delete=Button(ButtonFrame,text="Delete",font="arial 13 bold",bg="tomato",fg="white",cursor="hand2", command=self.delete)
        self.delete.place(x=356,y=10,width=163,height=50)




        # Search Panel
        self.search_var = StringVar()
        search_label = Label(self.root, text="Course Name: ", font="arial 13", bg="white", bd="1", relief=RIDGE).place(x=600, y=80, height=55, width=160)
        search_entry = Entry(self.root, textvariable=self.search_var, font="arial 13", bg="white").place(x=770, y=80, width=360, height=55)
        btn_search = Button(self.root, text="Search", font="arial 13 bold", bg="dodgerblue", fg="white", cursor="hand2",command=self.search).place(x=1120, y=80, width=150, height=55)


        #Course frame
        self.courseFrame=Frame(self.root, bd=2, relief=RIDGE)
        self.courseFrame.place(x=600,y=140,width=670 ,height=310)


        # Headings and Coloumns for the tables

        self.CourseTable=ttk.Treeview(self.courseFrame,columns=("cid","name","duration","charges","description"))
        self.CourseTable.pack(fill=BOTH, expand=1)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")

        self.CourseTable["show"] = "headings"
        self.CourseTable.column("cid", width=100)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)
        self.show_courses()  #all previous stored data will show


##################
#add course
    def add(self):
        connect = sqlite3.connect(database="rms.db")
        cursor = connect.cursor()

        try:
            # Message box for no course entry
            if self.course_name_var.get() == "":
                messagebox.showerror("Error", "Course name required", parent=self.root)
            # Message box for entering an existing course
            else:
                cursor.execute("SELECT * FROM course WHERE name=?", (self.course_name_var.get(),))
                row = cursor.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course name already exists", parent=self.root)
                else:
                    cursor.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)",
                                   (
                                    self.course_name_var.get(),
                                    self.course_credit_var.get(),
                                    self.course_fee_var.get(),
                                    self.description_entry.get("1.0", END)
                                                )
                                   )

                    connect.commit()
                    messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
                    self.show_courses()  #when we add data it will show in the table instantly


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")



#update course
    def update(self):
        connect = sqlite3.connect(database="rms.db")
        cursor = connect.cursor()

        try:
            # Message box for no course entry
            if self.course_name_var.get() == "":
                messagebox.showerror("Error", "Course name required", parent=self.root)
            # Message box for entering an existing course
            else:
                cursor.execute("SELECT * FROM course WHERE name=?", (self.course_name_var.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select course from list", parent=self.root)
                else:
                    cursor.execute("UPDATE course SET duration =? , charges =? , description =? where name =? ",
                                   (

                                    self.course_credit_var.get(),
                                    self.course_fee_var.get(),
                                    self.description_entry.get("1.0", END),
                                    self.course_name_var.get()
                                                )
                                   )

                    connect.commit()
                    messagebox.showinfo("Success", "Course Update Successfully", parent=self.root)
                    self.show_courses()  #when we add data it will show in the table instantly


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")




    # delete course
    def delete(self):
        connect = sqlite3.connect(database="rms.db")
        cursor = connect.cursor()

        try:
            # Message box for no course entry
            if self.course_name_var.get() == "":
                messagebox.showerror("Error", "Course name required", parent=self.root)
            # Message box for entering an existing course
            else:
                cursor.execute("SELECT * FROM course WHERE name=?", (self.course_name_var.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Select course from list", parent=self.root)
                else:
                    cursor.execute("DELETE FROM course WHERE name=?",
                                      (self.course_name_var.get(),)
                                   )

                    connect.commit()
                    messagebox.showinfo("Success", "Course Delete Successfully", parent=self.root)
                    self.show_courses()  # when we add data it will show in the table instantly


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")




    def show_courses(self):
        connect = sqlite3.connect(database="rms.db")
        cursor = connect.cursor()

        try:
            cursor.execute("SELECT * FROM course")
            rows = cursor.fetchall()

            self.CourseTable.delete(*self.CourseTable.get_children())

            for row in rows:
                self.CourseTable.insert('', 'end', values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error occurred: {str(ex)}")

    def search(self):
        connect = sqlite3.connect(database="rms.db")
        cursor = connect.cursor()

        try:
            # Fetch courses matching the search criteria
            cursor.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.search_var.get() + '%',))
            rows = cursor.fetchall()

            # Clear the existing data in the table widget
            self.CourseTable.delete(*self.CourseTable.get_children())

            # Insert fetched courses into the table widget
            for row in rows:
                self.CourseTable.insert('', 'end', values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error occurred: {str(ex)}")
########

if __name__ == "__main__":
    r = Tk()
    obj = course_class(r)
    r.mainloop()

