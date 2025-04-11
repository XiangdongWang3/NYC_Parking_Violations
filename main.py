from flask import Flask, request, jsonify
import psycopg


app = Flask(__name__)

conn = psycopg.connect(
    host="localhost",
    port='5432',
    dbname="54_Project",
    user="postgres",
    password="123")


# 1. Violation Summary
@app.route("/violations/summary", methods=["GET"])
def get_violation_summary():
    date = request.args.get("date")
    print(f"Received date: {date}")

    if not date:
        return jsonify({"error": "Missing date parameter"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) AS total_violations,
                   SUM(vf.fine_amount) AS total_fine
            FROM summons s
            JOIN violation_finance vf ON s.summons_number = vf.summons_number
            WHERE s.issue_date = %s
        """, (date,))
        result = cur.fetchone()
        cur.close()

        if not result or result[0] == 0:
            return jsonify({"message": f"No violations found for {date}"}), 404

        return jsonify({
            "date": date,
            "total_violations": result[0],
            "total_fine": float(result[1]) if result[1] else 0.0
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


# 2. Violation Type Distribution (Bar Chart)
@app.route("/violations/type-distribution", methods=["GET"])
def violation_type_distribution():
    date = request.args.get("date")
    print(f"Violation type distribution query for date: {date}")

    if not date:
        return jsonify({"error": "Missing date parameter"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.violation, COUNT(*) AS count
            FROM summons s
            WHERE s.issue_date = %s AND s.violation IS NOT NULL
            GROUP BY s.violation
            ORDER BY count DESC
        """, (date,))
        rows = cur.fetchall()
        cur.close()

        result = [{"violation": v, "count": c} for v, c in rows]
        return jsonify(result)

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


# 3. State Distribution (Pie Chart)
@app.route("/violations/state-distribution", methods=["GET"])
def state_distribution():
    date = request.args.get("date")
    print(f"State distribution query for date: {date}")

    if not date:
        return jsonify({"error": "Missing date parameter"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.state, COUNT(*) AS count
            FROM summons s
            WHERE s.issue_date = %s AND s.state IS NOT NULL
            GROUP BY s.state
            ORDER BY count DESC
        """, (date,))
        rows = cur.fetchall()
        cur.close()

        result = [{"state": s, "count": c} for s, c in rows]
        return jsonify(result)

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


# 4. Detailed Violation Lookup by Summons Number
@app.route("/violations/details", methods=["GET"])
def get_violation_details():
    summons_number = request.args.get("summons_number")
    print(f"Detail query for summons_number: {summons_number}")

    if not summons_number:
        return jsonify({"error": "Missing summons_number parameter"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT s.summons_number, s.plate, s.state, s.license_type, s.violation,
                   s.issue_date, s.violation_time, s.precinct,
                   vf.fine_amount, vf.penalty_amount, vf.interest_amount, vf.amount_due,
                   f.day_of_week, f.violation_hour, f.am_pm,
                   l.county, l.issuing_agency
            FROM summons s
            LEFT JOIN violation_finance vf ON s.summons_number = vf.summons_number
            LEFT JOIN violation_features f ON s.summons_number = f.summons_number
            LEFT JOIN location_info l ON s.summons_number = l.summons_number
            WHERE s.summons_number = %s
        """, (summons_number,))

        result = cur.fetchone()
        columns = [desc[0] for desc in cur.description]
        cur.close()

        if not result:
            return jsonify({"message": f"No violation found for summons_number {summons_number}"}), 404

        return jsonify(dict(zip(columns, result)))

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5004)
