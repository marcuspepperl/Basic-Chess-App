color_dict = {1 : 'w', -1 : 'b'}
name_dict = {1 : 'white', -1 : 'black'}
ranks = set(str(i) for i in range(1, 9))
philes = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}
lower_philes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

def chess_to_coords(grid_str):

    let = grid_str[0]
    n = grid_str[1]

    if let.isupper():
        return ord(let) - 65, int(n) - 1

    else:
        return ord(let) - 97, int(n) - 1

def phile(x):
    return chr(x + 97)

def coords_to_chess(x, y):

    return chr(x + 97) + str(y + 1)

def in_between(x1, x2, y1, y2, z1, z2):
    same_sign = (y1 > z1 - y1 < z1) == (z1 > x1 - z1 < x1)
    in_line = (y1 - x1) * (z2 - x2) == (z1 - x1) * (y2 - x2)
    if same_sign and in_line:
        return True
    return False


def standard_setup():

    whiterook1 = Rook(0, 0, 1)
    whiteknight1 = Knight(1, 0, 1)
    whitebishop1 = Bishop(2, 0, 1)
    whitequeen = Queen(3, 0, 1)
    whiteking = King(4, 0, 1)
    whitebishop2 = Bishop(5, 0, 1)
    whiteknight2 = Knight(6, 0, 1)
    whiterook2 = Rook(7, 0, 1)
    whitepawns = [Pawn(i, 1, 1) for i in range(8)]

    blackrook1 = Rook(0, 7, -1)
    blackknight1 = Knight(1, 7, -1)
    blackbishop1 = Bishop(2, 7, -1)
    blackqueen = Queen(3, 7, -1)
    blackking = King(4, 7, -1)
    blackbishop2 = Bishop(5, 7, -1)
    blackknight2 = Knight(6, 7, -1)
    blackrook2 = Rook(7, 7, -1)
    blackpawns = [Pawn(i, 6, -1) for i in range(8)]

    white_piece_lst = [whiterook1, whiteknight1, whitebishop1, whitequeen, whiteking, whitebishop2, whiteknight2, whiterook2] + whitepawns

    black_piece_lst = [blackrook1, blackknight1, blackbishop1, blackqueen, blackking, blackbishop2, blackknight2, blackrook2] + blackpawns


    return GameBoard(white_piece_lst + black_piece_lst)


