import xml.etree.ElementTree as ET

from numpy import void
doc = ET.parse("/home/marc/ros-ws/theconstructcore-ws/quadrotor-ws/src/hector_control/worlds/quadrotor_sim/scene_obstacle_v2.sdf")

root = doc.getroot()
def print_child(child):
    print(child.tag, child.attrib)


# search recursive tag and return element
def search_tag(doc, tag):
    for child in doc:
        if(child.tag == tag):
            # print(child)
            return child
        else:
            # print_child(child
            # return search_tag(child, tag)
            aux = search_tag(child, tag)
            if(aux == None):
                # print("okay") 
                pass
            else:
                return aux     
x, y =  [], []
w = search_tag(root, "state")
for child in w:
    # print(child.attrib)
    if(child.tag == "model"):
        for item in child:
            if(item.tag == "pose"):
                pose = item.text.split(" ")
                x.append(pose[0])
                y.append(pose[1])
        # print(child.tag, child.attrib)


print(y)