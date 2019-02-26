import json
import requests


LOCATION = "select * from Location"
SUPPLY_LINES = "select * from Feeder where LocationID=:LocationID"
FARMER_COUNT = "select * from Farmer , Feeder, Location where Farmer.FeederID = Feeder.FeederID and Feeder.LocationID = Location.LocationID and Location.LocationID =:LocationID"
COUNT_SUPPLY_LINES = "select count(FeederID) from Feeder , Location where Feeder.LocationID = Location.LocationID and Location.LocationID =:LocationID"
FARMER_TABLE_Q = "select * from Farmer, Feeder, Location, Crop where Crop.FarmerID = Farmer.FarmerID and Farmer.FeederID  = Feeder.FeederID and Feeder.LocationID = Location.LocationID and Location.LocationID =:LocationID"
FEEDER_TABLE = "select Feeder.Feeder_Name , count(Farmer.FarmerID) from Farmer, Feeder, Location where Farmer.FeederID = Feeder.FeederID and Feeder.LocationID = Location.LocationID and Location.LocationID =:LocationID group by Farmer.FeederID"

def get_farmer_count(location_id) :

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : FARMER_COUNT,
        'parameters' : {
            'LocationID' : location_id
        }
    })

    return json.loads(data.text)

def get_supply_lines(location_id) :

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : SUPPLY_LINES,
        'parameters' : {
            'LocationID' : location_id
        }
    })

    return json.loads(data.text)

def get_count_supply_lines(location_id) :

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : COUNT_SUPPLY_LINES,
        'parameters' : {
            'LocationID' : location_id
        }
    })

    return json.loads(data.text)['result'][0]['count(FeederID)']


def get_locations() :

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : LOCATION,
        'parameters' : None
    })

    return json.loads(data.text)


def get_farmer_table(location_id) :

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : FARMER_TABLE_Q,
        'parameters' : {
            'LocationID' : location_id 
        }
    })

    return json.loads(data.text)


def get_feeder_info(location_id) :

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : FEEDER_TABLE,
        'parameters' : {
            'LocationID' : location_id 
        }
    })

    return json.loads(data.text)

def insert_feeder(location_id, feeder_name) :

    #obtain latest FeederID from that location

    QUERY1 = "select count(FeederID) from Feeder where FeederID like :Pattern"

    res1 = requests.post('http://localhost:7000/api/select', json = {
        "query" : QUERY1,
        "parameters" : {
            "Pattern" : location_id[:2]+"%"
        }
    })


    count = int(json.loads(res1.text)['result'][0]["count(FeederID)"]) + 1

    values = (location_id, location_id[:2]+"0"+str(count), feeder_name)
    QUERY = "insert into Feeder (LocationID, FeederID, Feeder_Name) values "+str(values)

    #run insert query to add the result

    requests.post('http://localhost:7000/api/insert', json = {
        'query' : QUERY,
        'parameters' : None
    })

    #test

    data = requests.post('http://localhost:7000/api/select', json = {
        'query' : 'select * from Feeder where FeederID =:FeederID',
        "parameters" : {
            "FeederID" : location_id[:2] + "0" + str(count)
        }  
    })

    return json.load(data.text)



