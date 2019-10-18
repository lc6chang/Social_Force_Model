from gui import GUI
from people import PeopleList

#  创建GUI
gui = GUI()
gui.add_barrier()
gui.update_gui()

#  创建行人列表
people_list = PeopleList()
time = 0
#  在GUI初始化各个行人
for people in people_list.list:
    gui.add_oval(people.loc[0]-people.r, people.loc[1]-people.r,
                 people.loc[0]+people.r, people.loc[1]+people.r, people.id)
gui.update_gui()

#  各个行人开始移动
while people_list.list:
    i = 0
    while i < len(people_list.list):
        gui.del_oval(people_list.list[i].id)
        if people_list.list[i].loc[0] > 1040:  # 如果有人走出房间，则移除
            people_list.list.pop(i)
            continue
        i += 1
    people_list.move()  # 行人移动
    for people in people_list.list:  # 在GUI中更新行人位置
        gui.add_oval(int(people.loc[0]) - people.r, 
                     int(people.loc[1]) - people.r, int(people.loc[0]) + people.r,
                     int(people.loc[1]) + people.r, people.id)
    time = time + 0.005  # 更新时间
    gui.update_time(str(round(time, 3)))
    gui.update_gui()

gui.start()
