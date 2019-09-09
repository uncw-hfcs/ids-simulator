from crywolf import db
import models, random, string
with open("events.txt", 'r') as inFile:
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        event= models.Event(
            should_escalate=line[0],
            country_of_authentication1=line[1], 
            number_successful_logins1=line[2], 
            number_failed_logins1=line[3], 
            source_provider1=line[4], 
            country_of_authentication2=line[5], 
            number_successful_logins2=line[6], 
            number_failed_logins2=line[7], 
            source_provider2=line[8],
            time_between_authentications=line[9],
            vpn_confidence=line[10]
            )
        db.session.add(event)
        db.session.commit()

testerEvent1= models.Event(
        should_escalate=None,
        country_of_authentication1="For this event", 
        number_successful_logins1= "please just", 
        number_failed_logins1='select "Escalate"', 
        source_provider1= 'for your', 
        country_of_authentication2='decision', 
        number_successful_logins2='and "2"', 
        number_failed_logins2='for', 
        source_provider2='confidence',
        time_between_authentications="0",
        vpn_confidence="0"
        )
db.session.add(testerEvent1)
db.session.commit()
testerEvent2= models.Event(
        should_escalate=None,
        country_of_authentication1="For this event", 
        number_successful_logins1= "please just", 
        number_failed_logins1='select "Don\'t escalate"', 
        source_provider1= 'for your', 
        country_of_authentication2='decision', 
        number_successful_logins2='and "4"', 
        number_failed_logins2='for', 
        source_provider2='confidence',
        time_between_authentications="0",
        vpn_confidence="0"
        )
db.session.add(testerEvent2)
db.session.commit()

with open("trainingEvents.txt", 'r') as inFile:
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        training_event= models.TrainingEvent(
            should_escalate=line[0],
            country_of_authentication1=line[1], 
            number_successful_logins1=line[2], 
            number_failed_logins1=line[3], 
            source_provider1=line[4], 
            country_of_authentication2=line[5], 
            number_successful_logins2=line[6], 
            number_failed_logins2=line[7], 
            source_provider2=line[8],
            time_between_authentications=line[9],
            vpn_confidence=line[10]
            )
        db.session.add(training_event)
        db.session.commit()

from random import sample, shuffle



with open("users.txt", "r") as inFile:
    escalate = [x for x in range(49,73)]
    dont_escalate = [y for y in range(1,49)]

    group1Events = escalate + sample(dont_escalate,25)
    group2Events = sample(escalate,9) + sample(dont_escalate,40)
    group3Events = sample(escalate,1) + dont_escalate
    for line in inFile:
        line = line.rstrip() 
        line = line.split('\t')
        if line[1] == "1":
            temp = group1Events
        elif line[1] == "2":
            temp = group2Events
        else:
            temp = group3Events
        
        shuffle(temp)
        
        assignment = str(temp).strip("[]").replace(" ","")
        user= models.User(
            username = line[0],
            group = line[1],
            events = assignment,
            questionnaire_complete = False,
            training_complete = False,
            experiment_complete = False,
            survey_complete = False,
            completion_code = line[2]
            )
        db.session.add(user)
        db.session.commit()