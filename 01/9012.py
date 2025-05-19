import sys

sys.setrecursionlimit(10**6)
input = sys.stdin.readline

t = int(input().strip())

for _ in range(t):

    def solve():
        string = input().strip()
        stack = []
        for s in string:
            if s == "(":
                stack.append(1)
            else:
                if not stack:
                    print("NO")
                    return
                stack.pop()
        if stack:
            print("NO")
            return
        print("YES")

    solve()
