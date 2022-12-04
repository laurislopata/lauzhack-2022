from flask import Flask, request
import consumption
import consumption_comparison
import smart_advisors
import socket
import jsonify
from flask_cors import CORS, cross_origin
import prediction
import javalang
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import regex as re
clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
import pickle
filename = 'finalized_model.sav'

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))


if prediction == [1]:
    print('constant')
elif prediction == [2]:
    print('logn')
elif prediction == [3]:
    print('linear')
elif prediction == [4]:
    print('nlogn')
elif prediction == [5]:
    print('n2')
#Create a flask app
app = Flask(__name__)
cors = CORS(app)
#Create a route
@app.route('/')
def index():
    return 'Hello World test 2'

dB = {}

def remove_comments(string):
    pattern = r"(\".?\"|\'.?\')|(/\.?\/|//[^\r\n]$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

# pickle.dump(model, open(filename, 'wb'))
def ast_parse(java_code):
    try:
        tree = javalang.parse.parse(java_code)
        return tree
    except:
        return None
# some time later...
def graph_parse(tree, vector):
    if len(tree.children) > 0:
        for child in tree.children:
            if child:
                for li in child:
                    if li.__class__.__name__ == 'MethodDeclaration':
                        vector["MethodDeclaration"] = vector["MethodDeclaration"] + 1
                    if li.__class__.__name__ == 'IfStatement':
                        vector["IfStatement"] = vector["IfStatement"] + 1
                    if li.__class__.__name__ == 'ForStatement':
                        vector["ForStatement"] = vector["ForStatement"] + 1
                    if li.__class__.__name__ == 'ClassDeclaration':
                        vector["ClassDeclaration"] = vector["ClassDeclaration"] + 1
                    if li.__class__.__name__ == 'WhileStatement':
                        vector["WhileStatement"] = vector["WhileStatement"] + 1
                    if li.__class__.__name__ == 'StatementExpression':
                        vector["StatementExpression"] = vector["StatementExpression"] + 1
                    if li.__class__.__name__ == 'LocalVariableDeclaration':
                        vector["LocalVariableDeclaration"] = vector["LocalVariableDeclaration"] + 1
                    if hasattr(li, 'body'):
                        for node in li.body: 
                            if (not node is None) and (issubclass(type(node), javalang.tree.Statement) or issubclass(type(node), javalang.tree.Expression) or issubclass(type(node), javalang.tree.Declaration)):    
                                left_loop = False
                                if node.__class__.__name__ == 'MethodDeclaration':
                                    vector["MethodDeclaration"] = vector["MethodDeclaration"] + 1
                                if node.__class__.__name__ == 'IfStatement':
                                    vector["IfStatement"] = vector["IfStatement"] + 1
                                if node.__class__.__name__ == 'ForStatement':
                                    vector["ForStatement"] = vector["ForStatement"] + 1
                                    vector["CurrentNestingLevel"] = vector["CurrentNestingLevel"] + 1
                                    if vector["CurrentNestingLevel"] > vector["MaxNestingLevel"]:
                                        vector["MaxNestingLevel"] = vector["CurrentNestingLevel"]
                                    left_loop = True
                                if node.__class__.__name__ == 'ClassDeclaration':
                                    vector["ClassDeclaration"] = vector["ClassDeclaration"] + 1
                                if node.__class__.__name__ == 'WhileStatement':
                                    vector["WhileStatement"] = vector["WhileStatement"] + 1
                                    vector["CurrentNestingLevel"] = vector["CurrentNestingLevel"] + 1
                                    if vector["CurrentNestingLevel"] > vector["MaxNestingLevel"]:
                                        vector["MaxNestingLevel"] = vector["CurrentNestingLevel"]
                                    left_loop = True
                                if node.__class__.__name__ == 'StatementExpression':
                                    vector["StatementExpression"] = vector["StatementExpression"] + 1
                                
                                graph_parse(node, vector)
                                if left_loop: 
                                    vector["CurrentNestingLevel"] = vector["CurrentNestingLevel"] - 1 
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
    
