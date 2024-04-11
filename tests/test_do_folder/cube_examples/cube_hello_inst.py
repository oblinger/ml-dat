import os
import random
from typing import List

from dat.inst import InstContainer, Inst
# from settings import dataclass
from dat.do import do


class Annotation:
    time: float


class Alignment(object):
    gt: Annotation
    ai: Annotation
    code: Annotation

    @staticmethod
    def align(self, sequence1: List[Annotation], sequence2: List[Annotation]) \
            -> List[Annotation]:
        pass


class CubeHelloAnnotation(Annotation):
    color: str
    time: float


def build_hello_runs(num):
    path = f"/tmp/hello{num}_runs"
    os.system(f"rm -r {path}")
    c = InstContainer(path=path, spec={})
    c.save()
    for i in range(10):
        run = Inst(path=os.path.join(c.path, f"{i}"), spec={"main": {}})
        start = random.randint(0, 10)
        range_ = random.randint(0, 10)
        count = 10   # random.choice(20)
        data = [random.randint(0, range_) + start for _ in range(count)]
        run.spec["main"].update(dict(start=start, range=range_, count=count, data=data))
        run.save()


if __name__ == "__main__":
    print("The CWD = ", os.getcwd())
    build_hello_runs(5)
    build_hello_runs(10)
    do("cube_hello", show=True)
