  
@app.route("/", methods=["GET", "POST"])

def home():
    if request.method == "POST":
        zipcode = request.form["zip"]
        topic = request.form["topic"]
        stance = request.form["stance"]
        result = f"Got it!\nZip: {zipcode}\nTopic: {topic}\nStance: {stance}"
        return render_template_string(HTML, result=result)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
