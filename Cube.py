class Cube:
    def __init__(self):
        # 초기 면 배치 (0~3 인덱스는 전개도 z 모양 기준)
        self.faces = {
            'U': ['+','-','>','<'],
            'L': [']','-',';','<'],
            'F': ['[',']',':',';'],
            'R': ['+','[','>',' :'],
            'D': ['+','-','>','<'],
            'B': [';',':',']','[']
        }
        self.memory = [0] * 30000
        self.ptr = 0
        self.prev_up = None  # 이전 윗면 상태

    # -------------------------
    # 면 회전
    # -------------------------
    def rotate_face(self, face, clockwise=True):
        f = self.faces[face]
        if clockwise:
            self.faces[face] = [f[2], f[0], f[3], f[1]]
        else:
            self.faces[face] = [f[1], f[3], f[0], f[2]]

    # -------------------------
    # 주변 스티커 회전
    # -------------------------
    def _cycle_edges(self, faces, idxs):
        """faces 리스트에 해당 idxs를 순서대로 회전"""
        temp = [self.faces[faces[-1]][i] for i in idxs]
        for fi in range(len(faces)-1, 0, -1):
            for i in idxs:
                self.faces[faces[fi]][i] = self.faces[faces[fi-1]][i]
        for i, val in zip(idxs, temp):
            self.faces[faces[0]][i] = val

    # -------------------------
    # 회전 명령
    # -------------------------
    def move(self, move):
        face = move.upper()
        clockwise = move.isupper()
        self.rotate_face(face, clockwise)

        # 각 면 회전 규칙 (인덱스는 전개도 기준)
        if face == 'U':
            if clockwise:
                self._cycle_edges(['F','R','B','L'], [0,1])
            else:
                self._cycle_edges(['F','L','B','R'], [0,1])
        elif face == 'D':
            if clockwise:
                self._cycle_edges(['F','L','B','R'], [2,3])
            else:
                self._cycle_edges(['F','R','B','L'], [2,3])
        elif face == 'F':
            if clockwise:
                self._cycle_edges(['U','L','D','R'], [2,3,0,1])
            else:
                self._cycle_edges(['U','R','D','L'], [2,3,0,1])
        elif face == 'B':
            if clockwise:
                self._cycle_edges(['U','R','D','L'], [0,1,2,3])
            else:
                self._cycle_edges(['U','L','D','R'], [0,1,2,3])
        elif face == 'L':
            if clockwise:
                self._cycle_edges(['U','B','D','F'], [0,2,0,0])
            else:
                self._cycle_edges(['U','F','D','B'], [0,0,0,2])
        elif face == 'R':
            if clockwise:
                self._cycle_edges(['U','F','D','B'], [1,1,1,3])
            else:
                self._cycle_edges(['U','B','D','F'], [1,3,1,1])

        # 매 회전 후 윗면 체크
        self.check_up()

    # -------------------------
    # 윗면 검사
    # -------------------------
    def check_up(self):
        up = tuple(self.faces['U'])
        if up != self.prev_up:  # 이전 상태와 다르면
            counts = {}
            for c in up:
                counts[c] = counts.get(c,0) + 1
            for k,v in counts.items():
                if v >= 3:
                    self.execute(k)
                    break
        self.prev_up = up

    # -------------------------
    # Brainfuck 실행
    # -------------------------
    def execute(self, cmd):
        if cmd == '+':
            self.memory[self.ptr] = (self.memory[self.ptr] + 1) % 256
        elif cmd == '-':
            self.memory[self.ptr] = (self.memory[self.ptr] - 1) % 256
        elif cmd == '>':
            self.ptr = (self.ptr + 1) % len(self.memory)
        elif cmd == '<':
            self.ptr = (self.ptr - 1) % len(self.memory)
        elif cmd == '.':
            print(chr(self.memory[self.ptr]), end="")
        elif cmd == ',':
            self.memory[self.ptr] = ord(input()[0])
        # [ ] 루프는 별도 구현 필요

    def __str__(self):
        return str(self.faces)
