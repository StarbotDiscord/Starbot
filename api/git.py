def getCommit():
    with open(".git/HEAD") as f:
        HEADFileS = f.read()
        HFileA = HEADFileS.split(": ")
        with open(".git/{}".format(HFileA[1].strip())) as e:
            commit = e.read()
            return commit.strip()

def getBranch():
    with open(".git/HEAD") as f:
        HEADFileS = f.read()
        HFileA = HEADFileS.split(": ")
        branch = HFileA[1].split("/")[-1]
        return branch.strip()
