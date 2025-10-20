a = {"hoge":[0,1],1:1}
b = [0,1]
b.append(a)
c = [0,1]
c.append({"hoge":[0,1],1:1})
# c[2]["hoge"] = 2
if b == c:
    print(True)
else:
    print(False)
        