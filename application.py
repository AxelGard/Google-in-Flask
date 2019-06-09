from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import csv, wikipedia, os


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def get_search():
    #search_result = [page for page in RESULTS if page.startwith(request.args.get("q"))]
    search_result = []
    number_of_results = 0
    q = request.args.get("q")
    for page in RESULTS:
        if page[0].startswith(q) or page[0].find(q) != -1:
            page_sum = ""
            number_of_results += 1
            summary = wikipedia.summary(page[0])
            for i in range(len(summary)):
                #print(summary[i])
                if summary[i] == "." and i > 40:
                    break
                else:
                    page_sum += summary[i]
            page_sum += "."
            search_result += [page + [page_sum]]

    return render_template("search_result.html", search_result=search_result, number_of_results=number_of_results)

def get_all_pages():
    page_list = []
    with open('data_base.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            page_list += [[str(row[0]), str(row[1])]]

    #page_list = [["google", "https://www.google.com"], ["facebook", "https://www.facebook.com"], ["wikipedia", "https://www.wikipedia.org"], ["reddit", "https://www.reddit.com"]]
    return page_list

RESULTS = get_all_pages()

@app.route("/update")
def update():
    global RESULTS
    RESULTS = get_all_pages()
    return "<p> sucess </p>"

if __name__ == '__main__':
    app.run(debug=True, port=4000)


#regular exp : (\w+)\s+(\w+.*)
#replace with : $1,https://www.$2
