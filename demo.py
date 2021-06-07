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

app = Flask(__name__)


@app.route("/") 
def home():
    cur.execute('Select * from Student')
    rows = cur.fetchall()
    return render_template("studentPage.html", things=rows)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr =user))
    else:
        return render_template("login.html")



@app.route("/addRemoveStudent", methods = ["POST","GET"]) 
def addRemoveStudent():
    if request.method == "POST":
        if 'add' in request.form:
            #TODO double check data, protect against sql injections
            #TODO double check if values are legit
            StuID = request.form["studentID"]
            Fname = request.form["first"]
            Lname = request.form["last"]
            gender = request.form["gender"]
            super = request.form["super"]
            alias = request.form["alias"]
            dob = request.form["dob"]

            cur.execute('INSERT INTO Student (StudentID, FirstName, LastName, Alias, \
                Gender, SuperPower, DOB, IsCurrentlyEnrolled,adminID) \
                Values(%s,%s,%s,%s,%s,%s,%s,TRUE,1)',(int(StuID),Fname,Lname,alias,gender,super,dob))
            con.commit()
            return redirect(url_for("home"))
        elif 'delete' in request.form:
            try:
                # studID = int(request.form["studID"])
                # cur.execute("SELECT ID FROM STUDENT WHERE STUDENTID = %s",(studID))
                # studID = cur.fetchall()
                # print("message = " + studID)
                # cur.execute('DELETE FROM Transcript WHERE Transcript.StudentID = %s',[studID])
                # # Find the noteID based on studentID, use that to delete notes
                # # cur.execute('DELETE FROM Notes WHERE Student_Notes.StudentID = %s',[studID])
                # cur.execute('DELETE FROM Student_Notes WHERE Student_Notes.StudentID = %s',[studID])
                # cur.execute('DELETE FROM STUDENT WHERE ID = %s',[studID])
                return redirect(url_for("home"))
            except:
                flash('Invalid password provided', 'error')
        else:
            StuID = request.form["studentID"]
            Fname = request.form["first"]
            Lname = request.form["last"]
            gender = request.form["gender"]
            super = request.form["super"]
            alias = request.form["alias"]
            dob = request.form["dob"]
            enr = request.form["enrollment"]

            cur.execute('Update Student \
                SET FirstName= %s, LastName= %s, Alias= %s, \
                Gender= %s, SuperPower= %s, DOB= %s, \
                IsCurrentlyEnrolled= %s WHERE StudentID = %s' ,(Fname,Lname,alias,gender,super,dob,enr,int(StuID)))
            con.commit()
               
    else:
        return render_template("addRemoveStudent.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr} </h1>"

if __name__ == "__main__":
    app.run(debug =True)


# close cursor
cur.close()

#close the connection
con.close()
