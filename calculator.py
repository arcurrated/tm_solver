from slau_solver import solve_gauss
from classes import Force, V2, Node, Rod

def calculate_farm(rods: list[Rod], ex_forces: list[Force]) -> bool:
    # находим глобальные неизвестные (реакции)
    calculate_simple(ex_forces)

    # находим все задействованные ноды
    nodes = []
    for rod in rods:
        # flush defined flag
        rod.inner_force_defined = False
        for n in rod.nodes:
            if n not in nodes:
                nodes.append(n)

    while True:
        if len(nodes) == 0:
            break
        # take node
        curr_node = nodes.pop()
        # find external forces acting on node
        forces: list[Force] = []
        for force in ex_forces:
            if force.node == curr_node:
                forces.append(force)

        # find rods connected with node and add co-directed force
        rods_map: list[tuple[int]] = [] 
        # rods map - variable with tuples like (forces_index, fods_index, k)
        # for after-calculation force assignment
        c = 0 # counter of undefined forces
        for rod in rods:
            if curr_node in rod.nodes:
                k = 1 # if co-directed
                if curr_node == rod.nodes[1]:
                    # opposite directed
                    k = -1
                rods_map.append((len(forces), rods.index(rod), k))
                if not rod.inner_force_defined:
                    c += 1
                forces.append(Force(curr_node, 
                                    k * rod.inner_force.x, 
                                    k * rod.inner_force.y, 
                                    defined=rod.inner_force_defined))
        if c > 2:
            # undefined forces more than 2, wa cannot solve this system.
            # maybe later with other nodes we will calculate some rod inner forces...
            # we will try again and again
            nodes.insert(0, curr_node)
            continue
            # once we have to stop it, but not today. Today we loops forever

        res: bool = calculate_simple(forces)
        if not res:
            print("ERROR! UB UB UB")
            return False
        
        # propagate forces
        # el[2] is k koff which defined direction of force.
        # system solves relatively this node, but if this is a second node of rod, we must reverse it
        # we have to store force as the force from first node of rod to second
        for el in rods_map:
            rods[el[1]].inner_force.x = forces[el[0]].x * el[2]
            rods[el[1]].inner_force.y = forces[el[0]].y * el[2]
            rods[el[1]].inner_force_defined = True

    return True

def calculate_simple(forces: list[Force]) -> bool:
    '''
        Найти неопределенные силы. Возвращает успех/неудача
    '''
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
    
    # удаляем нулевые строки и столбцы
    i = 0
    length = len(A)
    while i < length:
        if A[i][i] == 0:
            del b[i]
            for j in range(0, length):
                del A[j][i]
            del A[i]
            i -= 1
            length -= 1
        i += 1

    x = solve_gauss(A, b)
    if x is None:
        return False

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
    print('Test simple: ')
    n1 = Node(V2(0, 0))
    n2 = Node(V2(5, 0))
    n3 = Node(V2(1, 1))
    n4 = Node(V2(4, 1))

    f1 = Force(n1, 0, 10, defined=False)
    f2 = Force(n2, 10, 0, defined=False)
    f3 = Force(n2, 0, 10, defined=False)

    f4 = Force(n3, 0, -100, defined=True)
    f5 = Force(n4, -120, 0, defined=True)

    forces = [f1, f2, f3, f4, f5]

    calculate_simple(forces)

    print("Result")
    for f in forces:
        print(f)

    print('Test farm: ')
    n1 = Node(V2(0, 0), title='A') # A
    n2 = Node(V2(0, 15), title='B') # B
    n3 = Node(V2(10, 10), title='C') # C
    n4 = Node(V2(10, 0), title='D') # D
    n5 = Node(V2(20, 5), title='E') # E

    f1 = Force(n1, 0, 10, defined=False)
    f2 = Force(n1, 10, 0, defined=False)
    f3 = Force(n2, 10, 0, defined=False)

    f4 = Force(n5, 0, -150, defined=True)
    # f5 = Force(n4, -120, 0, defined=True)
    # todo: debug!

    r1 = Rod(n1, n2)
    r2 = Rod(n1, n4)
    r3 = Rod(n2, n3)
    r4 = Rod(n2, n4)
    r5 = Rod(n3, n4)
    r6 = Rod(n5, n3)
    r7 = Rod(n5, n4)

    forces = [f1, f2, f3, f4]
    rods = [r1, r2, r3, r4, r5, r6, r7]
    

    calculate_farm(rods, forces)

    print("Result")
    for f in forces:
        print(f)
    for r in rods:
        print(r)
