"""
student`s name : Muhammad Idham
BLM22110 Final Project
"""

import random

#spacecraft initial
spacecraft = {
    "x": 0,
    "y": 0,
    "fuel": 100,
    "capacity": 50,
    "resourse": 0
}

####################### GALAXY BASICS #######################################
#Create Galaxy
def Galaxy_generate():
    planets = []

    for name in ['A', 'B', 'C', 'D', 'E']:
        planet = {
            "name": name,
            "x": random.randint(0, 9),
            "y": random.randint(1, 9),
            "resources": {'titanium':random.randint(0,20), 'aluminium': random.randint(5,20), 'wood':random.randint(5,20)},
            "gravity": random.randint(1, 10),
            "atmosphere": random.choice(["livable", "toxic", "intense"]),
            "visited": False
        }
        planets.append(planet)

    blackhole =  [{"x":random.randint(0,9), "y": random.randint(0,9)} for i in range(random.randint(2,5))]#en az 2 karadelik, en çok 5

    return planets, blackhole



#making a matrix as a galaxy map
def print_galaxy_map(planets, blackhole, spacecraft, rows=10, collumn=10):#default matrice = 10 x 10
    
    grid = [['  ' for _ in range(rows)] for _ in range(collumn)]#do a matrix
   
    for planet in planets:
        grid[planet["y"]][planet["x"]] = planet["name"] #merge the planet into the matrice
    for bh in blackhole:
        grid[bh["y"]][bh["x"]] = 'K'#merge the blackhole into the matrice

    grid[spacecraft["y"]][spacecraft["x"]] = '[]'#merge spacecraft into the matrice

    print("__________ GALAXY MAP _________")
    for row in grid[::-1]:
        print(' '.join(row))
    print("_______________________________")



#print galaxy info (menu)
def galaxy_info(planets , blackhole, spacecraft):
    
    print(f"your spacecraft is '[]' : (coordinate ({spacecraft['x']},{spacecraft['y']}))")
    
    for planet in planets :
        arrived = 'visited' if planet['visited'] else ''
        print(f"[ planet {planet['name']} ] (coordinate ({ planet['x']},{ planet['y']})) {arrived}")#if you visited it will write 'visited'
        
    for i, bh in enumerate(blackhole):
        print(f"[K] blackhole (coordinate({bh['x']},{bh['y']}))")
    print(f"fuel: {spacecraft['fuel']} | kargo capacity: {spacecraft['resourse']}/{spacecraft['capacity']}")
    print('####[  to end the game write "exit"  ]####')

 ############################ game functions ##############################################   


#taking cost to travel to the planet    
def move(x,y,gravity,spacecraft,adi):#gezegenden x ve y
    if adi == 'blackhole':
        print(f"entering {adi} ...")
    else:
        print(f"you ae travelling to planet{adi}..")
    x1 = x-spacecraft['x']
    if x1 < 0:
        x1 = -x1 
    y1 = y-spacecraft['y']
    if y1 < 0:
        y1 = -y1
    distance = x1 + y1
    Fuel_consumption= distance + round(gravity/2)

    if spacecraft['fuel'] >= Fuel_consumption:
        spacecraft['fuel'] -= Fuel_consumption
        spacecraft['x'] = x
        spacecraft['y'] = y
        print(f"fuel consumption :{Fuel_consumption}")
        print('fuel left :', spacecraft['fuel'] )
        return True
    else:
        print("Not enough fuel!")
        return False



