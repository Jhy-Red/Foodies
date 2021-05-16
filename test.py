def tests_flasks_online(ip = "http://127.0.0.1:4000"):

    import requests
    try : 
        r = requests.get('{ip}/'.format(ip=ip))
        r1 = requests.get('{ip}/about'.format(ip=ip))
        r2 = requests.get('{ip}/prediction-picture'.format(ip=ip))
        r3 = requests.get('{ip}/inscription'.format(ip=ip))

        print("home :" + str(r.status_code))
        print("about : " +str(r1.status_code))
        print("prediction :" + str(r2.status_code))
        print("inscription :" +str(r3.status_code))

        if r.status_code == 200 and r1.status_code == 200 and  r2.status_code == 200 and  r3.status_code == 200 : 
            print ("Statut serveur : OK")
        else :
            print ("Statut serveur : erreur")

    except :
        print("Statut serveur : injoignable")
tests_flasks_online()