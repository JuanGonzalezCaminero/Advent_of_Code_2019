f=open("input")
orbits=f.read()
f.close()
orbits = orbits.split("\n")
orbits = [o.split(')') for o in orbits]
orbits = [o for o in orbits if o!=['']]

def transfers_count(current_node, target_node, orbits):
    queued_nodes=[]
    for o in orbits:
        if o[0]==current_node:
            if o[1]==target_node:
                return 1
            if o[1] not in queued_nodes:
                queued_nodes.append(o[1]) 
        if o[1]==current_node:
            if o[0]==target_node:
                return 1
            if o[0] not in queued_nodes:
                queued_nodes.append(o[0])
    while True:
        try:
            next_node = queued_nodes.pop(0)
            transfers = transfers_count(next_node, target_node, orbits)
            if transfers>0:
                return transfers+1
        except:
            return 0
print(transfers_count("YOU", "SAN", orbits))
