from flask import Flask, request, jsonify, Blueprint
import socket

# Define the Blueprint for tool2
tool2 = Blueprint('tool2', __name__)

# Manually add CORS headers for tool2
@tool2.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all domains (you can specify specific domains if needed)
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def scan_ports(ip, ports):
    results = {}
    for port in ports:
        results[port] = "Open" if scan_port(ip, port) else "Closed"
    return results

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            return True
    except:
        return False

@tool2.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    ip = data.get("ip")
    ports = data.get("ports", [])
    try:
        ports = list(map(int, ports))
    except ValueError:
        return jsonify({"error": "Invalid ports input"}), 400
    results = scan_ports(ip, ports)
    return jsonify(results)

# Don't use `app.run` here in a blueprint; it's managed by the main app.
