import pycountry
import os
import shutil

countries = [o for o in os.listdir(os.getcwd()) 
            if os.path.isdir(os.path.join(os.getcwd(),o))]


use_countries = {
    'zh_TW': 'TW',
    'pt_BR': 'BR',
    'ro': 'RO',
    'lt': 'LT',
    'cs': 'CZ',
    'es': 'ES',
    'kl': 'MY',
    'sk': 'SK',
    'el': 'GR',
    'lv': "LV"
}

# eu = basque (eus iso)

for country in countries:
    if country == "en":
        continue

    if country in use_countries.keys():
        code = use_countries.get(country)
        iso = pycountry.countries.get(alpha_2=code).alpha_3
    else:
        try:
            iso = pycountry.languages.get(alpha_2=country).alpha_3.upper()
        except:
            print "ERROR GETTING ISO FOR %s" % country

    path = os.getcwd() + "/" + country + "/csv/%s-formatted.csv" % country
    from_file = open(path) 
    line = from_file.readline()

    line = line.replace("<ISO-code>", iso)

    to_file = open(path, mode="w")
    to_file.write(line)
    shutil.copyfileobj(from_file, to_file)
    print "Finished setting ISO code for country %s" % iso