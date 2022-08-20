from time import sleep


f = open("pixel.txt", "r", encoding="utf8")
i = 0
for line in f:
    if line != "\n":
        print(f"{i:>4}{line}")
    i += 1
f.close()
