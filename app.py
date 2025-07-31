from flask import Flask, jsonify, request
import random
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock alert data generator
def generate_mock_alerts(num_alerts=3):
    alerts = []
    event_types = ["Server Downtime", "Security Breach", "High CPU Usage", "Disk Space Low", "Network Latency"]
    severity_levels = ["Critical", "High", "Medium", "Low"]
    urgency_levels = ["Immediate", "Expected"]
    description_templates = [
        "Detected {issue} on host {host}. Impact: {impact}. Recommend {action}.",
        "Alert triggered due to {issue}. Current status: {status}. Last checked {time} ago.",
        "{issue} reported in {area}. Potential cause: {cause}. Monitor for escalation.",
        "System experiencing {issue}. Affected services: {services}. Resolve by {time}."
    ]
    host_examples = [
        f"server-{random.choice(['web', 'db', 'app'])}{random.randint(100, 999)}",
        f"node-{chr(random.randint(65, 90))}{random.randint(10, 99)}",  # e.g., node-A23
        f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"   # Random IP
    ]
    area_codes = [f"{random.choice(['DC', 'ZONE', 'CLUSTER'])}-{random.randint(1, 99):03d}{chr(random.randint(65, 90)) if random.random() > 0.5 else ''}" for _ in range(10)]  # Pre-generate some codes like DC-001A

    for i in range(num_alerts):
        host = random.choice(host_examples)
        area_code = random.choice(area_codes)
        event = random.choice(event_types)
        desc_template = random.choice(description_templates)
        desc = desc_template.format(
            issue=event.lower(),
            host=host,
            impact=random.choice(["service outage", "performance degradation", "data loss risk"]),
            action=random.choice(["reboot", "investigate logs", "scale resources"]),
            status=random.choice(["unresolved", "intermittent", "escalating"]),
            time=random.randint(5, 60),
            area=area_code,
            cause=random.choice(["hardware failure", "configuration error", "traffic spike"]),
            services=random.choice(["API endpoints", "database queries", "user authentication"])
        )
        alert = {
            "id": f"alert-{random.randint(1000, 9999)}",
            "event": event,
            "severity": random.choice(severity_levels),
            "status": "Active",
            "sent": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
            "effective": datetime.now().isoformat(),
            "expires": (datetime.now() + timedelta(hours=1)).isoformat(),
            "headline": f"Alert: {random.choice(['Urgent', 'Warning'])} Issue Detected",
            "description": desc,
            "affectedArea": area_code,  # e.g., "DC-004B"
            "host": host,  # New field
            "urgency": random.choice(urgency_levels),
            "certainty": "Observed"
        }
        alerts.append(alert)
    return alerts

@app.route('/alerts', methods=['GET'])
def get_alerts():
    offset = request.args.get('offset')
    if offset:
        try:
            uuid.UUID(offset)  # Validate it's a UUID
            random.seed(offset)
        except ValueError:
            return jsonify({"error": "Invalid offset GUID"}), 400
    else:
        random.seed()  # Use system time for initial randomness

    # Generate alerts with the seeded random (1-5 for variation, but deterministic per seed)
    alerts = generate_mock_alerts(random.randint(10, 50))

    # Generate a new random next_offset GUID (not seeded, truly random each time)
    next_offset = str(uuid.uuid4())

    return jsonify({
        "type": "AlertCollection",
        "count": len(alerts),
        "next_offset": next_offset,
        "alerts": alerts,
        "updated": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on localhost:5000 or deploy to a server