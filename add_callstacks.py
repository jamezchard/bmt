from pathlib import Path
from bmt_v2bm import v2bm

import sys
import re


def main() -> None:
    # will try to support more kinds of callstacks
    regex_gpuview = r"(\S*\.dll!.*) \[(.*) \@ (\S*)\]"
    with open(sys.argv[1], mode="r", encoding="utf-8") as txt:
        for textline in txt:
            if len(textline.strip()) == 0:
                continue
            matches = re.findall(regex_gpuview, textline.strip(), re.MULTILINE)
            if not (len(matches) == 1 and len(matches[0]) == 3):
                print(textline)
                raise RuntimeError
            label, pos, line = matches[0]
            v2bm(Path(pos), int(line), str(label))


if __name__ == "__main__":
    main()