#Create a post route to receive string
@app.route('/predict_code', methods=['POST'])
@cross_origin()
def predict_code():
    #Parse the request body
    data = request.get_json()
    print(data["code"])
    java_code = data["code"]
    nw_code = remove_comments(java_code)

    ast_code = ast_parse(nw_code)
    vect = {"MethodDeclaration": 0, "IfStatement": 0, "ForStatement": 0, 
    "ClassDeclaration": 0, "WhileStatement": 0, "StatementExpression": 0, 
    "LocalVariableDeclaration": 0, "MaxNestingLevel": 0, "CurrentNestingLevel": 0}
    if ast_code is not None:
        graph_code = graph_parse(ast_code, vect)

    x = list(vect.values())
    x.extend([0,0,0,0,0])
    print(x)

    loaded_model = pickle.load(open(filename, 'rb'))

    prediction = loaded_model.predict([x])
    ans = ""
    if prediction == [1]:
        ans = 'constant'
    elif prediction == [2]:
        ans = 'logn'
    elif prediction == [3]:
        ans = 'linear'
    elif prediction == [4]:
        ans = 'nlogn'
    elif prediction == [5]:
        ans = 'n2'
    print(ans)
    return ans





#Create a post route
@app.route('/sustainable_models', methods=['POST'])
@cross_origin()
def post():
    
    monetary_cost, electricity_cost, carbon_cost, electricity_comparison, carbon_comparison, hardware_recommendation, server_region_recommendation = compute_model(request)
    
    #Generate a uid for the request
    uid = socket.gethostname() + str(len(dB))

    #Store the results in a dictionary
    response = {
        "uid": uid,
        "monetary_cost": monetary_cost, 
        "electricity_cost": electricity_cost, 
        "electricity_comparison": electricity_comparison, 
        "carbon_cost": carbon_cost, 
        "carbon_comparison": carbon_comparison,
        "hardware_recommendation": hardware_recommendation,
        "server_region_recommendation": server_region_recommendation
    }

    dB[uid] = response

    return response

#Create a post route
@app.route('/sustainable_models_recompute/{string:uid}', methods=['POST'])
@cross_origin()
def post_recompute(uid):
    monetary_cost, electricity_cost, carbon_cost, electricity_comparison, carbon_comparison, hardware_recommendation, server_region_recommendation = compute_model(request)

    #Store the results in a dictionary
    response = {
        "uid": uid,
        "monetary_cost": monetary_cost, 
        "electricity_cost": electricity_cost, 
        "electricity_comparison": electricity_comparison, 
        "carbon_cost": carbon_cost, 
        "carbon_comparison": carbon_comparison,
        "hardware_recommendation": hardware_recommendation,
        "server_region_recommendation": server_region_recommendation
    }

    dB[uid] = response

    return response

#Create a get route to display all dB entries
@app.route('/sustainable_models', methods=['GET'])
@cross_origin()
def get():
    print(dB)
    return dB

#Create a get route to display all dB entries
@app.route('/sustainable_models/{string:uid}', methods=['GET'])
@cross_origin()
def get_json(uid):
    return jsonify(dB[uid])

### DEBUGGING ###
#Create a get route to retrieve google cloud co2 data
@app.route('/get_google_carbon', methods=['GET'])
@cross_origin()
def get_google_carbon_data():
    #Call the retrieve_server_cost function from consumption.py
    #By default, assume the input size is n=1000
    google_dict = consumption.retrieve_carbon_data_from_google()
    print(google_dict)
    
    return 'Got'

@app.route('/get_optimal_hardware', methods=['GET'])
@cross_origin()
def get_best_hardware():
    #Parse the request body
    data = request.get_json()

    electricity_map_data = smart_advisors.smart_hardware_allocator(data["runtime"])
    print(electricity_map_data)
    
    return 'Got'

@app.route('/get_electricity_map_data', methods=['GET'])
@cross_origin()
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