class GameBoard:
    def __init__(self, piece_lst):

        self.board = []
        self.strboard = []
        self.white_pieces = []
        self.black_pieces = []
        self.white_casualties = []
        self.black_casualties = []

        rank = [None] * 8
        strrank = [""] * 8

        self.white_king = None
        self.black_king = None

        for i in range(8):
            self.board.append(rank.copy())
            self.strboard.append(strrank.copy())

        for piece in piece_lst:
            x, y = piece.get_coords()
            piece_str = str(piece)

            if piece_str[0] == 'w':
                if piece_str[1] == 'K':
                    if self.white_king == None:
                        self.white_king = piece
                    else:
                        print("There cannot be more than one white king")
                        quit()

                self.white_pieces.append(piece)
            else:
                if piece_str[1] == 'K':
                    if self.black_king == None:
                        self.black_king = piece
                    else:
                        print("There cannot be more than one black king")
                        quit()
                self.black_pieces.append(piece)

            if self.board[x][y] != None:
                print("Invalid board setup")
                quit()
            self.board[x][y] = piece
            self.strboard[x][y] = piece_str

        if self.white_king == None or self.black_king == None:
            print("There must be one black king and one white king")
            quit()


    def display_board(self, color):

        w = 23
        divide_str = ' ' * 2 + '|' + '_' * w + '|'
        edge_str = ' ' * 2 + '_' * (w + 2)
        if color == 1:
            print(edge_str)
            for y in range(7, -1, -1):
                piece_lst = []
                for x in range(8):
                    if self.strboard[x][y]:
                        piece_lst.append(self.strboard[x][y])
                    else:
                        piece_lst.append(' ' * 2)
                print_str = str(y + 1) + ' |' + '|'.join(piece_lst) + '|'
                print(print_str)
                if y != 0:
                    print(divide_str)

            print(edge_str)
            phile_str = ' ' * 3 + (' ' * 2).join(lower_philes)
            print(phile_str)

        else:
            phile_str = ' ' * 3 + (' ' * 2).join(reversed(lower_philes))
            print(phile_str)
            print(edge_str)
            for y in range(8):
                piece_lst = []
                for x in range(7, -1, -1):
                    if self.strboard[x][y]:
                        piece_lst.append(self.strboard[x][y])
                    else:
                        piece_lst.append(' ' * 2)
                print_str = '  |' + '|'.join(piece_lst) + '| ' + str(y + 1)
                print(print_str)
                if y != 7:
                    print(divide_str)

            print(edge_str)


    def get_strboard(self):
        return self.strboard

    def get_piece(self, x, y):
        return self.board[x][y]

    def add_piece(self, piece):
        x, y = piece.get_coords()
        color = piece.get_color()

        dest_piece = self.board[x][y]
        takes = dest_piece != None

        if takes:

            dest_color = dest_piece.get_color()

            if dest_color == 1:
                self.white_pieces.remove(dest_piece)
                self.white_casualties.append(dest_piece)
            else:
                self.black_pieces.remove(dest_piece)
                self.black_casualties.append(dest_piece)

        if color == 1:
            self.white_pieces.append(piece)
        else:
            self.black_pieces.append(piece)


        self.board[x][y] = piece
        self.strboard[x][y] = str(piece)

        return takes


    def remove_piece(self, x, y):

        piece = self.board[x][y]
        remove = piece != None

        if remove:
            color = piece.get_color()

            if color == 1:
                self.white_pieces.remove(piece)
                self.white_casualties.append(piece)

            else:
                self.black_pieces.remove(dest_piece)
                self.black_casualties.append(dest_piece)

            self.board[x][y] = None
            self.strboard[x][y] = ""

        return remove



    def move_piece(self, x, y, newx, newy):

        piece = self.board[x][y]
        piece_str = self.strboard[x][y]

        dest_piece = self.board[newx][newy]

        self.board[x][y] = None
        self.strboard[x][y] = ""

        self.board[newx][newy] = piece
        self.strboard[newx][newy] = piece_str

        piece.increment_move_count()
        piece.modify_coords(newx, newy)

        takes = dest_piece != None

        if takes:
            dest_color = dest_piece.get_color()
            if dest_color == 1:
                self.white_pieces.remove(dest_piece)
                self.white_casualties.append(dest_piece)
            else:
                self.black_pieces.remove(dest_piece)
                self.black_casualties.append(dest_piece)

        return takes


    def is_pinned(self, x, y, color):

        if color == 1:
            king = self.white_king
        else:
            king = self.black_king

        if self.strboard[x][y] == '' or self.strboard[x][y][0] != color_dict[color] or self.strboard[x][y][1] == 'K':
            return False

        king_x, king_y = king.get_coords()

        xdif = x - king_x
        ydif = y - king_y
        if xdif != 0 and ydif != 0 and abs(xdif) != abs(ydif):
            return False

        xsign = (xdif > 0) - (xdif < 0)
        ysign = (ydif > 0) - (ydif < 0)

        newx = king_x + xsign
        newy = king_y + ysign

        while True:
            if x == newx and y == newy:
                break
            if self.strboard[newx][newy] != '':
                return False
            newx += xsign
            newy += ysign

        newx += xsign
        newy += ysign

        while True:
            if 0 <= newx < 8 and 0 <= newy < 8:

                if self.strboard[newx][newy] == '':
                    newx += xsign
                    newy += ysign
                    continue

                if self.strboard[newx][newy][0] == color_dict[color] or self.strboard[newx][newy][1] == 'P':
                    return False

                attacking_piece = self.get_piece(newx, newy)

                if attacking_piece.is_valid_move(self.strboard, x, y):
                    return (newx, newy)
                else:
                    return False

            else:
                return False



    def is_check(self, color):

        if color == 1:
            attacking_pieces = self.black_pieces
            king_x, king_y = self.white_king.get_coords()
        else:
            attacking_pieces = self.white_pieces
            king_x, king_y = self.black_king.get_coords()

        for piece in attacking_pieces:
            if piece.is_valid_move(self.strboard, king_x, king_y):
                return True
        return False


    def is_check_at(self, x, y, color):

        if color == 1:
            attacking_pieces = self.black_pieces
            king = self.white_king
            king_x, king_y = king.get_coords()
        else:
            attacking_pieces = self.white_pieces
            king = self.black_king
            king_x, king_y = king.get_coords()

        new_strboard = []
        for row in self.strboard:
            new_strboard.append(row.copy())

        new_strboard[king_x][king_y] = ""
        new_strboard[x][y] = str(king)

        for piece in attacking_pieces:
            if piece.get_coords() != (x, y) and piece.is_valid_move(new_strboard, x, y):
                    return True
        return False

    def is_check_by(self, color):

        piece_lst = []
        if color == 1:
            attacking_pieces = self.black_pieces
            king_x, king_y = self.white_king.get_coords()
        else:
            attacking_pieces = self.white_pieces
            king_x, king_y = self.black_king.get_coords()

        for piece in attacking_pieces:
            if piece.is_valid_move(self.strboard, king_x, king_y):
                piece_lst.append(piece)

        return piece_lst

    def escapes_check(self, x, y, newx, newy, color):

        defend_piece = self.get_piece(x, y)
        defend_type = str(defend_piece)[1]

        if color == 1:
            king = self.white_king
        else:
            king = self.black_king
        king_x, king_y = king.get_coords()

        attack_lst = self.is_check_by(color)
        attackers = len(attack_lst)

        if defend_type != 'K' and attackers == 1:

            attack_piece = attack_lst[0]
            attack_type = str(attack_piece)[1]
            attack_x, attack_y = attack_piece.get_coords()

            if self.is_pinned(x, y, color):
                return self.is_pinned(x, y, color) == (attack_x, attack_y)

            if newx == attack_x and newy == attack_y:
                return True

            if attack_type != 'N':
                return in_between(x, y, attack_x, attack_y, newx, newy)

        elif defend_type == 'K':
            if not self.is_check_at(newx, newy, color):
                return True


        return False


    def is_checkmate(self, color):

        attack_lst = self.is_check_by(color)
        attackers = len(attack_lst)

        if color == 1:
            king = self.white_king
            king_x, king_y = king.get_coords()
            defending_pieces = self.white_pieces
        else:
            king = self.black_king
            king_x, king_y = king.get_coords()
            defending_pieces = self.black_pieces

        if not attackers:
            return False

        elif attackers == 1:
            attack_piece = attack_lst[0]
            attack_type = str(attack_piece)[1]
            attack_x, attack_y = attack_piece.get_coords()
            xdif = attack_x - king_x
            ydif = attack_y - king_y

            for defend_piece in defending_pieces:
                defend_x, defend_y = defend_piece.get_coords()
                if defend_x == king_x and defend_y == king_y:
                    continue
                if defend_piece.is_valid_takes(self.strboard, attack_x, attack_y) and not self.is_pinned(defend_x, defend_y, color):
                    return False

            if attack_type == 'P':
                row = (color > 0) * 2 + (color < 0) * 5
                if attack_y == row and attack_piece.get_move_count() == 1:
                    defend_x = attack_x - (king_x - attack_x)
                    if not self.is_pinned(defend_x, attack_y, color) and self.strboard[defend_x][attack_y] == color_dict[color] + 'P':
                        return False

            if attack_type != 'N':

                if xdif == 0:
                    absdif = abs(ydif)
                else:
                    absdif = abs(xdif)

                xsign = (xdif > 0) - (xdif < 0)
                ysign = (ydif > 0) - (ydif < 0)
                for i in range(1, absdif):
                    block_x = king_x + i * xsign
                    block_y = king_y + i * ysign
                    for defend_piece in defending_pieces:
                        defend_x, defend_y = defend_piece.get_coords()
                        if defend_x == king_x and defend_y == king_y:
                            continue
                        if defend_piece.is_valid_move(self.strboard, block_x, block_y) and not self.is_pinned(defend_x, defend_y, color):
                            return False


        for valid_move in king.get_valid_moves(self.strboard):
            newx, newy = valid_move
            if not self.is_check_at(newx, newy, color):
                print(newx, newy)
                return False

        return True


    def is_stalemate(self, color, move_lst):
        if color == 1:
            pieces = self.white_pieces
        else:
            pieces = self.black_pieces

        for piece in pieces:
            x, y = piece.get_coords()
            if self.is_pinned(x, y, color):
                continue

            if piece.get_valid_moves(self.strboard):
                return False

            piece_type = str(piece)[1]
            if piece_type == 'P':
                if (color == 1 and y == 5) or (color == -1 and y == 2):
                    if move_lst and len(move_lst[-1]) == 2:
                        prev_x, prev_y = chess_to_coords(move_lst[-1])
                        prev_piece = self.Board.get_piece(prev_x, prev_y)
                        if prev_piece.get_move_count() == 1 and abs(prev_x - x) == 1 and prev_y == y:
                            return False

        return True



