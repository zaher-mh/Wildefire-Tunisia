from conf import *
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqldb://'+user_mysql+':'+pass_mysql+'@'+host_mysql+'/' + db_name)
def construct_geojson():
    query = ('select * from fire where latitude>30.410782 and latitude<37.410782 and longitude>7 and longitude<12 and timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR) AND timestamp <= NOW();')
    rawData = engine.execute(query)




    # the template. where data from the csv will be formatted to geojson
    template = \
        ''' \
        { "type" : "Feature",
            "id" : %s,
                "geometry" : {
                    "type" : "Point",
                    "coordinates" : [%s,%s]},
            "properties" : { "confidence" : "%s", "date" : "%s", "time" : "%s"}
            },'''

    # the head of the geojson file
    output = \
        ''' \
    { "type" : "Feature Collection",
        "features" : [
        '''

    # loop through the csv by row skipping the first
    iter = 0
    for row in rawData:
        id = iter
        lat = row[0]
        lon = row[1]
        confidence = row[8]
        date = row[5]
        time = row[6]
        output += template % (id, lon, lat, confidence, date,time)

    # the tail of the geojson file
    output = output[:-1]
    output += \
        ''' \
        ]
    }
        '''
    return output
    # opens an geoJSON file to write the output to
    #outFileHandle = open("/home/zaher/other_projects/tnelec/leaflet/output.geojson", "w")
    #outFileHandle.write(output)
    #outFileHandle.close()