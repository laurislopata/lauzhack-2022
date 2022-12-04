import random
# Use data from https://www.reliant.com/en/residential/electricity/save-energy/tips-to-lower-your-electricity-bill/electricity-consumption-comparison.jsp 
# to compare everyday household items
def compare_electricity(estimated_watthours):
    led_bulb = 100 #Watts
    incandescent_bulb = 60 #Watts
    laptop = 65 #Watts
    desktop = 200 #Watts
    refrigerator = 600 #Watts

    led_bulb_hours = estimated_watthours / led_bulb
    incandescent_bulb_hours = estimated_watthours / incandescent_bulb
    laptop_hours = estimated_watthours / laptop
    desktop_hours = estimated_watthours / desktop
    refrigerator_hours = estimated_watthours / refrigerator

    list = []
    list.append(["LED bulb", led_bulb_hours])
    list.append(["incandescent bulb", incandescent_bulb_hours])
    list.append(["laptop", laptop_hours])
    list.append(["desktop", desktop_hours])
    list.append(["refrigerator", refrigerator_hours])

    #Pick a random entry from the list
    random_entry = random.choice(list)
    
    return "This is roughly equivalent to the electricity consumption of " + str(random_entry[1]) + " hours of a " + random_entry[0] + "."



# Use data from https://www.visualcapitalist.com/comparing-the-carbon-footprint-of-transportation-options/
# to compare different carbon footprints
def compare_carbon_footprint(estimated_carbon_footprint):
    Bus_carbon = 105 #gCO2eq
    Car_carbon = 171 #gCO2eq
    Train_carbon = 41 #gCO2eq

    bus = estimated_carbon_footprint / Bus_carbon
    car = estimated_carbon_footprint / Car_carbon
    train = estimated_carbon_footprint / Train_carbon

    list = []
    list.append(["bus", bus])
    list.append(["car", car])
    list.append(["train", train])

    #Pick a random entry from the list
    random_entry = random.choice(list)

    return "This is roughly equivalent to the carbon footprint of " + str(random_entry[1]) + " " + random_entry[0] + " rides."

    