class Pawn:
    def __init__(self, x, y, color):
        self.move_count = 0
        self.x = x
        self.y = y
        self.color = color
        self.colorstr = color_dict[self.color]
        self.value = 1

    def __str__(self):
        return self.colorstr + 'P'

    def increment_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def get_coords(self):
        return self.x, self.y

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def modify_coords(self, newx, newy):
        self.x = newx
        self.y = newy

    def is_valid_move(self, strboard, newx, newy):
        xdif = newx - self.x
        ydif = newy - self.y
        if ydif == self.color:
            if xdif == 0:
                return strboard[newx][newy] == ''
            elif abs(xdif) == 1:
                return strboard[newx][newy] and strboard[newx][newy][0] != color_dict[self.color]
        elif ydif == 2 * self.color and xdif == 0 and not self.move_count:
                return strboard[newx][self.y + self.color] == '' and strboard[newx][newy] == ''
        return False

    def is_valid_takes(self, strboard, newx, newy):
        xdif = newx - self.x
        ydif = newy - self.y
        if ydif == self.color and abs(xdif) == 1:
            return strboard[newx][newy] and strboard[newx][newy][0] != color_dict[self.color]
        return False


    def get_valid_moves(self, strboard):
        valid_moves = []
        if 0 <= self.y + self.color < 8 and strboard[self.x][self.y + self.color] == '':
            valid_moves.append((self.x, self.y + self.color))
            if 0 <= self.y + 2 * self.color < 8 and strboard[self.x][self.y + 2 * self.color] == '':
                valid_moves.append((self.x, self.y + 2 * self.color))

        if 0 <= self.y + self.color < 8:
            newx = self.x - 1
            newy = self.y + self.color
            if 0 <= newx and strboard[newx][newy] != '' and strboard[newx][newy][0] != self.colorstr:
                valid_moves.append((newx, newy))
            newx = self.x + 1
            if 0 <= newx and strboard[newx][newy] != '' and strboard[newx][newy][0] != self.colorstr:
                valid_moves.append((newx, newy))

        return valid_moves



