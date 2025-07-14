"""
öğrenci adı soyadı: Muhammad Idham Bin Sirajuddin
öğrenci numara: 2321041351

BLM22110 Final Proje

"""

import random

#uzay aracı başlık
uzay_araci = {
    "x": 0,
    "y": 0,
    "fuel": 100,
    "kapasite": 50,
    "kaynak": 0
}

#######################galaksi temelleri#######################################
#galaksi oluştur
def Galaxy_generate():
    gezegenler = []

    for name in ['A', 'B', 'C', 'D', 'E']:
        gezegen = {
            "name": name,
            "x": random.randint(0, 9),
            "y": random.randint(1, 9),#uzay aracıyla aynı koordinat olmamak için 1 den başlar
            "resources": {'titanium':random.randint(0,20), 'aluminium': random.randint(5,20), 'ahşap':random.randint(5,20)},
            "gravity": random.randint(1, 10),
            "atmosphere": random.choice(["yaşanabilir", "zehirli", "yoğun"]),
            "visited": False
        }
        gezegenler.append(gezegen)

    karadelikler =  [{"x":random.randint(0,9), "y": random.randint(0,9)} for i in range(random.randint(2,5))]#en az 2 karadelik, en çok 5

    return gezegenler, karadelikler



#making a matrix as a galaxy map
def print_galaxy_map(gezegenler, karadelikler, uzay_araci, satir=10, sutun=10):#default matrice = 10 x 10
    
    grid = [['  ' for _ in range(sutun)] for _ in range(satir)]#matris oluştur
   
    for gezegen in gezegenler:
        grid[gezegen["y"]][gezegen["x"]] = gezegen["name"] #gezegen matrisee birleştirme
    for bh in karadelikler:
        grid[bh["y"]][bh["x"]] = 'K'#karadelik matrise birleştime

    grid[uzay_araci["y"]][uzay_araci["x"]] = '[]'#matrise uzay araci birleştirme

    print("__________ GALAXY MAP _________")
    for row in grid[::-1]:
        print(' '.join(row))
    print("_______________________________")




#print galaxy info (menu)
def galaxy_info(gezegenler, karadelikler, uzay_araci):
    
    print(f"uzay gemisin '[]' : (koordinat({uzay_araci['x']},{uzay_araci['y']}))")
    
    for gezegen in gezegenler:
        geldi = 'geldiniz' if gezegen['visited'] else ''
        print(f"[ gezegen {gezegen['name']} ] (koordinat ({ gezegen['x']},{ gezegen['y']})) {geldi}")# gezegene geldiyse 'geldi' yazılır
        
    for i, bh in enumerate(karadelikler):
        print(f"[K] kadadelik (koordinat({bh['x']},{bh['y']}))")
    print(f"yakıt: {uzay_araci['fuel']} | kargo kapasitesi: {uzay_araci['kaynak']}/{uzay_araci['kapasite']}")#{kapasite": 50,"kaynak": 0}
    print('####[  oyundan çıkmak için "exit" yazın  ]####')

 ############################oyun fonksiyon##############################################   


#taking cost to travel to the planet    
def hareket(x,y,gravity,uzay_araci,adi):#gezegenden x ve y
    if adi == 'karadeliğe':
        print(f"{adi} gidiyorsunuz...")
    else:
        print(f"gezegen {adi}'ye gidiyorsunuz...")
    x1 = x-uzay_araci['x']
    if x1 < 0:
        x1 = -x1 
    y1 = y-uzay_araci['y']
    if y1 < 0:
        y1 = -y1
    uzaklik = x1 + y1
    yakit_maliyet= uzaklik + round(gravity/2)

    if uzay_araci['fuel'] >= yakit_maliyet:
        uzay_araci['fuel'] -= yakit_maliyet
        uzay_araci['x'] = x
        uzay_araci['y'] = y
        print(f"Yakıt tüketimi :{yakit_maliyet}")
        print('kalan yakıt :', uzay_araci['fuel'] )
        return True
    else:
        print("Not enough fuel!")
        return False



