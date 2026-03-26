from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def add():
    return render_template("add.html")

@app.route("/list")
def list_task():
    return render_template("list_task.html")

@app.route("/add", methods=["GET", "POST"])
def get_add_input():
    if request.method == "POST" :
        task_name = request.form["task_name"]
        deadline = request.form["deadline"]
        subject = request.form["subject"]

        print("="*20, "\nData Di Terima")
        print(f"Nama Tugas : {task_name}\nTanggal Dikumpulkan : {deadline}\nMapel : {subject}\n", "="*20)
    
        return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)