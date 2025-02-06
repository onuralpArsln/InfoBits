import random
list1 = [[1234],[5678]] # 2 d list instead of tuple which is immutable
for i in range(len(list1)):
        print("preshuff",list1[i])
        random.shuffle(list1[i]) # shuffled in place
        print("postshuff",list1[i])