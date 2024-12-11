from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dictionary representing the 3x6 grid of monitors and their IP addresses
CELL_IPS = {
    "A1": "192.168.1.11", "A2": "192.168.1.12", "A3": "192.168.1.13", "A4": "192.168.1.14", "A5": "192.168.1.15", "A6": "192.168.1.16",
    "B1": "192.168.1.21", "B2": "192.168.1.22", "B3": "192.168.1.23", "B4": "192.168.1.24", "B5": "192.168.1.25", "B6": "192.168.1.26",
    "C1": "192.168.1.31", "C2": "192.168.1.32", "C3": "192.168.1.33", "C4": "192.168.1.34", "C5": "192.168.1.35", "C6": "192.168.1.36"
}

def mdc_command(ip_address, action):
    """
    Simulate sending a command to the monitor with the given IP address.
    :param ip_address: Monitor IP address
    :param action: Action to perform ("on" or "off")
    """
    print(f"Sending '{action}' command to IP: {ip_address}")
    return f"Monitor at IP {ip_address} turned {action}"

def driver_function(selected_cells, action):
    """
    Loop through selected cells, retrieve their IPs, and send the specified command.
    :param selected_cells: List of selected cell keys (e.g., "A1")
    :param action: Action to perform ("on" or "off")
    """
    results = []
    for cell in selected_cells:
        ip_address = CELL_IPS.get(cell)
        if ip_address:
            result = mdc_command(ip_address, action)
            results.append(result)
    return results

@app.route('/')
def index():
    # Pass the CELL_IPS dictionary to the frontend
    return render_template('index.html', cell_ips=CELL_IPS)

@app.route('/apply-action', methods=['POST'])
def apply_action():
    # Get the selected cells and the action from the AJAX request
    data = request.json
    selected_cells = data.get('selectedCells', [])
    action = data.get('action', 'on')  # Default action is "on"

    # Call the driver function to apply the action
    results = driver_function(selected_cells, action)

    # Return the results to the frontend
    return jsonify({"message": f"Action '{action}' applied successfully", "results": results})

if __name__ == '__main__':
    app.run(debug=True)