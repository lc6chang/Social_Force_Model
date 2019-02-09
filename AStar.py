class Node:
    def __init__(self):
        #  初始化各个坐标点的g值、h值、f值、父节点
        self.g = 0
        self.h = 0
        self.f = 0
        self.father = (0, 0)


class AStar:
    @staticmethod
    def next_loc(x, y):
        # 初始化各种状态
        start_loc = (x, y)  # 初始化起始点
        aim_loc = [(26, 4)]  # 初始化目标地点
        open_list = []  # 初始化打开列表
        close_list = []  # 初始化关闭列表
        barrier_list = []  # 初始化障碍列表
        #  添加障碍
        for i in range(0, 27):
            barrier_list.append((i, 0))
            barrier_list.append((i, 16))
        for i in range(1, 16):
            barrier_list.append((0, i))
            barrier_list.append((26, i))
        barrier_list.remove((26, 4))
        for i in range(10, 18):
            for j in range(4, 7):
                barrier_list.append((i, j))
            for j in range(10, 13):
                barrier_list.append((i, j))

        # 创建存储节点的矩阵
        node_matrix = [[0 for i in range(17)] for i in range(27)]
        for i in range(0, 27):
            for j in range(0, 17):
                node_matrix[i][j] = Node()

        open_list.append(start_loc)  # 起始点添加至打开列表
        # 开始算法的循环
        while True:
            now_loc = open_list[0]
            for i in range(1, len(open_list)):  # （1）获取f值最小的点
                if node_matrix[open_list[i][0]][open_list[i][1]].f < node_matrix[now_loc[0]][now_loc[1]].f:
                    now_loc = open_list[i]
            #   （2）切换到关闭列表
            open_list.remove(now_loc)
            close_list.append(now_loc)
            #  （3）对相邻格中的每一个
            list_offset = [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]
            for temp in list_offset:
                temp_loc = (now_loc[0] + temp[0], now_loc[1] + temp[1])
                if temp_loc[0] < 0 or temp_loc[0] > 26 or temp_loc[1] < 0 or temp_loc[1] > 16:
                    continue
                if temp_loc in barrier_list:  # 如果在障碍列表，则跳过
                    continue
                if temp_loc in close_list:  # 如果在关闭列表，则跳过
                    continue

                #  该节点不在open列表，添加，并计算出各种值
                if temp_loc not in open_list:
                    open_list.append(temp_loc)
                    node_matrix[temp_loc[0]][temp_loc[1]].g = (node_matrix[now_loc[0]][now_loc[1]].g +
                                                             int(((temp[0]**2+temp[1]**2)*100)**0.5))
                    node_matrix[temp_loc[0]][temp_loc[1]].h = (abs(aim_loc[0][0]-temp_loc[0])
                                                               + abs(aim_loc[0][1]-temp_loc[1]))*10
                    node_matrix[temp_loc[0]][temp_loc[1]].f = (node_matrix[temp_loc[0]][temp_loc[1]].g +
                                                               node_matrix[temp_loc[0]][temp_loc[1]].h)
                    node_matrix[temp_loc[0]][temp_loc[1]].father = now_loc
                    continue

                #  如果在open列表中，比较，重新计算
                if node_matrix[temp_loc[0]][temp_loc[1]].g > (node_matrix[now_loc[0]][now_loc[1]].g +
                                                             int(((temp[0]**2+temp[1]**2)*100)**0.5)):
                    node_matrix[temp_loc[0]][temp_loc[1]].g = (node_matrix[now_loc[0]][now_loc[1]].g +
                                                             int(((temp[0]**2+temp[1]**2)*100)**0.5))
                    node_matrix[temp_loc[0]][temp_loc[1]].father = now_loc
                    node_matrix[temp_loc[0]][temp_loc[1]].f = (node_matrix[temp_loc[0]][temp_loc[1]].g +
                                                               node_matrix[temp_loc[0]][temp_loc[1]].h)

            #  判断是否停止
            if aim_loc[0] in close_list:
                break

        #  依次遍历父节点，找到下一个位置
        temp = aim_loc[0]
        while node_matrix[temp[0]][temp[1]].father != start_loc:
            temp = node_matrix[temp[0]][temp[1]].father
        #  返回下一个位置的方向向量，例如：（-1,0），（-1,1）......
        re = (temp[0] - start_loc[0], temp[1] - start_loc[1])
        return re
