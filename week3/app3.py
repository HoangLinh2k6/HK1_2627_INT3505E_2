from flask import Flask, jsonify, request

app = Flask(__name__)

ORDERS = [
    {
        "id": 1,
        "customer_id": 101,
        "status": "paid",
        "total": 150.0,
        "created_at": "2026-01-01",
    },
    {
        "id": 2,
        "customer_id": 102,
        "status": "pending",
        "total": 200.0,
        "created_at": "2026-01-02",
    },
    {
        "id": 3,
        "customer_id": 101,
        "status": "paid",
        "total": 50.0,
        "created_at": "2026-01-03",
    },
    {
        "id": 4,
        "customer_id": 103,
        "status": "cancelled",
        "total": 300.0,
        "created_at": "2026-01-04",
    },
    {
        "id": 5,
        "customer_id": 102,
        "status": "paid",
        "total": 120.0,
        "created_at": "2026-01-05",
    },
    {
        "id": 6,
        "customer_id": 101,
        "status": "pending",
        "total": 80.0,
        "created_at": "2026-01-06",
    },
    {
        "id": 7,
        "customer_id": 104,
        "status": "paid",
        "total": 220.0,
        "created_at": "2026-01-07",
    },
]


@app.route("/orders", methods=["GET"])
def get_orders():
  status = request.args.get("status")
  customer_id = request.args.get("customer_id")
  sort_param = request.args.get("sort", "id")
  fields = request.args.get("fields")
  cursor = request.args.get("cursor")
  try:
    limit = int(request.args.get("limit", 10))
  except ValueError:
    return (
        jsonify({
            "type": "https://api.example.com/probs/invalid-param",
            "title": "Invalid Parameter",
            "status": 400,
            "detail": "'limit' must be an integer.",
            "instance": request.path,
        }),
        400,
        {"Content-Type": "application/problem+json"},
    )

  results = list(ORDERS)
  if status:
    results = [o for o in results if o["status"] == status]

  if customer_id:
    try:
      cid = int(customer_id)
      results = [o for o in results if o["customer_id"] == cid]
    except ValueError:
      return (
          jsonify({
              "type": "https://api.example.com/probs/invalid-param",
              "title": "Invalid Parameter",
              "status": 400,
              "detail": "'customer_id' must be an integer.",
              "instance": request.path,
          }),
          400,
          {"Content-Type": "application/problem+json"},
      )
  reverse = False
  sort_key = sort_param
  if sort_param.startswith("-"):
    reverse = True
    sort_key = sort_param[1:]

  if results and sort_key in results[0]:
    results.sort(key=lambda x: x[sort_key], reverse=reverse)
  if cursor:
    try:
      last_id = int(cursor)
      start_index = 0
      found = False
      for idx, item in enumerate(results):
        if item["id"] == last_id:
          start_index = idx + 1
          found = True
          break

      results = results[start_index:] if found else []
    except ValueError:
      return (
          jsonify({
              "type": "https://api.example.com/probs/invalid-cursor",
              "title": "Invalid Cursor",
              "status": 400,
              "detail": (
                  f"Cursor '{cursor}' invalid."
              ),
              "instance": request.path,
          }),
          400,
          {"Content-Type": "application/problem+json"},
      )
  has_next = len(results) > limit
  paginated_results = results[:limit]
  next_cursor = None
  if has_next and paginated_results:
    next_cursor = paginated_results[-1]["id"]
  if fields:
    field_list = [f.strip() for f in fields.split(",") if f.strip()]
    paginated_results = [
        {k: v for k, v in item.items() if k in field_list}
        for item in paginated_results
    ]

  return (
      jsonify({
          "data": paginated_results,
          "pagination": {
              "limit": limit,
              "next_cursor": next_cursor,
              "has_more": has_next,
          },
      }),
      200,
  )