class Knight:
    def __init__(self, x, y, color):
        self.move_count = 0
        self.x = x
        self.y = y
        self.color = color
        self.colorstr = color_dict[self.color]
        self.value = 3

    def __str__(self):
        return color_dict[self.color] + 'N'

    def get_coords(self):
        return self.x, self.y

    def increment_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def modify_coords(self, newx, newy):
        self.x = newx
        self.y = newy

    def is_valid_move(self, strboard, newx, newy):
        absxdif = abs(newx - self.x)
        absydif = abs(newy - self.y)
        if (absxdif == 1 and absydif == 2) or (absxdif == 2 and absydif == 1):
            return strboard[newx][newy] == '' or self.colorstr != strboard[newx][newy][0]
        return False

    def is_valid_takes(self, strboard, newx, newy):
        return self.is_valid_move(strboard, newx, newy)

    def get_valid_moves(self, strboard):
        directions = [(1, 2), (2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1), (-1, 2), (-2, 1)]
        valid_moves = []
        for direction in directions:
            xchange, ychange = direction
            newx = self.x + xchange
            newy = self.y + ychange
            if 0 <= newx < 8 and 0 <= newy < 8 and (not strboard[newx][newy] or strboard[newx][newy][0] != self.colorstr):
                valid_moves.append((newx, newy))

        return valid_moves


