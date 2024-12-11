from flask import Flask, render_template, request, jsonify
import subprocess
from samsung_mdc import MDC


app = Flask(__name__)

# Dictionary representing the 3x6 grid of monitors and their IP addresses
CELL_IPS = {
    "A1": "192.168.0.11", "A2": "192.168.0.12", "A3": "192.168.0.13", "A4": "192.168.0.14", "A5": "192.168.0.15", "A6": "192.168.0.16",
    "B1": "192.168.0.21", "B2": "192.168.0.22", "B3": "192.168.0.23", "B4": "192.168.0.24", "B5": "192.168.0.25", "B6": "192.168.0.26",
    "C1": "192.168.0.31", "C2": "192.168.0.32", "C3": "192.168.0.33", "C4": "192.168.0.34", "C5": "192.168.0.35", "C6": "192.168.0.36"
}
# CELL_IPS = {
#     "A1": "192.168.1.11", "A2": "192.168.1.12", "A3": "192.168.1.13", "A4": "192.168.1.14", "A5": "192.168.1.15", "A6": "192.168.1.16",
#     "B1": "192.168.1.21", "B2": "192.168.1.22", "B3": "192.168.1.23", "B4": "192.168.1.24", "B5": "192.168.1.25", "B6": "192.168.1.26",
#     "C1": "192.168.1.31", "C2": "192.168.1.32", "C3": "192.168.1.33", "C4": "192.168.1.34", "C5": "192.168.1.35", "C6": "192.168.1.36"
# }
def mdc_power(ip_address, power_state):
    """
    Controls the power state of a monitor using the samsung-mdc CLI tool.
    :param ip_address: IP address of the monitor (e.g., "192.168.0.10").
    :param power_state: Power state ("ON", "OFF", "REBOOT").
    :return: Command result or error message.
    """
    target = f"0@{ip_address}"  # Assuming display ID is 0
    try:
        # Execute the samsung-mdc command for the power state
        result = subprocess.run(
            ["samsung-mdc", target, "power", power_state],
            capture_output=True,
            text=True
        )
        # Check if the command was successful
        if result.returncode == 0:
            return f"Success: {result.stdout.strip()}"
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: Failed to execute command for {ip_address} - {str(e)}"

@app.route('/')
def index():
    # Pass the CELL_IPS dictionary to the frontend
    return render_template('index.html', cell_ips=CELL_IPS)

@app.route('/apply-action', methods=['POST'])
def apply_action():
    # Get the selected cells and the action from the AJAX request
    data = request.json
    selected_cells = data.get('selectedCells', [])
    power_state = data.get('action', 'ON')  # Default to "ON"

    # Loop through selected cells and apply the power command
    results = []
    for cell in selected_cells:
        ip_address = CELL_IPS.get(cell)
        if ip_address:
            result = mdc_power(ip_address, power_state)
            results.append(f"{cell} ({ip_address}): {result}")

    # Return results to the frontend
    return jsonify({"message": f"Power action '{power_state}' applied successfully", "results": results})

if __name__ == '__main__':
    app.run(debug=True)