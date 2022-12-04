import requests
import lxml.html as lh
import math

def retrieve_consumption_data(asymptotic_runtime, min_ram, n=1000, region="Zurich"):
    runtime, hardware_config, monetary_cost = retrieve_monetary_cost(asymptotic_runtime, min_ram, n, region)

    # Retrieve the energy cost for the given region
    energy_cost = retrieve_energy_cost(runtime, hardware_config)

    # Retrieve the co2 cost for the given region
    co2_cost = retrieve_co2_cost(runtime, region)

    return monetary_cost, energy_cost, co2_cost, runtime #Runtime in hours

def retrieve_monetary_cost(asymptotic_runtime, min_ram, n, region):
    # Retrieve the server cost for the given cores, memory and storage on Exoscale platform
    # https://cloud.google.com/compute/vm-instance-
    
    exoscale_pricing_data_dict = retrieve_pricing_data_from_exoscale()
    
    selected_memory = round_up_memory(min_ram, list(exoscale_pricing_data_dict))
    hardware_configuration = exoscale_pricing_data_dict[selected_memory]

    # Match the asymptotic runtime to the correct function
    total_flops = 1 #flops
    if asymptotic_runtime == "constant":
        total_flops = constant(n)
    elif asymptotic_runtime == "log":
        total_flops = log(n)
    elif asymptotic_runtime == "linear":
        total_flops = linear(n)
    elif asymptotic_runtime == "nlogn":
        total_flops = nlog(n)
    elif asymptotic_runtime == "n2":
        total_flops = n2(n)

    # Calculate the hardware flops for an average cpu
    cpu_flops = int(hardware_configuration["cpu"]) * 1.5 * 10**9 #flops

    runtime = total_flops / cpu_flops #seconds

    # Convert runtime to hours
    runtime = runtime / 3600 #hours

    monetary_cost = runtime * hardware_configuration["price"]

    return runtime, hardware_configuration, monetary_cost

def round_up_memory(min_ram, memory_list):
    for memory in memory_list:
        mem = float(memory)
        if mem > min_ram:
            return mem
    return float(memory_list[-1])

def retrieve_energy_cost(runtime, hardware_config): #runtime in hours

    #From https://smarterbusiness.co.uk/blogs/how-much-energy-do-my-appliances-use-infographic/#:~:text=A%20desktop%20PC%20typically%20uses,the%20equivalent%20of%200.1%20kWh.
    #Average desktop PC uses 0.1 kWh per hour

    Average_wattage = 0.1 #kWh

    simple_wattage_model = Average_wattage * (1.3 * int(hardware_config["cpu"])) #Simplification, access to API would allow for accurate energy cost tracking

    watthours_used = simple_wattage_model * runtime

    return watthours_used

def retrieve_co2_cost(runtime, region): #runtime in hours
    google_carbon_data_dict = retrieve_carbon_data_from_google()

    region_specific_data = google_carbon_data_dict[region]

    # Retrieve the co2 cost for the given region
    co2_cost = runtime * int(region_specific_data["carbon_intensity"]) #gCO2eq
    
    return co2_cost

# Costs from https://www.exoscale.com/calculator/

# Costs from Google Cloud Platform: https://cloud.google.com/products/calculator

# Electricity costs: https://app.electricitymaps.com/map

# Cumulator: https://pypi.org/project/cumulator/

