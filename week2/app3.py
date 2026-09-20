from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

DEFAULT_SIZE, MAX_SIZE = 20, 100

BOOKS = [{"id":1,"title":"A1","author":"B1"},
         {"id":2,"title":"A2","author":"B2"},
         {"id":3,"title":"A3","author":"B3"},
         {"id":4,"title":"A4","author":"B4"},
         {"id":5,"title":"A5","author":"B5"},
         {"id":6,"title":"A6","author":"B6"},
         {"id":7,"title":"A7","author":"B7"},
         {"id":8,"title":"A8","author":"B8"},
         {"id":9,"title":"A9","author":"B9"},
         {"id":10,"title":"A10","author":"B10"},
         {"id":11,"title":"A11","author":"B11"},
         {"id":12,"title":"A12","author":"B12"},
         {"id":13,"title":"A13","author":"B13"},
         {"id":14,"title":"A14","author":"B14"},
         {"id":15,"title":"A15","author":"B15"},
         {"id":16,"title":"A16","author":"B16"},
         {"id":17,"title":"A17","author":"B17"},
         {"id":18,"title":"A18","author":"B18"},
         {"id":19,"title":"A19","author":"B19"},
         {"id":20,"title":"A20","author":"B20"},
         {"id":21,"title":"A21","author":"B21"}]

@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    flt = BOOKS
    a = request.args.get("author")
    if a:
        flt = [b for b in flt if b["author"].lower()==a.lower()]
    q = (request.args.get("q")or"").lower()
    if q:
        flt = [b for b in flt if q in b["title"].lower()]

    total = len(flt); start=(page-1)*size; end=start+size
    items = flt[start:end]; last=(total+size-1)//size

    def u(p):
        return f"/books?page={p}&size={size}"
    links = {
        "self":{"href":u(page)},
        "first":{"href":u(1)},
        "last":{"href":u(max(last,1))}
    }
    if page > 1:
        links["prev"]={"href":u(page-1)}
    if end < total:
        links["next"]={"href":u(page+1)}
    body = {
        "data":items,
        "pagination": {
            "page":page,
            "size":size,
            "total":total,
            "total_pages":last
        },
        "_links":links
    }
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"]="public, max-age=30"
    return resp