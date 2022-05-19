def loadRoute(file):
    names = []
    with open(file, 'r') as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[1:]
            x = x[:-2]
            # add current item to the list
            x = x.split(", ")
            for num in range(len(x)):
                x[num] = float(x[num])
            names.append(x)
    return names