# Our world in Energy: https://ourworldindata.org/energy
def retrieve_pricing_data_from_exoscale():
    url = "https://www.exoscale.com/pricing/"
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    col = []
    i = 0

    table_dict = {}

    #Add all table entries to the dict
    for t in range(1, 11):
        T = tr_elements[t]
        for j in T.iterchildren():
            print(j.text_content())

        dict_entry = {}

        #Append exoscale's T to the dict_entry
        dict_entry["type"] = T[0].text_content()
        ram_exo = T[1].text_content()
        ram_val = 0.5
        if ram_exo == "512 MB":
            dict_entry["ram"] = 0.5
            ram_val = 0.5
        if ram_exo == "1 GB":
            dict_entry["ram"] = 1
            ram_val = 1
        if ram_exo == "2 GB":
            dict_entry["ram"] = 2
            ram_val = 2
        if ram_exo == "4 GB":
            dict_entry["ram"] = 4
            ram_val = 4
        if ram_exo == "8 GB":
            dict_entry["ram"] = 8
            ram_val = 8
        if ram_exo == "16 GB":
            dict_entry["ram"] = 16
            ram_val = 16
        if ram_exo == "32 GB":
            dict_entry["ram"] = 32
            ram_val = 32
        if ram_exo == "64 GB":
            dict_entry["ram"] = 64
            ram_val = 64
        if ram_exo == "128 GB":
            dict_entry["ram"] = 128
            ram_val = 128
        if ram_exo == "225GB":
            dict_entry["ram"] = 225
            ram_val = 225

        
        cpu_exo = T[2].text_content()
        if cpu_exo == "1 Cores":
            dict_entry["cpu"] = 1
        if cpu_exo == "2 Cores":
            dict_entry["cpu"] = 2
        if cpu_exo == "4 Cores":
            dict_entry["cpu"] = 4
        if cpu_exo == "8 Cores":
            dict_entry["cpu"] = 8
        if cpu_exo == "12 Cores":
            dict_entry["cpu"] = 12
        if cpu_exo == "16 Cores":
            dict_entry["cpu"] = 16
        if cpu_exo == "24 Cores":
            dict_entry["cpu"] = 24
        
        dict_entry["storage"] = T[3].text_content()

        #Hard-code the pricing information (as cannot be scraped from site directly)
        if dict_entry["type"] == "Micro":
            dict_entry["price"] = 0.00729000
        elif dict_entry["type"] == "Tiny":
            dict_entry["price"] = 0.01458000
        elif dict_entry["type"] == "Small":
            dict_entry["price"] = 0.02333000
        elif dict_entry["type"] == "Medium":
            dict_entry["price"] = 0.04666000
        elif dict_entry["type"] == "Large":
            dict_entry["price"] = 0.09333000
        elif dict_entry["type"] == "Extra-Large":
            dict_entry["price"] = 0.18667000
        elif dict_entry["type"] == "Huge":
            dict_entry["price"] = 0.37333000
        elif dict_entry["type"] == "Mega":
            dict_entry["price"] = 0.74667000
        elif dict_entry["type"] == "Titan":
            dict_entry["price"] = 1.49333000
        elif dict_entry["type"] == "Jumbo":
            dict_entry["price"] = 2.24000000

        #Add the dict_entry to the table_dict
        table_dict[ram_val] = dict_entry
        i += 1
    
    print(table_dict)
    return table_dict


# Retrieve the carbon data from the devsite-table-wrapper table on the following page: https://cloud.google.com/sustainability/region-carbon
# https://stackoverflow.com/questions/50831499/how-to-scrape-table-data-from-a-website-using-python
def retrieve_carbon_data_from_google():
    # Retrieve the carbon data from the devsite-table-wrapper table on the following page: https://cloud.google.com/sustainability/region-carbon
    # https://stackoverflow.com/questions/50831499/how-to-scrape-table-data-from-a-website-using-python
    url = "https://cloud.google.com/sustainability/region-carbon"
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    col = []
    i = 0
    
    table_dict = {}

    # Add all table entries to the dict
    for t in range(1, len(tr_elements)):
        T = tr_elements[t]

        dict_entry = {}

        #Append an entry to the dict_entry
        dict_entry["region"] = T[0].text_content()
        dict_entry["location"] = T[1].text_content()
        dict_entry["cfe"] = T[2].text_content()
        dict_entry["carbon_intensity"] = int(T[3].text_content())

        #Add the dict_entry to the table_dict
        table_dict[T[1].text_content()] = dict_entry
        i += 1
    
    return table_dict


# "Constant"
# "Log(n)"
# "Linear"
# "Nlog(n)"
# "N^2"

def constant(n):
    return 1

def log(n):
    return math.log(n)

def linear(n):
    return n

def nlog(n):
    return n * math.log(n)

def n2(n):
    return n * n