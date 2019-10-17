import random
import math
from astar import AStar
class People:
    def __init__(self, _id, _loc_x, _loc_y,):
        self.id = _id  # 行人编号
        self.m = 50 + random.randint(0, 20)  # 行人质量/kg
        self.r = (35 + random.randint(0, 5))/2  # 行人半径(肩宽/2)/cm
        self.d_v = (60 + random.randint(0, 20)) / 100  # 期望速度大小/m/s
        self.loc = (_loc_x, _loc_y)  # 当前位置
        self.v = (0, 0)  # 当前速度
        self.a = (0, 0)  # 当前加速度



class PeopleList:
    def __init__(self):
        self.list = []
        count = 0
        #  依次添加行人至self.list
        for i in range(0, 15):
            self.list.append(People("o"+str(count), 60, 60 + i * 40))
            count = count + 1
            self.list.append(People("o"+str(count), 100, 60 + i * 40))
            count = count + 1
            self.list.append(People("o"+str(count), 140, 60 + i * 40))
            count = count + 1

        # 在一开始就计算好各个位置的下一步方向向量，并存储到矩阵中，以节省算力
        k = 5
        self.matrix = [[0 for i in range(17)] for i in range(27)]
        for i in range(0, 27):
            for j in range(0, 17):
                if i == 0:  # 将障碍物的位置也设置对应的方向向量，以便在特殊情况撞墙后能及时调整回来
                    self.matrix[i][j] = (k, 0)
                elif i == 26:
                    self.matrix[i][j] = (-1 * k, 0)
                elif j == 0:
                    self.matrix[i][j] = (0, k)
                elif j == 16:
                    self.matrix[i][j] = (0, -1 * k)
                elif i == 10:
                    if (j == 4) or (j == 10):
                        self.matrix[i][j] = (-1 * k, -1 * k)
                    elif (j == 5) or (j == 11):
                        self.matrix[i][j] = (-1 * k, 0)
                    elif (j == 6) or (j == 12):
                        self.matrix[i][j] = (-1 * k, k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)
                elif i == 17:
                    if (j == 4) or (j == 10):
                        self.matrix[i][j] = (k, -1 * k)
                    elif (j == 5) or (j == 11):
                        self.matrix[i][j] = (k, 0)
                    elif (j == 6) or (j == 12):
                        self.matrix[i][j] = (k, k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)
                elif (j == 4) or (j == 10):
                    if (i > 10) and (i < 17):
                        self.matrix[i][j] = (0, -1 * k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)
                elif (j == 6) or (j == 12):
                    if (i > 10) and (i < 17):
                        self.matrix[i][j] = (0, k)
                    else:
                        self.matrix[i][j] = AStar.next_loc(i, j)
                elif (i > 10) and (i < 17) and ((j == 5) or (j == 11)):
                    self.matrix[i][j] = (0, k)
                else:
                    self.matrix[i][j] = AStar.next_loc(i, j)
        self.matrix[26][4] = (1, 0)


    def move(self):
        #  设置间隔时间、A、B参数
        deta_time = 0.005
        A = 2000
        B = -0.08
        #  下面开始依次计算各个行人下一时刻的加速度
        for i in range(0, len(self.list)):
            now = self.list[i]
            #  下面计算社会力模型的第一项
            next_desired = self.matrix[int(now.loc[0]//40)][int(now.loc[1]//40)]  # 获取下一位置的方向向量
            desired_v = (now.d_v*next_desired[0], now.d_v*next_desired[1])
            #  下面计算社会力模型的第二项fij
            sum_of_fij = (0, 0)
            for j in range(0, len(self.list)):
                if i == j:
                    continue
                temp = self.list[j]
                d = (((now.loc[0] - temp.loc[0])/100)**2 + ((now.loc[1] - temp.loc[1])/100)**2)**0.5
                if d >= 1.4:  # 如果两个行人质心距离超过1.4m（或距离超过1m），之间的作用力可以忽略不计
                    continue
                fij = A * math.exp((d-now.r/100-temp.r/100)/B)
                sum_of_fij = (sum_of_fij[0] + fij * (now.loc[0] - temp.loc[0])/100,
                              sum_of_fij[1] + fij * (now.loc[1] - temp.loc[1])/100)
            #  下面计算社会力模型的第三项fiW
            sum_of_fiw = (0, 0)
            #  首先计算四周墙壁的fiW
            d = now.loc[0] - 40
            if d < 120:
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = 1040 - now.loc[0]
            if (d < 120) and (now.loc[1] > 220 or now.loc[1] < 140):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * (-1) * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = now.loc[1] - 40
            if d < 120:
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * d / 100 + sum_of_fiw[1])
            d = 640 - now.loc[1]
            if d < 120:
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * (-1) * d / 100 + sum_of_fiw[1])
            #  下面计算中间障碍物1的fiW
            d = 400 - now.loc[0]
            if (d < 120) and (d > 0) and (now.loc[1] > 160) and (now.loc[1] < 280):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * (-1) * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = now.loc[0] - 720
            if (d < 120) and (d > 0) and (now.loc[1] > 160) and (now.loc[1] < 280):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = 160 - now.loc[1]
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * (-1) * d / 100 + sum_of_fiw[1])
            d = now.loc[1] - 280
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * d / 100 + sum_of_fiw[1])
            #  下面计算障碍物2的fiW
            d = 400 - now.loc[0]
            if (d < 120) and (d > 0) and (now.loc[1] > 400) and (now.loc[1] < 520):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * (-1) * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = now.loc[0] - 720
            if (d < 120) and (d > 0) and (now.loc[1] > 400) and (now.loc[1] < 520):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (fiw * d / 100 + sum_of_fiw[0], sum_of_fiw[1])
            d = 400 - now.loc[1]
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * (-1) * d / 100 + sum_of_fiw[1])
            d = now.loc[1] - 520
            if (d < 120) and (d > 0) and (now.loc[0] > 400) and (now.loc[0] < 720):
                fiw = A * math.exp((d - now.r) / 100 / B)
                sum_of_fiw = (sum_of_fiw[0], fiw * d / 100 + sum_of_fiw[1])
            #  下面计算各个行人的加速度分量
            a_x = ((now.m * (desired_v[0] - now.v[0]) / 0.5) + sum_of_fij[0] + sum_of_fiw[0]) / now.m
            a_y = ((now.m * (desired_v[1] - now.v[1]) / 0.5) + sum_of_fij[1] + sum_of_fiw[1]) / now.m
            self.list[i].a = (a_x, a_y)

        #  开始计算各个行人新的速度、下一位置，并更新
        for i in range(0, len(self.list)):
            now = self.list[i]
            a_x = now.a[0]
            a_y = now.a[1]
            v0_x = now.v[0]
            v0_y = now.v[1]
            v_x = v0_x + a_x * deta_time  # 计算新速度并更新
            v_y = v0_y + a_y * deta_time
            self.list[i].v = (v_x, v_y)
            l_x = (v0_x * deta_time + deta_time * a_x * deta_time * deta_time)*100 + now.loc[0]  # 计算新的速度并更新
            l_y = (v0_y * deta_time + deta_time * a_y * deta_time * deta_time)*100 + now.loc[1]
            self.list[i].loc = (l_x, l_y)


