from flask import Flask, request
import consumption
import consumption_comparison
import smart_advisors
import socket

#Create a flask app
app = Flask(__name__)

#Create a route
@app.route('/')
def index():
    return 'Hello World test 2'

dB = {}

def compute_model(request):
    #Parse the request body
    data = request.get_json()
    print(data)

    runtime_complexity = data["runtime_complexity"]
    memory = data["memory"] #Memory in GB
    n = data["n"]
    region = data["region"]

    #Call the retrieve_server_cost function from consumption.py
    #By default, assume the input size is n=1000
    monetary_cost, electricity_cost, carbon_cost, runtime = consumption.retrieve_consumption_data(runtime_complexity, memory, n, region)
    
    electricity_comparison = consumption_comparison.compare_electricity(electricity_cost)
    carbon_comparison = consumption_comparison.compare_carbon_footprint(carbon_cost)

    hardware_recommendation = smart_advisors.smart_hardware_allocator(runtime)
    server_region_recommendation = smart_advisors.smart_location_allocator()

    print("Monetary_cost: ", monetary_cost, "CHF")

    print()
    print("Electricity_cost: ", electricity_cost, "kWh")
    print("Electricity_comparison:", electricity_comparison)

    print()
    print("Carbon_cost: ", carbon_cost, " gCo2eq")
    print("Carbon_comparison:", carbon_comparison)

    print()
    print("Hardware recommendation: ", hardware_recommendation)

    print()
    print("Server region recommendation: ", server_region_recommendation)

    return monetary_cost, electricity_cost, carbon_cost, electricity_comparison, carbon_comparison, hardware_recommendation, server_region_recommendation
    

#Create a post route
@app.route('/sustainable_models', methods=['POST'])
def post():
    
    monetary_cost, electricity_cost, carbon_cost, electricity_comparison, carbon_comparison, hardware_recommendation, server_region_recommendation = compute_model(request)
    
    #Generate a uid for the request
    uid = socket.gethostname() + str(len(dB))

    #Store the results in a dictionary
    dB[uid] = {
        "uid": uid,
        "monetary_cost": monetary_cost, 
        "electricity_cost": electricity_cost, 
        "electricity_comparison": electricity_comparison, 
        "carbon_cost": carbon_cost, 
        "carbon_comparison": carbon_comparison,
        "hardware_recommendation": hardware_recommendation,
        "server_region_recommendation": server_region_recommendation
    }

    return 'Posted'

#Create a post route
@app.route('/sustainable_models_recompute/{string:uid}', methods=['POST'])
def post_recompute(uid):
    monetary_cost, electricity_cost, carbon_cost, electricity_comparison, carbon_comparison, hardware_recommendation, server_region_recommendation = compute_model(request)

    #Store the results in a dictionary
    dB[uid] = {
        "uid": uid,
        "monetary_cost": monetary_cost, 
        "electricity_cost": electricity_cost, 
        "electricity_comparison": electricity_comparison, 
        "carbon_cost": carbon_cost, 
        "carbon_comparison": carbon_comparison,
        "hardware_recommendation": hardware_recommendation,
        "server_region_recommendation": server_region_recommendation
    }

    return 'Recomputed'

#Create a get route to display all dB entries
@app.route('/sustainable_models', methods=['GET'])
def get():
    print(dB)
    return dB

### DEBUGGING ###
#Create a get route to retrieve google cloud co2 data
@app.route('/get_google_carbon', methods=['GET'])
def get_google_carbon_data():
    #Call the retrieve_server_cost function from consumption.py
    #By default, assume the input size is n=1000
    google_dict = consumption.retrieve_carbon_data_from_google()
    print(google_dict)
    
    return 'Got'

@app.route('/get_optimal_hardware', methods=['GET'])
def get_best_hardware():
    #Parse the request body
    data = request.get_json()

    electricity_map_data = smart_advisors.smart_hardware_allocator(data["runtime"])
    print(electricity_map_data)
    
    return 'Got'

@app.route('/get_electricity_map_data', methods=['GET'])
def get_electricity_map_data():
    #Parse the request body
    data = request.get_json()

    #Call the retrieve_server_cost function from consumption.py
    #By default, assume the input size is n=1000
    electricity_map_data = smart_advisors.smart_location_allocator(data["region"])
    
    return 'Got'

#Run the app
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port, debug=True)