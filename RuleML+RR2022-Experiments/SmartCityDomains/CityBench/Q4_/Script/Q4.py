import haversine as hs
import json

def isClosest(Lat1, Lon1, cTime):
	pathToLocation="newSRBenchCorrect/Q4_/BK/eventLocations.json"
	pathToDuration="newSRBenchCorrect/Q4_/BK/eventDurations.json"
	eventLocations=dict()
	eventDurations=dict()
	with open(pathToLocation) as f:
		eventLocations = json.loads(f.read())
	with open(pathToLocation) as f:
		eventDurations = json.loads(f.read())
	userloc=(float(Lat1),float(Lon1))
	currentTime=float(cTime)
	event=None
	dist=None
	for l in eventDurations:
		duration=eventDurations[l]
		if currentTime>=duration[0] and currentTime<=duration[1]:
			eventLoc=eventLocations[l]
			#print(eventLocations[l])
			loc2=(eventLoc[0],eventLoc[1])
			dist2=hs.haversine(userloc,loc2)
			if dist==None or dist2<dist:
				event=l
				dist=dist2
	if event==None:
		return "no close events"
	return event
