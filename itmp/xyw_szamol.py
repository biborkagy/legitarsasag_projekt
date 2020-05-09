fajl = open('count.txt')
xy_db = 0
w_db = 0

while True:
    char = fajl.read(1)
    if char:
        if char == 'X' or char == 'Y':
            xy_db += 1
        if char == 'W':
            w_db += 1

    else:
        break

print(xy_db)
print(w_db)
print(xy_db-w_db)

fajl.close()