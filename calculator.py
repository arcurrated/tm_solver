from slau_solver import solve_gauss
from classes import Force, V2, Node

def calculate_simple(forces: list[Force]) -> bool:
    undef_forces_counter = 0

    A = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    b = [0, 0, 0]


    # соответствие индекса в матрице индексу в списке forces
    forces_map = []

    for i, force in enumerate(forces):
        if force.defined:
            m = get_moment(V2(0, 0), force.node.position, force.node.position + force)
            if m is None:
                m = 0
            b[0] = b[0] - force.x # x
            b[1] = b[1] - force.y # y
            b[2] = b[2] - m # moment
        else:
            kof = get_kof(V2(0, 0), force.node.position, force.node.position + force)
            if kof is None:
                kof = 0
            A[0][undef_forces_counter] = force.x/force.norm() # cos
            A[1][undef_forces_counter] = force.y/force.norm() # sin
            A[2][undef_forces_counter] = kof
            forces_map.append(i)
            undef_forces_counter += 1
    
    # смещаем так, чтобы не было нулей на главной диагонали
    for i in range(0, 3):
        if A[i][i] == 0:
            for j in range(i+1, 3):
                if A[j][i] != 0:
                    tmp = A[j]
                    A[j] = A[i]
                    A[i] = tmp
                    tmp = b[j]
                    b[j] = b[i]
                    b[i] = tmp
    
    # todo: удаляем нулевые строки

    x = solve_gauss(A, b)
    if x is None:
        return False
    
    print('from calc: ')
    print(A)
    print(b)
    print(x)
    
    for i, val in enumerate(x):
        orig_f: Force = forces[forces_map[i]]
        norm = orig_f.norm()
        orig_f.x = val * orig_f.x/norm
        orig_f.y = val * orig_f.y/norm
        orig_f.defined = True

    return True

def get_moment(pos1: V2, pos2: V2, pos3: V2):
    # входные аргументы - это вектора с двумя координатами (x, y)
    # 1 - точка отсчета, 2 - начало вектора силы, 3 - конец вектора силы
    
    OA = pos2-pos1
    AB = pos3-pos2
    if OA.norm() == 0 or AB.norm() == 0:
        return None
    # M = a*|F|*(cos(alpha)*cos(beta) - sin(alpha)*sin(beta))
    moment = OA.norm()*AB.norm()*( (OA.x/OA.norm()) * (AB.y/AB.norm()) - (OA.y/OA.norm()) * (AB.x/AB.norm()) )
    return moment

def get_kof(pos1: V2, pos2: V2, pos3: V2):
    # входные аргументы - это вектора с двумя координатами (x, y)
    # 1 - точка отсчета, 2 - начало вектора силы, 3 - конец вектора силы
    # фунция отличается от предыдущей тем, что не включает в расчет
    # величину силы. Это нужно, чтобы определить для матрицы A коэффициент,
    # содержащий лишь плечо и углы расположения этой силы
    
    OA = pos2-pos1
    AB = pos3-pos2
    if OA.norm() == 0 or AB.norm() == 0:
        return None
    # M = a*(cos(alpha)*cos(beta) - sin(alpha)*sin(beta))
    kof = OA.norm()*( (OA.x/OA.norm()) * (AB.y/AB.norm()) - (OA.y/OA.norm()) * (AB.x/AB.norm()) )
    return kof


if __name__ == '__main__':
    n1 = Node(V2(0, 0))
    n2 = Node(V2(5, 0))
    n3 = Node(V2(1, 1))
    n4 = Node(V2(4, 1))

    f1 = Force(n1, 0, 10, defined=False)
    f2 = Force(n2, 10, 0, defined=False)
    f3 = Force(n2, 0, 10, defined=False)
    f4 = Force(n3, 0, -100, defined=True)
    f5 = Force(n4, -120, 0, defined=True)

    tmp = [f1, f2, f3, f4, f5]

    calculate_simple(tmp)

    print("Result")
    for f in tmp:
        print(f)