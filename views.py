achievements=[]
tasks=[]
def label(value):
    labely=input("Do you want to label this as achievement?")
    if labely== "Yes":
        achievements.append(value)

def addtasks():
    for i in range(0,100):
        value=input("Enter a new task: ")
        tasks.append(value)
        
        if value == "Stop":
            print("Oh Cool, Thank you")
            print("Achievements are here: ", achievements)
            tasks.remove("Stop")
            return tasks
        label(value)

op=addtasks()
print("The Tasks: ", op)

    
