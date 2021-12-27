# # 18428
n = int(input())
board = []
teacher = []
student = []
for i in range(n):
    tmp = input().split()
    for j in range(n):
        if tmp[j] == 'T':
            teacher.append((i, j))
        elif tmp[j] == 'S':
            student.append((i, j))
    board.append(tmp)
direction = [(1,0),(0,1),(-1,0),(0,-1)]

def check():
    visited = [[False for _ in range(n)] for _ in range(n)]
    queue = teacher[:]
    while queue:
        x, y = queue.pop(0)
        for dx, dy in direction:
            nx, ny = x+dx, y+dy
            while True:
                if 0 > nx or nx >= n or 0 > ny or ny >= n:
                    break
                if board[nx][ny] == 'X' and not visited[nx][ny]:
                    visited[nx][ny] = True
                elif board[nx][ny] == 'S':
                    return False
                elif board[nx][ny] == 'O':
                    break
                nx, ny = nx+dx, ny+dy

    return True

answer = False

def dfs(cnt):
    global answer
    if cnt == 3:
        if check():
            answer = True
        return

    for i in range(n):
        for j in range(n):
            if board[i][j] == 'X':
                board[i][j] = 'O'
                dfs(cnt+1)
                board[i][j] = 'X'
dfs(0)
print("YES" if answer else "NO")

# 1038
"""
0 1 2 3 4 5 6 7 8 9 10 20 21 30 31 32 40 41 42 43 ...
"""
n = int(input())
if n < 10:
    print(n)
else:
    answer, idx = 0, 9
    def dfs(depth, limit, num):
        global answer, idx
        if depth == limit:
            idx += 1
            if idx == n:
                answer = num
                return
        for i in range(int(num[-1])):
            dfs(depth+1, limit, num+str(i))
    for i in range(1, 11):
        for j in range(1, 10):
            dfs(0, i, str(j))
    print(answer if answer != 0 else -1)



# 1747
def prime(x):
    if x == 1:
        return False
    for i in range(2, int(x**0.5)+1):
        if x % i ==0:
            return False
    return True
n = int(input())
answer = 0
while True:
    if prime(n) and str(n) == str(n)[::-1]:
        answer = n
        break
    n += 1
print(answer)