pushpops = list()

i = 0
for line in list(open("example1.s", "r")):
	if "push" in line:
		pushpops.append(("push", i))
		i += 1
	elif "pop" in line:
		pass
	else:
		pass

"""for line in reversed(list(open("example1.s", "r"))):
	if "pop" in line:
		pushpops.pop(0)
	else:
		pass"""

# i ist nr vom push-pop pair
# startet von 0
def find_pop_zu_push(nr):
	index = nr
	for line in reversed(list(open("example1.s", "r"))):
		print("test")
		if "pop" in line and index==0:
			pushpops.append(("pop", nr))
			return
		else:
			index -= 1


for p,i in pushpops:
	find_pop_zu_push(i)

print(pushpops)
