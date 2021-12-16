import pygame
from pygame.locals import *
import time
from drawingPrimitives import *

graph = {}
visited = {}
queue = []


def DFS(rootNode):
    if (visited[rootNode] == False):
        visited[rootNode] = True
        TraversalDraw()
        time.sleep(1)
        for i in graph[rootNode]:
            DFS(i)


def BFS():
    global queue
    if(len(queue) == 0):
        return 0
    node = queue.pop(0)
    for tempNode in graph[node]:
        if(not(tempNode in queue)):
            queue.append(tempNode)
    if(visited[node] == False):
        visited[node] = True
    TraversalDraw()
    time.sleep(1)
    for x in visited:
        if(visited[x] == False):
            BFS()


def TraversalDraw():
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    index = 0
    for i in graph:
        if visited[i] == True:
            drawFilledCircle(i[0], i[1])
            index += 1
    for i in graph:
        if visited[i] == True and graph[i]:
            for endpoint in graph[i]:
                if visited[endpoint] == True:
                    drawLine(i[0], i[1], endpoint[0], endpoint[1])
    pygame.display.flip()


def draw():
    index = 0
    for pos in graph:
        drawHollowCircle(pos[0], pos[1], index)
        index += 1
        # textsurface = myfont.render('0', False, (0, 0, 255))
        # screen.blit(textsurface, dest=(pos[0], pos[1]))
    for node in graph:
        if(graph[node]):
            for endPoint in graph[node]:
                drawLine(node[0], node[1], endPoint[0], endPoint[1])


def main():
    pygame.init()
    pygame.font.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluOrtho2D(0, WIDTH, HEIGHT, 0)

    # default mode
    mode = "view-only"
    print("current mode is "+mode)
    print("key-bindings are")
    print("i: Thêm node, c: Thêm cạnh, d: Xóa cạnh, e: Xóa nốt, a: Duyệt DFS , b: Duyệt BFS, any other key for view-only")

    connections = 0
    conNode = None
    deletions = 0
    delNode = None
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                keyPressed = event.key
                if pygame.key.name(keyPressed) == 'i':
                    mode = "insert"
                elif pygame.key.name(keyPressed) == 'c':
                    mode = "connect"
                elif pygame.key.name(keyPressed) == 'd':
                    mode = "disconnect"
                elif pygame.key.name(keyPressed) == 'e':
                    mode = "eliminate"
                elif pygame.key.name(keyPressed) == 'a':
                    mode = "DFS"
                elif pygame.key.name(keyPressed) == 'b':
                    mode = "BFS"
                else:
                    mode = "view-only"
                    print(
                        "i for insert, c for connect, d for disconnect, e for eliminate, a for DFS , b for BFS, any other key for view-only")
                print("key "+pygame.key.name(keyPressed) +
                      " pressed, mode is "+mode)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and mode == "insert":
                    pos = pygame.mouse.get_pos()
                    flag = 0
                    if((pos[0] <= RAD or pos[0] >= WIDTH-RAD) or (pos[1] <= RAD or pos[1] >= HEIGHT-RAD)):
                        flag = 1
                    for pos1 in graph:
                        if(flag == 1):
                            break
                        dist = distance(pos[0], pos[1], pos1[0], pos1[1])
                        if(dist <= 2*RAD):
                            flag = 1
                            break
                    if(flag == 0):
                        graph[pos] = []
                elif event.button == 1 and mode == "connect":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            connections += 1
                            if(connections == 1):
                                conNode = node
                                break
                            elif(connections == 2):
                                if (node != conNode) and (not (node in graph[conNode])):
                                    graph[conNode].append(node)
                                    graph[node].append(conNode)
                                connections = 0
                                break

                elif event.button == 1 and mode == "disconnect":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            deletions += 1
                            if(deletions == 1):
                                delNode = node
                                print('delNode', delNode)
                                break
                            elif(deletions == 2):
                                print('node', node)
                                if delNode in graph[node]:
                                    graph[delNode].remove(node)
                                    graph[node].remove(delNode)
                                deletions = 0
                                break

                elif event.button == 1 and mode == "eliminate":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            for key in graph:
                                for temp in graph[key]:
                                    if temp == node:
                                        graph[key].remove(temp)
                            del graph[node]
                            break

                elif event.button == 1 and mode == "DFS":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            # clearing the visited list
                            for i in graph:
                                visited[i] = False
                            DFS(node)
                            print("DFS COMPLETED, Setting mode to view-only")
                            mode = "view-only"
                            break

                elif event.button == 1 and mode == "BFS":
                    pos = pygame.mouse.get_pos()
                    for node in graph:
                        if (distance(node[0], node[1], pos[0], pos[1]) <= RAD):
                            # clearing the visited list
                            for i in graph:
                                visited[i] = False
                            global queue
                            print(queue)
                            del queue[:]
                            queue.append(node)
                            BFS()
                            print("BFS COMPLETED, Setting mode to view-only")
                            mode = "view-only"
                            break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.607, 0.278, 0.3, 1)
        draw()
        pygame.display.flip()


main()
