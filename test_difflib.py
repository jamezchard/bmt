import difflib
import jellyfish

def main():
    with open("left.txt", mode='r',encoding='utf-8') as lf:
        lline = lf.readlines()[0]
    with open("right.txt", mode='r',encoding='utf-8') as rf:
        rline = rf.readlines()[0]
    sm = difflib.SequenceMatcher(isjunk=None,a=lline, b=rline)
    jws = jellyfish.jaro_winkler_similarity(lline,rline)
    print(sm.ratio())
    print(jws)


if __name__ == "__main__":
    main()
