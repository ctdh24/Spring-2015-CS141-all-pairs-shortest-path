import os
import re
import sys
import time

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(\\d+)")

def BellmanFord(G):
     pathPairs = [[0 for i in range(len(G[0]))] for j in range(len(G[0]))]
     for i in range(len(G[0])):
         for j in range(len(G[0])):
             if(i == j):
                pathPairs[i][j] = float(0)
             else:
                pathPairs[i][j] = float("Inf")
     #assume starting node is 0
     pathPairs[0][0] = 0
     for i in range(1, len(G[0])-1):
         for j in range(len(G[0])):
             for k in range(len(G[0])):
                 for l in range(len(G[0])):
                    if float(pathPairs[j][k]) + float(G[1][k][l]) < float(pathPairs[k][l]):
                        pathPairs[k][l] = float(pathPairs[j][k]) + float(G[1][k][l])
     for j in range(len(G[0])):
         for k in range(len(G[0])):
             for l in range(len(G[0])):
                if float(pathPairs[k][l]) + float(G[1][j][k]) < float(pathPairs[k][l]):
                    print "false"
                    return pathPairs
        
    # i = 1
    # for i in range(len(G[0])-1):
    #     for j in range(len(G[0])-1):
    #         print ("d")
    # Fill in your Bellman-Ford algorithm here
    # The pathPairs will contain a matrix of path lengths:
    #    0   1   2 
    # 0 x00 x01 x02
    # 1 x10 x11 x12
    # 2 x20 x21 x22
    # Where xij is the length of the shortest path between i and j
     print "true"
     return pathPairs
    
def FloydWarshall(G):
    l = len(G[0])
    pathPairs = [[0 for i in range(l)] for j in range(l)]
    # Fill in your Floyd-Warshall algorithm here
    # The pathPairs will contain a matrix of path lengths:
    #    0   1   2 
    # 0 x00 x01 x02
    # 1 x10 x11 x12
    # 2 x20 x21 x22
    # Where xij is the length of the shortest path between i and j
    for i in range(l):
        for j in range(l):
            if i == j:
                pathPairs[i][j] = float(0)
            elif G[1][i][j] != float("Inf"):
                pathPairs[i][j]  = G[1][i][j]
            else:
                pathPairs[i][j] = float("Inf")
    for k in range(l):
        for i in range(l):
                for j in range(l):
                    pathPairs[i][j] = min(float(pathPairs[i][j]), float(pathPairs[i][k])+float(pathPairs[k][j]))
    #print (G[1][0])
    return pathPairs

def readFile(filename):
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) >= len(vertices) or int(sink) >= len(vertices):
                print("Attempting to insert an edge between "+str(source)+" and "+str(sink)+" in a graph with "+str(len(vertices))+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)][int(sink)]=weight
    # TODO: Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

def writeFile(lengthMatrix,filename):
    filename=os.path.splitext(os.path.split(filename)[1])[0]
    outFile=open('output/'+filename+'_output.txt','w')
    for vertex in lengthMatrix:
        for length in vertex:
            outFile.write(str(length)+',')
        outFile.write('\n')


def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    pathLengths=[]
    if algorithm == 'b' or algorithm == 'B':
        pathLengths=BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        pathLengths=FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))
    writeFile(pathLengths,filename)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python bellman_ford.py -<f|b> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
