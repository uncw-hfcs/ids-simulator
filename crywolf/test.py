from crywolf import db
import models
with open("testEvents.txt", 'r') as inFile:
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        event= models.TrainingEvent(
            alert_type=line[0],
            name=line[1], 
            email=line[2], 
            result=line[3], 
            source_ip=line[4], 
            organization=line[5], 
            geo_country=line[6], 
            geo_city=line[7], 
            geo_region=line[8]
            )
        db.session.add(event)
        db.session.commit()