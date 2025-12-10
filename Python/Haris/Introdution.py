name : str = "Haris"
full_name : str = "Hariswandi Maulana"
age : int = 17
adress = ["Jl.Kandang Aur" ,"Simpang Rumbio" , "Kota Solok", "Sumatra Barat", "Indonesia"]
baris = 0

def Intro() :
    global baris
    print("\n", "="*20,"\n=====Perkenalan=====\n", "="*20)
    print(f"Nama : {name} \nNama Panjang : {full_name}\nUmur : {age}\nAlamat :")
    for adres in adress:
        if baris == 2:
            print("")
            baris = 0
        print(adres,end=", ")
        baris += 1
    print("\n","="*20,"\n=====Perkenalan=====\n","="*20)


Intro()