#landing in a planet
def land(planet,spacecraft):
    print(f"\n you arrived to planet {planet['name']} !!")
    planet['visited'] = True

    print(f"\nAtmosfer: {planet['atmosphere']}")
    print(f"gravity: {planet['gravity']}")

    if planet['atmosphere'] == "toxic":
        spacecraft["fuel"] -= 10
        print('[used 10 fuel for life suppert]\n')
    elif planet['atmosphere'] == "intense": 
        spacecraft["fuel"] -= 20
        print('[used 20 fuel for life support]\n')

    resources = sum(planet['resources'].values())

    while True:
        print(f"resource: {planet['resources']}")
        print(f"spacecraft info [ fuel :{spacecraft['fuel']}, capacity: {spacecraft['capacity']}, resources: {spacecraft['resourse']}]")
        print("\n what you want to do?:")
        print("1. take resources")
        print("2. refuel")
        print("3. upgrade spaceship")
        print("4. go to other planet\n")

        choices = input("please choose (1-4): ")

        resources = sum(planet['resources'].values())

        if choices == '1':#ake resources
            taken = min(resources, spacecraft["capacity"] - spacecraft["resourse"]) #only take resource base from the capacity
            takenx = taken;  
            for kaynak in planet['resources']:#kaynak = resources
                taken = min(takenx, planet['resources'][kaynak]) #start emptying resource start from aluminium
                planet['resources'][kaynak] -= taken
                takenx -= taken
                if takenx == 0:
                    break
            spacecraft["resourse"] += taken
            print()
            print(f" you have taken {taken} resources .")
            print()
            print(f" capacity is {spacecraft['resourse']}/{spacecraft['capacity']} left")
            
        elif choices == '2':#refuel
            taken = min(spacecraft["resourse"], 10)  # x: will not use more than 10 resources, if less than 10, it will use all resources
            spacecraft["fuel"] += round(taken * 2)     #
            spacecraft["resourse"] -= taken
            print(f"used {taken} to refuel {round(taken * 2)} fuel.\n")

        
        elif choices == '3':#upgrae capacity
            taken = min(spacecraft["resourse"], 20)  
            spacecraft['capacity'] += round(taken / 2)
            spacecraft['resourse'] -= taken
            print(f"capacity has been upgraded by {round(taken / 2)}.\n")
            
        elif choices == '4':#go to other planet (go to main screen)
            print(f"to launch your rocket you need {planet['gravity']} fuel, confirm?\n")
            confirm = input('yes or no?')
            if confirm == 'yes':
                spacecraft["fuel"] -= planet['gravity']
                break
            if confirm == 'no':
                print("returning to planet")
            else:
                print('invalid input')
                print("returning to planet")
        else:
            print("#############")
            print("invalid inout.")
            print("#############")



#entering blackhole
def enter_blackhole(spacecraft, planet):
    print("entering blackhole...")
    pity = random.choice(["free", "cost"])

    if pity == "free":
        destination = random.choice(planet)
        spacecraft["x"] = destination["x"]
        spacecraft["y"] = destination["y"]
        print(f"You entered planet {destination['name']} safely without any extra cost.")
        land(destination, spacecraft)
    else:
        if spacecraft["fuel"] >= 10 and spacecraft["resources"] >= 5:   
            spacecraft["fuel"] -= 10
            spacecraft["resources"] -= 5
            destination = random.choice(planet)
            spacecraft["x"] = destination["x"]
            spacecraft["y"] = destination["y"]
            print(f"you entered  planet {destination['name']}\n but your spaceship are damaged by spacejunk in the blachole \n(fuel -10, resources -5)")
            land(destination, spacecraft)
        else: 
            print("##################################")
            print("fuel or resources are not enough to enter the blackhole.")
            print("##################################")



# Check if all planets are visited
def all_visited(planet):
    for p in planet:
        if not p["visited"]:
            return False
    return True



# ===============================
# MAIN GAME LOOP
# ===============================

planets , blackhole = Galaxy_generate()#create galaxy
print("=== space exploration gme ===")
print(" starting resources:")
print("- fuel : 100 ")
print("- cargo capacity: 50")
print("in this galaxy, there is 5 planets. choose your way and start your exploration!!")

while spacecraft["fuel"] > 0 and not all_visited(planets ):
    print_galaxy_map(planets , blackhole, spacecraft)#print galaxy map
    galaxy_info(planets , blackhole, spacecraft)#print galaxy info
    choice = input("\n where do you wan to go? (A-E or K): ").upper()#take choice from player

    if choice == "EXIT":#exit from game
        break

    # Find selected planet
    choosen_planet = None
    
    for n in planets :
        if n["name"] == choice:
            choosen_planet = n
            break

    if choosen_planet:
        if move(choosen_planet["x"], choosen_planet["y"], choosen_planet["gravity"], spacecraft, choosen_planet["name"]):
            land(choosen_planet, spacecraft)
        continue

    # Black hole landling
    if choice == "K":
        try:#if the spacecraft doesn't have resources or fuel left, it will be error if random.choice(["free", "cost"]) came out "cost"
            if blackhole:  # make sure list is not empty
                index = random.randint(0 , len(blackhole)-1)
                bh = blackhole[index]
                move(bh["x"], bh["y"], 0, spacecraft, 'blackhole')
                enter_blackhole(spacecraft, planets )#this function will return error if cannot use fuel and resources from rand.choice ["free", "cost"]
                del blackhole[index]  # remove the used black hole
            else:
                print('no blackholes left in the galaxy.')
        except:
            print("\n##########################[    error!      ]############################")
            print("    Maybe your resources are not enough to enter the blackhole....")
            print("  you can try to enter other blackhole or you can go to other planet...")
            print("#########################################################################")
        continue

    print("##############################")
    print("Invalid input. please try again.")
    print("##############################")

#oyun bitti
print("\nGame Over!")
print(f"Fuel left: {spacecraft['fuel']}")
print(f"Taken resources: {spacecraft["resourse"]}")

