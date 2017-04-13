def getCommit():
    if getBranch() == "UNKNOWN":
        return "UNKNOWN"
    else:
        with open(".git/{}".format(getBranch())) as e:
            commit = e.read()
            return commit.strip()

def getBranch():
    with open(".git/HEAD") as f:
        HEADFileS = f.read()
        HFileA = HEADFileS.split(": ")
        if len(HFileA) == 2:
            branch = HFileA[1].split("/")[-1]
            return branch.strip()
        else:
            return "UNKNOWN"