class Bishop:
    def __init__(self, x, y, color):
        self.move_count = 0
        self.x = x
        self.y = y
        self.color = color
        self.colorstr = color_dict[self.color]
        self.value = 3

    def __str__(self):
        return self.colorstr + 'B'

    def increment_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def get_coords(self):
        return self.x, self.y

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def modify_coords(self, newx, newy):
        self.x = newx
        self.y = newy

    def is_valid_move(self, strboard, newx, newy):
        xdif = newx - self.x
        absxdif = abs(xdif)
        ydif = newy - self.y
        absydif = abs(ydif)

        if xdif != 0 and absxdif == absydif:
            xsign = (xdif > 0) - (xdif < 0)
            ysign = (ydif > 0) - (ydif < 0)

            for i in range(1, absxdif):
                if strboard[self.x + i * xsign][self.y + i * ysign] != '':
                    return False
            return not strboard[newx][newy] or strboard[newx][newy][0] == color_dict[-1 * self.color]
        else:
            return False

    def is_valid_takes(self, strboard, newx, newy):
        return self.is_valid_move(strboard, newx, newy)

    def get_valid_moves(self, strboard):
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        valid_moves = []
        for direction in directions:
            xsign, ysign = direction
            newx = self.x + xsign
            newy = self.y + ysign
            while True:
                if 0 <= newx < 8 and 0 <= newy < 8:
                    if strboard[newx][newy]:
                        if strboard[newx][newy][0] != self.colorstr:
                            valid_moves.append((newx, newy))
                        break
                    else:
                        valid_moves.append((newx, newy))
                        newx += xsign
                        newy += ysign
                else:
                    break

        return valid_moves


class Rook:
    def __init__(self, x, y, color):
        self.move_count = 0
        self.x = x
        self.y = y
        self.color = color
        self.colorstr = color_dict[self.color]
        self.value = 5

    def __str__(self):
        return self.colorstr + 'R'

    def increment_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def get_coords(self):
        return self.x, self.y

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def modify_coords(self, newx, newy):
        self.x = newx
        self.y = newy


    def is_valid_move(self, strboard, newx, newy):
        xdif = newx - self.x
        ydif = newy - self.y

        if xdif == 0 and ydif != 0:
            ysign = (ydif > 0) - (ydif < 0)
            absydif = abs(ydif)

            for i in range(1, absydif):
                if strboard[self.x][self.y + i * ysign]:
                    return False
            return not strboard[newx][newy] or strboard[newx][newy][0] != self.colorstr

        elif xdif != 0 and ydif == 0:
            xsign = (xdif > 0) - (xdif < 0)
            absxdif = abs(xdif)

            for i in range(1, absxdif):
                if strboard[self.x + i * xsign][self.y]:
                    return False
            return not strboard[newx][newy] or strboard[newx][newy][0] != self.colorstr

        return False

    def is_valid_takes(self, strboard, newx, newy):
        return self.is_valid_move(strboard, newx, newy)


    def get_valid_moves(self, strboard):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        valid_moves = []
        for direction in directions:
            xsign, ysign = direction
            newx = self.x + xsign
            newy = self.y + ysign
            while True:
                if 0 <= newx < 8 and 0 <= newy < 8:
                    if strboard[newx][newy]:
                        if strboard[newx][newy][0] != self.colorstr:
                            valid_moves.append((newx, newy))
                        break
                    else:
                        valid_moves.append((newx, newy))
                        newx += xsign
                        newy += ysign
                else:
                    break

        return valid_moves


