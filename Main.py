from GUI import GUI
from PEOPLE import PeopleList

#  创建GUI
a = GUI()
a.add_barrier()
a.update_gui()

#  创建行人列表
people_list = PeopleList()
time = 0
#  在GUI初始化各个行人
for i in range(0, len(people_list.list)):
    now = people_list.list[i]
    a.add_oval(now.loc[0]-now.r, now.loc[1]-now.r, now.loc[0]+now.r, now.loc[1]+now.r, now.id)
a.update_gui()

#  各个行人开始移动
while len(people_list.list) > 0:
    i = 0
    while i < len(people_list.list):
        a.del_oval(people_list.list[i].id)
        if people_list.list[i].loc[0] > 1040:  # 如果有人走出房间，则移除
            people_list.list.pop(i)
            continue
        i = i+1
    people_list.move()  # 行人移动
    for i in range(0, len(people_list.list)):  # 在GUI中更新行人位置
        now = people_list.list[i]
        a.add_oval(int(now.loc[0]) - now.r, int(now.loc[1]) - now.r, int(now.loc[0]) + now.r,
                   int(now.loc[1]) + now.r, now.id)
    time = time + 0.005  # 更新时间
    a.update_time(str(round(time, 3)))
    a.update_gui()

a.start()
