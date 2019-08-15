from crywolf import db
import models, random, string
with open("testEvents.txt", 'r') as inFile:
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        event= models.Event(
            is_false_positive=bool(int(line[0])),
            country_of_authentication1=line[1], 
            number_successful_logins1=int(line[2]), 
            number_failed_logins1=int(line[3]), 
            source_provider1=line[4], 
            country_of_authentication2=line[5], 
            number_successful_logins2=int(line[6]), 
            number_failed_logins2=int(line[7]), 
            source_provider2=line[8],
            time_between_authentications=float(line[9]),
            vpn_confidence=line[10]
            )
        db.session.add(event)
        db.session.commit()

with open("trainingEvents.txt", 'r') as inFile:
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        training_event= models.TrainingEvent(
            is_false_positive=bool(int(line[0])),
            country_of_authentication1=line[1], 
            number_successful_logins1=int(line[2]), 
            number_failed_logins1=int(line[3]), 
            source_provider1=line[4], 
            country_of_authentication2=line[5], 
            number_successful_logins2=int(line[6]), 
            number_failed_logins2=int(line[7]), 
            source_provider2=line[8],
            time_between_authentications=float(line[9]),
            vpn_confidence=line[10]
            )
        db.session.add(training_event)
        db.session.commit()

with open("users.txt", "r") as inFile:
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        user= models.User(
            username = line[0],
            group = line[1]
        )
        db.session.add(user)
        db.session.commit()