class Queen:
    def __init__(self, x, y, color):
        self.move_count = 0
        self.x = x
        self.y = y
        self.color = color
        self.colorstr = color_dict[self.color]
        self.value = 9

    def __str__(self):
        return self.colorstr + 'Q'

    def increment_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def get_coords(self):
        return self.x, self.y

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def modify_coords(self, newx, newy):
        self.x = newx
        self.y = newy

    def is_valid_move(self, strboard, newx, newy):
        xdif = newx - self.x
        absxdif = abs(xdif)
        ydif = newy - self.y
        absydif = abs(ydif)

        if xdif != 0 and absxdif == absydif:
            xsign = (xdif > 0) - (xdif < 0)
            ysign = (ydif > 0) - (ydif < 0)

            for i in range(1, absxdif):
                if strboard[self.x + i * xsign][self.y + i * ysign]:
                    return False
            return strboard[newx][newy] == '' or strboard[newx][newy][0] == color_dict[-1 * self.color]

        elif xdif == 0 and ydif != 0:
            ysign = (ydif > 0) - (ydif < 0)

            for i in range(1, absydif):
                if strboard[self.x][self.y + i * ysign]:
                    return False
            return strboard[newx][newy][0] == color_dict[-1 * self.color]

        elif xdif != 0 and ydif == 0:
            xsign = (xdif > 0) - (xdif < 0)

            for i in range(1, absxdif):
                if strboard[self.x + i * xsign][self.y]:
                    return False
            return strboard[newx][newy][0] == color_dict[-1 * self.color]

        return False

    def is_valid_takes(self, strboard, newx, newy):
        return self.is_valid_move(strboard, newx, newy)

    def get_valid_moves(self, strboard):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        valid_moves = []
        for direction in directions:
            xsign, ysign = direction
            newx = self.x + xsign
            newy = self.y + ysign
            while True:
                if 0 <= newx < 8 and 0 <= newy < 8:
                    if strboard[newx][newy]:
                        if strboard[newx][newy][0] != self.colorstr:
                            valid_moves.append((newx, newy))
                        break
                    else:
                        valid_moves.append((newx, newy))
                        newx += xsign
                        newy += ysign
                else:
                    break

        return valid_moves


class King:
    def __init__(self, x, y, color):
        self.move_count = 0
        self.x = x
        self.y = y
        self.color = color
        self.colorstr = color_dict[self.color]
        self.value = None

    def __str__(self):
        return self.colorstr + 'K'

    def increment_move_count(self):
        self.move_count += 1

    def get_move_count(self):
        return self.move_count

    def get_coords(self):
        return self.x, self.y

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def modify_coords(self, newx, newy):
        self.x = newx
        self.y = newy

    def is_valid_move(self, strboard, newx, newy):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        xdif = newx - self.x
        ydif = newy - self.y
        if (xdif, ydif) in directions:
            return not strboard[newx][newy] or strboard[newx][newy][0] != self.colorstr
        return False

    def is_valid_takes(self, strboard, newx, newy):
        return self.is_valid_move(strboard, newx, newy)

    def get_valid_moves(self, strboard):
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        valid_moves = []
        for direction in directions:
            newx = self.x + direction[0]
            newy = self.y + direction[1]
            if 0 <= newx < 8 and 0 <= newy < 8 and (not strboard[newx][newy] or strboard[newx][newy][0] != self.colorstr):
                valid_moves.append((newx, newy))
        return valid_moves



