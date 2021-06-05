import psycopg2
from flask import Flask, redirect, url_for, render_template, request, flash

#connect to the local host db
con = psycopg2.connect (
host = "database-finalproject.cwap51qwtcts.us-west-2.rds.amazonaws.com",
database = "webdb",
user = "postgres",
password = "2fD9vPoMU6HAfMM"
)

#cursor
cur = con.cursor()

#execute query
cur.execute('Select * from Student')
rows = cur.fetchall()

for r in rows:
   print(f"ID {r[0]} name {r[1]}")

#execute query
cur.execute('Select * from Course_Catalog')
courseRows = cur.fetchall()

for r in courseRows:
   print(f"SLN {r[0]} Name {r[1]} CourseCredits {r[2]} Type {r[3]}")

print(id) 
#execute query
cur.execute('Select * from Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID)')
courseInfoRows = cur.fetchall()

#execute query
cur.execute('SELECT * FROM Course_Info JOIN Course_Catalog ON (Course_Info.CourseID = Course_Catalog.ID) JOIN Transcript ON (Course_Info.ID = Transcript.ClassID) JOIN Student ON (Student.ID = Transcript.StudentID) WHERE Course_Info.SLN = 10000 AND Course_Info.RoomID = 5')
courseAttendeesRows = cur.fetchall()

# close cursor
#cur.close()

#close the connection
#con.close()

app = Flask(__name__)
app.secret_key = '1234'

@app.route("/") 
def home():
    return render_template("studentPage.html", things = rows)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")

@app.route("/courseInfo") 
def courseInfo():
    return render_template("courseInfoPage.html", things = courseInfoRows)

@app.route("/courseAttendees") 
def courseAttendees():
    return render_template("courseAttendees.html", things = courseAttendeesRows)

@app.route("/addCourse", methods = ["POST", "GET"])
def add():
    if request.method == "POST":

        # request data
        name = request.form["nm"]
        cc = request.form["creds"]
        type = request.form["type"]

        # check if its an add or remove
        if 'add' in request.form:

            # checks if course already exists
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            for r in courseRows:
                curName = r[1]
               
                if (curName == name): 
                    flash("You cannot add a course that already exists.", "error") 
                    return render_template("addCourse.html")

            # ---------------
            # adds to course catalog
            cur.execute("""INSERT INTO Course_Catalog (Name, CourseCredits, Type) 
                            VALUES (%s, %s, %s)""", (name, cc, type))

            # update table
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            con.commit()

            return render_template("coursePage.html", things = courseRows)
        else:

            # checks if course doesn't exist
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            for r in courseRows:
                curName = r[1]
               
                if (curName == name): 
                   # removes course from course catalog
                    cur.execute("""DELETE FROM Course_Catalog WHERE Name = %s""", [name])
                    con.commit()

                    # update table
                    cur.execute('Select * from Course_Catalog')
                    courseRows = cur.fetchall()
                    
                    return render_template("coursePage.html", things = courseRows) 
                else:
                    flash("You cannot remove a course that doesn't exists.", "error") 
                    return render_template("addCourse.html")
    else:
        return render_template("addCourse.html")

@app.route("/addClass", methods = ["POST", "GET"])
def addClass():
    if request.method == "POST":

        # request data
        name = request.form["name"]
        section = request.form["section"]
        roomid = request.form["roomid"]
        instructor = request.form["ins"]
        time = request.form["time"]
        quarter = request.form["quarter"]
        year = request.form["yr"]

        # check if its an add or remove
        if 'add' in request.form:
        
            cur.execute('Select * from Course_Catalog')
            courseRows = cur.fetchall()
            for r in courseRows:
                curName = r[1]
               
                if (curName == name): 
                    # adds to course info
                    cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [name])
                    idEntry = cur.fetchall()
                    id = idEntry[0][0]
                    
                    cur.execute("""INSERT INTO Course_Info (CourseID, Section, RoomID, InstructorName, Time, Quarter, Year) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)""", (id, section, roomid, instructor, time, quarter, year))

                    con.commit()

                    # update table
                    cur.execute('Select * from Course_Info')
                    courseInfoRows = cur.fetchall()
                    con.commit()

                    return render_template("courseInfoPage.html", things = courseInfoRows)

                else: 
                    flash("You cannot add a class to a course that doesn't exists.", "error") 
                    return render_template("addCourse.html")
        else:

            # for class delete only name and section are needed
            # checks if course doesn't exist
            cur.execute('Select * from Course_Info')
            courseInfoRows = cur.fetchall()
            for r in courseInfoRows:
                curName = r[1]
               
                if (curName == name): 
                    cur.execute('SELECT ID FROM Course_Catalog WHERE Name = %s', [name])
                    idEntry = cur.fetchall()
                    id = idEntry[0][0]

                    cur.execute('SELECT SLN FROM Course_Info WHERE CourseID = %s AND Section = %s', (id, section))
                    slnEntry = cur.fetchall()
                    sln = slnEntry[0][0]

                    # removes course from course Info
                    cur.execute("""DELETE FROM Course_Info WHERE SLN = %s""", [sln])
                    con.commit()

                    # update table
                    cur.execute('Select * from Course_Info')
                    courseInfoRows = cur.fetchall()
            
                    return render_template("courseInfoPage.html", things = courseInfoRows)
                else:
                    flash("You cannot remove a class that doesn't exists.", "error") 
                    return render_template("addCourse.html")
            
    else:
        # show main screen initially
        return render_template("addClass.html")

@app.route("/CourseCatalog") 
def course():
    return render_template("coursePage.html", things = courseRows)


if __name__ == "__main__":
     app.run(debug =True)
     
# close cursor
cur.close()

#close the connection
con.close()