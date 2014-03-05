import random

oldidlist = range(1,100000)
newidlist = set()

random.seed(123456)

while len(newidlist) < len(oldidlist):
	newidlist.add(random.randint(100000000,999999999))

print len(newidlist)

newidactuallist = list(newidlist)

for i in range(1,20):
	print newidactuallist[i]

#----------------------------

oldidlist = range(1,100000)
newidlist = set()

random.seed(123456)

while len(newidlist) < len(oldidlist):
	newidlist.add(random.randint(100000000,999999999))

print len(newidlist)

newidactuallist2 = list(newidlist)

for i in range(1,20):
	print newidactuallist2[i]

if newidactuallist2 == newidactuallist:
	print "Hooray!"

#----------------------------

oldidlist = range(1,10000)
newidlist = set()

random.seed(123456)

while len(newidlist) < len(oldidlist):
	newidlist.add(random.randint(100000000,999999999))

print len(newidlist)

newidactuallist3 = list(newidlist)

for i in range(1,20):
	print newidactuallist3[i]

if newidactuallist3 == newidactuallist[0:9998]:
	print "Hooray!"
else:
	print "Boo."

# build large and small set; extend existing set of alternate ids
# by converting old list to set, then keep adding to full size, then
# take those not in old set and add to list.
