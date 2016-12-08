import bisect
import sys

dist = [0]*2761

for i in range (0, 2760):
	with open("./output/part-r-" + str(i), "r") as f:
		for line in f:
			parse = line.split(" ")
			source = int(parse[0])
			value = int(parse[1])
			if dist[source] < value:
				dist[source] = value

node = 0
value = 1000
for i in range (0, 2760):
	if dist[i] < value:
		value = dist[i];
		node = i

f = open("./Result", "w")
f.write(str(node) + " with value of " + str(value) + ".\n")

print(str(node) + " é o nó central com um valor máximo de " + str(value) + " de distancia entre todos os nós")
