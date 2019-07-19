from flask import Flask, render_template, url_for

app = Flask(__name__)

## ⊕ [python - Flask css not updating - Stack Overflow](https://stackoverflow.com/questions/21714653/flask-css-not-updating)
def dated_url_for(endpoint, **values):
    import os
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

## -----------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    print('.. about')
    return render_template("about.html")

@app.route("/about_bs")
def about_bs():
    print('.. about')
    return render_template("about_bs.html")

@app.route("/salvador")
def salvador():
    return "Hello, Salvador"

if __name__ == "__main__":
    app.run(debug=True)
