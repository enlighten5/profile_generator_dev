from constraint import *
import memoryReader as mr
import sys
pointers = {
    1: 920902048,
    2: 920478224,
    3: 920211665,
    4: 920900320,
    5: 920903312,
    6: 921813888,
    7: 921577801
}
pointer_field = [
    [1, 100],
    [2, 99],
    [3, 102],
    [4, 103],
    [5, 105],
    [9, 105]
]

string_field = [
    [1, 'swapper']
]

integer_field = [
    [1, 1],
    [2, 1]
]
def mm_struct(p):
    if p == 1352743728:
        return True
def task_struct(problem, base_addr, facts):
    #pointers = ['mm', 'active_mm', 'tasks', 'tasks2', 'parent', 'real_parent', 'child', 'group_leader',
    #          'thread_group', 'real_cred', 'cred', 'fs_struct', 'files']
    pointers = ['mm', 'active_mm', 'tasks', 'parent', 'real_parent', 'child', 'group_leader']
    problem.addVariables(pointers, facts['pointers'])
    #problem.addVariable('mm', facts['pointers'])
    #problem.addVariable('active_mm', facts['pointers'])

    strings = ['comm']
    problem.addVariables(strings, facts['strings'])

    #integers = ['pid', 'tgid']
    #problem.addVariables(integers, facts['integers'])

    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('mm', 'active_mm'))
    problem.addConstraint(lambda a, b=1000: a[0] > b, ('active_mm',))
    problem.addConstraint(lambda a, b=0: a[1]!=b, ('mm',))
    problem.addConstraint(lambda a, b=0: a[1]!=b, ('active_mm',))
    problem.addConstraint(lambda a, b=True: mm_struct(a[1])==b, ('active_mm',))
    problem.addConstraint(lambda a, b: a[0] < b[0], ('tasks', 'active_mm'))
    problem.addConstraint(lambda a, b: a[0] > b[0]-100, ('tasks', 'active_mm'))
    problem.addConstraint(lambda a, b=0: a[1]!=b, ('tasks',))
    problem.addConstraint(lambda a, b=0: a[1]!=b, ('parent',))
    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('parent', 'real_parent'))
    problem.addConstraint(lambda a, b: b[0] > a[0], ('active_mm', 'parent'))
    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('real_parent', 'child'))
    problem.addConstraint(lambda a, b: b[0] < a[0] + 32, ('child', 'group_leader'))
    problem.addConstraint(lambda a, b: b[0] > a[0], ('child', 'group_leader'))
    problem.addConstraint(lambda a, b: b[0] > a[0], ('child', 'comm'))
    problem.addConstraint(lambda a, b=2: len(a[1]) > b, ('comm', ))

    '''

    problem.addConstraint(lambda a, b: a[0] > b[0] - 100, ('tasks', 'active_mm'))
    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('tasks', 'tasks2'))
    #problem.addConstraint(lambda a, b: b[0] == a[0] + 4, ('pid', 'tgid'))
    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('parent', 'real_parent'))
    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('real_parent', 'child'))
    problem.addConstraint(lambda a, b: b[0] < a[0] + 32, ('child', 'group_leader'))
    problem.addConstraint(lambda a, b: b[0] == a[0] + 8, ('real_cred', 'cred'))
    problem.addConstraint(lambda a, b=2400: a[0] < b, ('cred',))
    '''
    #problem.addConstraint(lambda a, b: b[0] > a[0], ('cred', 'comm'))
    
    solutions = problem.getSolutions()
    for item in solutions:
        print(item)

def test():
    problem = Problem()
    f = ['field_a', 'field_b']
    problem.addVariables(f, pointer_field)
    #problem.addVariable('field_a', pointer_field)
    #problem.addVariable('field_b', pointer_field)
    problem.addConstraint(lambda a, b: a[0] < b[0],
                            ("field_a", "field_b"))
    problem.addConstraint(lambda a, b: a[1] > b[1],
                            ("field_a", "field_b"))
    solutions = problem.getSolutions()
    print(solutions)
    #for item in solutions:
    #    print(item['field_a'])

def main():
    mem_path = sys.argv[1]
    addr_space = mr.AddressSpace(mem_path, 0x50a0a000)
    facts = addr_space.extract_facts(1352742720)
    problem = Problem(BacktrackingSolver())
    task_struct(problem, 1352742720, facts)
    #print(facts['pointers'])



if __name__ == "__main__":
    main()