#landing in a planet
def gezegene_inis(gezegen,uzay_araci):
    print(f"\n{gezegen['name']} gezegende iniş yaptınız!!")
    gezegen['visited'] = True

    print(f"\nAtmosfer: {gezegen['atmosphere']}")
    print(f"Yerçekim: {gezegen['gravity']}")

    if gezegen['atmosphere'] == "zehirli":
        uzay_araci["fuel"] -= 10
        print('[yaşam desteği için 10 yakıt kullanıldı]\n')
    elif gezegen['atmosphere'] == "yoğun": #ekstra yakıt kullanılacak eğer kirli veya zehirli otmosfere girdiyse
        uzay_araci["fuel"] -= 20
        print('[yaşam desteği için 20 yakıt kullanıldı]\n')

    resources = sum(gezegen['resources'].values())

    while True:
        print(f"kaynak: {gezegen['resources']}")
        print(f"gemi bilgisi [ yakit :{uzay_araci['fuel']}, kapasite: {uzay_araci['kapasite']}, kaynak: {uzay_araci['kaynak']}]")
        print("\n ne yapmak isterseniz?:")
        print("1. Kaynak topla")
        print("2. yakıt yenile")
        print("3. Araç geliştirme")
        print("4. başka gezegene git\n")

        secim = input("lütfen seçin (1-4): ")

        resources = sum(gezegen['resources'].values())

        if secim == '1':#kaynak toplama
            topla = min(resources, uzay_araci["kapasite"] - uzay_araci["kaynak"]) #kaynak aracını kapasitesinden daha fazlaysa sadece kapasite kadar alınır
            toplax = topla;  
            for kaynak in gezegen['resources']:
                alinan = min(toplax, gezegen['resources'][kaynak]) #gezegen[rsources] boşaltmak istiyoruz 'altın'dan başlayarak
                gezegen['resources'][kaynak] -= alinan
                toplax -= alinan
                if toplax == 0:
                    break
            uzay_araci["kaynak"] += topla
            print()
            print(f"{topla} kaynak topladınız.")
            print()
            print(f" kapasite {uzay_araci['kaynak']}/{uzay_araci['kapasite']} kaldı")
            
        elif secim == '2':#yakıt doldurma
            kullandik = min(uzay_araci["kaynak"], 10)  # x: 10 kaynaktan fazla kullanmayacak, kalan kaynak az ise kalan kaynak kullanılacak
            uzay_araci["fuel"] += round(kullandik * 2)     #
            uzay_araci["kaynak"] -= kullandik
            print(f"{kullandik} kullanarak {round(kullandik * 2)} yakıt yenilendi.\n")

        
        elif secim == '3':#kapasite geliştirme
            kullandik = min(uzay_araci["kaynak"], 20)  
            uzay_araci['kapasite'] += round(kullandik / 2)
            uzay_araci['kaynak'] -= kullandik 
            print(f"kapasite {round(kullandik / 2)}'e geliştirildi.\n")
            
        elif secim == '4':#başka gezegene git/ başlık ekrana git
            print(f"ucuş yapmak için {gezegen['gravity']} yakit kullanıldı")
            uzay_araci["fuel"] -= gezegen['gravity']
            break
        else:
            print("#############")
            print("Yanlış seçim.")
            print("#############")



#entering blackhole
def karadelik_gir(uzay_araci, gezegen):
    print("karadeliğe giriyor...")
    sonuc = random.choice(["free", "cost"])

    if sonuc == "free":
        destination = random.choice(gezegen)
        uzay_araci["x"] = destination["x"]
        uzay_araci["y"] = destination["y"]
        print(f"Karadeliğe girdiniz ve Gezegen {destination['name']}’ye hiç yakıt harcamadan ısınlandınız.")
        gezegene_inis(destination, uzay_araci)
    else:
        if uzay_araci["fuel"] >= 10 and uzay_araci["resources"] >= 5:   
            uzay_araci["fuel"] -= 10
            uzay_araci["resources"] -= 5
            destination = random.choice(gezegen)
            uzay_araci["x"] = destination["x"]
            uzay_araci["y"] = destination["y"]
            print(f"Karadeliğe girdiniz, 10 yakıt ve 50 kaynak kullanarak Gezegen {destination['name']}’ye girdiniz")
            gezegene_inis(destination, uzay_araci)
        else:
            print("##################################")
            print("Yakıtınız veya kaynağınız yetmiyor")
            print("##################################")



# Check if all planets are visited
def all_visited(gezegen):
    for p in gezegen:
        if not p["visited"]:
            return False
    return True



# ===============================
# MAIN GAME LOOP
# ===============================

gezegenler, karadelikler = Galaxy_generate()#galaksi oluştur
print("=== UZAY GEZGIN OYUNU ===")
print("Başlangıç özellikleriniz:")
print("- Yakıt: 100 birim")
print("- Kargo Kapasitesi: 50 birim")
print("Galakside 5 gezegen var. Hedefinizi seçin ve keşfe başlayın!")

while uzay_araci["fuel"] > 0 and not all_visited(gezegenler):
    print_galaxy_map(gezegenler, karadelikler, uzay_araci)#harita yazdır
    galaxy_info(gezegenler, karadelikler, uzay_araci)#bilgileri yazdır
    choice = input("\n nereye gitmek istiyorsunuz? (A-E or K): ").upper()#oyuncudan seçim al

    if choice == "EXIT":#oyundan çıkmak
        break

    # Find selected planet
    secilen_gezegen = None
    
    for n in gezegenler:
        if n["name"] == choice:
            secilen_gezegen = n
            break

    if secilen_gezegen:
        if hareket(secilen_gezegen["x"], secilen_gezegen["y"], secilen_gezegen["gravity"], uzay_araci, secilen_gezegen["name"]):
            gezegene_inis(secilen_gezegen, uzay_araci)
        continue

    # Black hole handling
    if choice == "K":
        try:#if the spacecraft doesn't have resources or fuel left, it will be error if random.choice(["free", "cost"]) came out "cost"
            if karadelikler:  # make sure list is not empty
                index = random.randint(0 , len(karadelikler)-1)
                bh = karadelikler[index]
                hareket(bh["x"], bh["y"], 0, uzay_araci, 'karadeliğe')
                karadelik_gir(uzay_araci, gezegenler)#bu fonksiyonda error dönüştürecek eğer yakıt ve kaynak harcanamazsa(yetmediyse) ["free", "cost"]
                del karadelikler[index]  # remove the used black hole
            else:
                print('hiç karadelik kalmadı')
        except:
            print("\n##########################[   hata oluştu!  ]############################")
            print("     Sanırım yakıtınız ya da kaynağınız ışınlanmanı için yetmedi....")
            print("  Yine karadeliğe girebilirsiniz ya da başka gezegene gidebilirsiniz...")
            print("#########################################################################")
        continue

    print("##############################")
    print("Invalid input. Tekrar deneyin.")
    print("##############################")

#oyun bitti
print("\nGame Over!")
print(f"Kalan Yakıt: {uzay_araci['fuel']}")
print(f"Toplanan Kaynak: {uzay_araci["kaynak"]}")

