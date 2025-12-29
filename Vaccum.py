Agent={"Pos":[1,1], 
        "Dir": 0, 
        "HasDirt": False, 
        "Score": 0}
Map={"Size":[7,7],
    "DirtLocations":[[2,2],[2,4],[5,4]],
    "WallLocations":[[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[1,0],[1,5],[1,6],[2,0],[2,5],[2,6],[3,0],[3,5],[3,6],[4,0],[4,2],[4,6],[5,0],[5,1],[5,2],[5,3],[5,6],[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6]]}
def MoveForward(Agent, Map):
    NewPos=Agent["Pos"].copy()
    if Agent["Dir"]==0:
        NewPos[1]+=1
    elif Agent["Dir"]==1:
        NewPos[0]+=1
    elif Agent["Dir"]==2:
        NewPos[1]-=1
    elif Agent["Dir"]==3:
        NewPos[0]-=1
    if (0 <= NewPos[0] < Map["Size"][0] and
        0 <= NewPos[1] < Map["Size"][1] and
        NewPos not in Map["WallLocations"]):
        Agent["Pos"]=NewPos
    return Agent

def TurnLeft(Agent):
    Agent["Dir"]=(Agent["Dir"]-1)%4
    return Agent

def TurnRight(Agent):
    Agent["Dir"]=(Agent["Dir"]+1)%4
    return Agent

def SuckDirt(Agent, Map):
    if Agent["Pos"] in Map["DirtLocations"]:
        Map["DirtLocations"].remove(Agent["Pos"])
        Agent["HasDirt"]=True
        Agent["Score"]+=10
    return Agent, Map

def DropDirt(Agent, Map):
    if Agent["HasDirt"]:
        Agent["HasDirt"]=False
        Agent["Score"]-=5
    return Agent, Map

def GetPercept(Agent, Map):
    Percept={"Bump": False,
             "Dirt": Agent["Pos"] in Map["DirtLocations"],
             "WallAhead": False}
    NewPos=Agent["Pos"].copy()
    if Agent["Dir"]==0:
        NewPos[1]+=1
    elif Agent["Dir"]==1:
        NewPos[0]+=1
    elif Agent["Dir"]==2:
        NewPos[1]-=1
    elif Agent["Dir"]==3:
        NewPos[0]-=1
    if (NewPos[0] < 0 or NewPos[0] >= Map["Size"][0] or
        NewPos[1] < 0 or NewPos[1] >= Map["Size"][1] or
        NewPos in Map["WallLocations"]):
        Percept["WallAhead"]= True
    return Percept


max_steps = 10000
steps = 0
while len(Map["DirtLocations"])>0 and steps < max_steps:
    Percept=GetPercept(Agent, Map)
    if Percept["Dirt"]:
        Agent, Map=SuckDirt(Agent, Map)
        print("Sucked dirt at position:", Agent["Pos"])
    elif not Percept["WallAhead"]:
        Agent=MoveForward(Agent, Map)
        print("Moved to position:", Agent["Pos"])
    else:
        Agent=TurnRight(Agent)
        print("Turned right. New direction:", Agent["Dir"])
    steps += 1

if steps >= max_steps:
    print("Stopped: reached max step limit without cleaning all dirt.")
print("Final Agent State:", Agent)
print("Final Map State:", Map)
