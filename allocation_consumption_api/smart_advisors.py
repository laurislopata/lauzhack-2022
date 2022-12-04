import requests

electricity_map_api_key = "uCSbdOwGdyniZQQ3ESAMU1SVT4x5fTH3"

#TODO: Implement a smarter hardware algorithm by using data from EPFL data centers
#Based on the runtime, tell the user which hardware configuration to use
def smart_hardware_allocator(runtime): #runtime in hours
    hardware_configurations = {
        "latest_hardware": {"type": "Latest hardware", "description": "more efficient than older hardware, thus it is more sustainable to run intense workloads", "name": "Nvidia Tesla V300", "cpu": 4, "memory": 8, "storage": 100, "efficiency": 0.1}, 
        "old_hardware": {"type": "Old hardware", "description": "less efficient relative to latest hardware, but it is more sustainable to re-purpose this hardware to run small workloads", "name": "Nvidia Tesla V100", "cpu": 2, "memory": 4, "storage": 50, "efficiency": 0.06}
    }

    #Convert runtime to seconds
    runtime = runtime * 3600
    
    # If the runtime is less than 1 second, use the old hardware
    if runtime < 1:
        best_config = hardware_configurations["old_hardware"]
        return "The best configuration to use is the " + best_config["name"] + " since you have a small workload (runtime is " + str(runtime) +  " seconds). This hardware is " + best_config["description"] + "."
    # If the runtime is more than 1 second, use the latest hardware
    else:
        best_config = hardware_configurations["latest_hardware"]
        return "The best configuration to use is the " + best_config["name"] + " since you have an intense workload (runtime is " + str(runtime) +  " seconds). This hardware is " + best_config["description"] + "."



#Identify the server from electricity maps with the lowest carbon intensity
def smart_location_allocator():

    base_url = "https://api-access.electricitymaps.com/tw0j3yl62nfpdjv4/"

    european_zones_carbon_data = {}

    #List of european countries zone keys
    europe_zone_keys = ["AT", "BE", "BG", "CH", "CY", "CZ", "DE", "DK", "EE", "ES", "FI", "FR", "GB", "GR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "NO", "PL", "PT", "RO", "SE", "SI", "SK"]
    
    for zone in europe_zone_keys:
        #print("Zone: ", zone)
        zone_url = base_url + "/carbon-intensity/latest?zone=" + zone
        zone_data = requests.get(zone_url, headers={"X-BLOBR-KEY": electricity_map_api_key}).json()

        #Check if zone_data contains "carbonIntensity" key
        if "carbonIntensity" in zone_data:
            european_zones_carbon_data[zone_data["carbonIntensity"]] = zone_data
    
    #print(list(european_zones_carbon_data))

    #Find the zone with the lowest carbon intensity
    min_zone_carbon_intensity = 1000

    for key in list(european_zones_carbon_data):
        int_key = int(key)
        if int_key < min_zone_carbon_intensity:
            min_zone_carbon_intensity = int_key
        
    #Retrieve the current lowest carbon intensity zone
    optimal_location = european_zones_carbon_data[min_zone_carbon_intensity]

    #Create a mapping between zone keys and country names
    zone_key_to_country_name = {
        "AT": "Austria",
        "BE": "Belgium",
        "BG": "Bulgaria",
        "CH": "Switzerland",
        "CY": "Cyprus",
        "CZ": "Czechia",
        "DE": "Germany",
        "DK": "Denmark",
        "EE": "Estonia",
        "ES": "Spain",
        "FI": "Finland",
        "FR": "France",
        "GB": "United Kingdom",
        "GR": "Greece",
        "HR": "Croatia",
        "HU": "Hungary",
        "IE": "Ireland",
        "IT": "Italy",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "LV": "Latvia",
        "MT": "Malta",
        "NL": "Netherlands",
        "NO": "Norway",
        "PL": "Poland",
        "PT": "Portugal",
        "RO": "Romania",
        "SE": "Sweden",
        "SI": "Slovenia",
        "SK": "Slovakia"
    }

    recommendation_string = "The optimal location to run your workload at the current time is " + zone_key_to_country_name[optimal_location["zone"]] + " since it has the lowest carbon intensity, with a carbon intensity of " + str(optimal_location["carbonIntensity"]) + " gCO2eq/kWh."

    return recommendation_string