class Chess():

    def __init__(self, setup_method = standard_setup):

        self.Board = setup_method()
        self.turn = 1
        self.check = False
        self.moves = []

        self.play_game()

    def play_again(self, setup_method = standard_setup):

        self.Board = setup_method()
        self.turn = 1
        self.check = False
        self.moves = []

        self.play_game()

    def select_promotion(self, x, y):
        while True:
            inp = input("What piece do you want to promote to (Knight, Bishop, Rook, Queen)? ")
            if inp in {'Knight', 'knight', 'N', 'n'}:
                return Knight(x, y, self.turn)

            elif inp in {'Bishop', 'bishop', 'B', 'b'}:
                return Bishop(x, y, self.turn)

            elif inp in {'Rook', 'rook', 'R', 'r'}:
                return Rook(x, y, self.turn)

            elif inp in {'Queen', 'queen', 'Q', 'q'}:
                return Queen(x, y, self.turn)

            else:
                print("Invalid selection")


    def handle_en_passant(self, piece, x, y, newx, newy):

        piece_type = str(piece)[1]

        if not piece_type == 'P':
            return False

        if ((self.turn == 1 and y == 5) or (self.turn == -1 and y == 2)) and abs(newx - x) == 1 and not self.Board.get_piece(newx, newy):
            if not self.moves or len(self.moves[-1]) != 2:
                print("The piece can't move there")
                return "Continue"

            prev_x, prev_y = chess_to_coords(self.moves[-1])
            prev_piece = self.Board.get_piece(prev_x, prev_y)

            if prev_x != newx or prev_y != y or prev_piece.get_move_count() != 1:
                print("The piece can't move there")
                return "Continue"

            self.Board.move_piece(x, y, newx, newy)
            self.Board.remove_piece(newx, newy - self.turn)
            self.add_move(piece_type, x, y, newx, newy, takes = True)
            return True


        else:
            return False



    def handle_promotion(self, piece, x, y, newx, newy):

        piece_type = str(piece)[1]

        if piece_type == 'P' and ((self.turn == 1 and y == 6) or (self.turn == -1 and y == 1)):
            if not piece.is_valid_move(self.Board.get_strboard(), newx, newy):
                print("The piece can't move there")
                return "Continue"

            takes = self.Board.move_piece(x, y, newx, newy)
            promotion_piece = self.select_promotion(newx, newy)
            self.Board.add_piece(promotion_piece)
            self.add_move(piece_type, x, y, newx, newy, promotion = str(promotion_piece)[1], takes = takes)
            return True

        return False

    def handle_castles(self, piece, x, y, newx, newy):
        piece_type = str(piece)[1]
        xdif = newx - x
        ydif = newy - y
        if piece_type == 'K' and abs(xdif) == 2 and ydif == 0:

            if piece.get_move_count() != 0:
                print("Cannot Castle")
                return "Continue"

            if self.check:
                print("Cannot Castle")
                return "Continue"

            kingside = xdif > 0
            rook_x = kingside * 7

            strboard = self.Board.get_strboard()
            if strboard[rook_x][y] != color_dict[self.turn] + 'R':
                print("Cannot Castle")
                return "Continue"

            in_between = True

            if kingside:
                for newx in range(x + 1, rook_x):
                    if strboard[newx][y] != '':
                        in_between = False
            else:
                for newx in range(rook_x + 1, x):
                    if strboard[newx][y] != '':
                        in_between = False

            if not in_between:
                print("Cannot Castle")
                return "Continue"

            in_between = True

            if kingside:
                for newx in range(x + 1, rook_x):
                    if self.Board.is_check_at(newx, y, self.turn):
                        in_between = False
            else:
                for newx in range(rook_x + 1, x):
                    if self.Board.is_check_at(newx, y, self.turn):
                        in_between = False

            if not in_between:
                print("Cannot Castle")
                return "Continue"

            if kingside:
                move_str = 'K'
            else:
                move_str = 'Q'

            self.Board.move_piece(x, y, newx, newy)
            self.add_move(piece_type, x, y, newx, newy, castles = move_str)
            return True

        else:
            return False

    def handle_normal(self, piece, x, y, newx, newy):

        piece_type = str(piece)[1]

        if not piece.is_valid_move(self.Board.get_strboard(), newx, newy):
            print("The piece can't move there")
            return "Continue"

        takes = self.Board.move_piece(x, y, newx, newy)
        self.add_move(piece_type, x, y, newx, newy, takes = takes)

        return True



    def request_move(self):

        while True:

            inp = input('\nEnter move for %s: ' % name_dict[self.turn])
            if inp == "Resign" or inp == "resign":
                self.end_game(outcome = -1 * self.turn)

            elif inp == "Draw" or inp == "draw":

                if self.accept_draw(-1 * self.turn):
                    self.end_game(outcome = 0)
                else:
                    print("Draw not accepted")

            else:
                if not (len(inp) > 4 and inp[0] in philes and inp[-2] in philes and inp[1] in ranks and inp[-1] in ranks):
                    print('Enter move in format \'e2 to e4\'')
                    continue

                grid1 = inp[:2]
                grid2 = inp[-2:]
                x, y = chess_to_coords(grid1)
                newx, newy = chess_to_coords(grid2)

                piece = self.Board.get_piece(x, y)
                if piece == None or str(piece)[0] != color_dict[self.turn]:
                    print("You don't have a piece there")
                    continue

                location = self.Board.is_pinned(x, y, self.turn)
                if location:
                    if str(piece)[1] == 'N':
                        print("You cannot move into check")
                        continue

                    attack_x, attack_y = location

                    if not in_between(x, y, attack_x, attack_y, newx, newy):
                        print("You cannot move into check")
                        continue

                if self.check:
                    if not self.Board.escapes_check(x, y, newx, newy, self.turn):
                        print("You are in check")
                        continue

                promotion = self.handle_promotion(piece, x, y, newx, newy)
                if promotion == "Continue":
                    continue
                elif promotion:
                    break

                en_passant = self.handle_en_passant(piece, x, y, newx, newy)
                if en_passant == "Continue":
                    continue
                elif en_passant:
                    break

                castles = self.handle_castles(piece, x, y, newx, newy)
                if castles == "Continue":
                    continue
                elif castles:
                    break

                normal = self.handle_normal(piece, x, y, newx, newy)
                if normal != "Continue":
                    break


    def accept_draw(self, side):

        inp = input('Does %s accept the draw (Y/N)?' % name_dict[side])
        if inp in {'Y', 'y', 'Yes', 'yes'}:
            return True
        return False

    def add_move(self, piece_type, x, y, newx, newy, takes = False, castles = False, promotion = False):

        if castles:
            if castles == 'K':
                move_str == 'O-O'
            else:
                move_str == 'O-O-O'
        else:
            if piece_type == 'P':
                if takes:
                    move_str = phile(x) + 'x' + coords_to_chess(newx, newy)
                else:
                    move_str = coords_to_chess(newx, newy)
                if promotion:
                    move_str += '=' + promotion
            else:
                move_str = piece_type
                if takes:
                    move_str += 'x'
                move_str += coords_to_chess(newx, newy)
        self.moves.append(move_str)

    def print_moves(self):

        nmoves = len(self.moves)
        pairs = nmoves // 2
        for i in range(1, pairs + 1):
            print('%d. %s %s' % (i, self.moves[2 * (i - 1)], self.moves[2 * i - 1]))

        if nmoves % 2:
            print('%d. %s' % (pairs + 1, self.moves[-1]))


    def play_game(self):

        while True:
            self.Board.display_board(self.turn)

            self.request_move()

            if self.Board.is_check(-1 * self.turn):
                if self.Board.is_checkmate(-1 * self.turn):

                    self.Board.display_board(self.turn)
                    print("Checkmate")
                    self.moves[-1] = self.moves[-1] + '#'
                    self.end_game(outcome = self.turn)
                    break

                else:
                    print("Check")
                    self.check = True
                    self.moves[-1] = self.moves[-1] + '+'

            elif self.Board.is_stalemate(-1 * self.turn, self.moves):

                self.Board.display_board(self.turn)
                print("Stalemate")
                self.end_game(outcome = 0)
                break

            else:
                self.check = False

            self.turn *= -1


    def end_game(self, outcome):

        if outcome:
            print('Congratulations, %s wins!' % name_dict[outcome])
        else:
            print('A draw was reached.')

        inp = input('Do you want to see the moves (Y/N)? ')
        if inp in {'Y', 'y', 'Yes', 'yes'}:
            self.print_moves()

        inp = input('Do you want to play again (Y/N)? ')
        if inp in {'Y', 'y', 'Yes', 'yes'}:
            self.play_again()
        else:
            print('Game quit')
            quit()



if __name__ == '__main__':
    Chess()
