/*
This file contains part of logic rules used by LogicMem
In the following code, tuples represent the address and value of a field.
for example, in [MM_addr, MM_addr_val], the MM_addr is a candidate address of the mm field, and MM_val 
is the value of that field. 

offset can be calculated by MM_addr - Base_addr

*/
query_task_struct(Base_addr) :-
    statistics(real_time, [Start|_]),
    get_time(Current),
    current_predicate(string_val/1),
    pointer(Ptr),
    string_val(Str),
    int(Int),
    Ptr_profile = ([
        [MM_addr, MM_val],
        [MM2_addr, MM2_val],
        [Tasks_addr, Tasks_val],
        [Tasks2_addr, Tasks2_val],
        [Parent_addr, Parent_val],
        [Real_parent_addr, Real_parent_val],
        [Child_addr, Child_val],
        [Group_leader_addr, Group_leader_val],
        [Thread_group_addr, Thread_group_val],
        [Real_cred_addr, Real_cred_val],
        [Cred_addr, Cred_val],
        [Fs_struct_addr, Fs_struct_val],
        [Files_addr, Files_val]
    ]),
    Str_profile = ([
        [Comm_addr, Comm_val]    
    ]),
    Int_profile = ([
        [Pid_addr, Pid_val],
        [Tgid_addr, Tgid_val]    
    ]),
    
    % adjacency constraints
    MM2_addr #= MM_addr + 8,
    MM2_val #> 0,
    Tasks_addr #> MM2_addr - 100,
    Tasks2_addr #= Tasks_addr + 8,

    Tgid_addr #= Pid_addr + 4,
    Real_parent_addr #< Tgid_addr + 20,
    Real_parent_addr #= Parent_addr - 8,
    Child_addr #= Parent_addr + 8,

    Group_leader_addr #=< Child_addr +32,
    Cred_addr #= Real_cred_addr + 8,
    
    Files_addr #< Comm_addr + 200,
    Files_addr #= FS_struct_addr + 8,
    FS_struct_val #> 0,
    
    % apply order constants
    chain([Tasks_addr, Tasks2_addr, MM_addr, MM2_addr, Pid_addr, Tgid_addr, Real_parent_addr, Parent_addr , Child_addr, 
           Group_leader_addr, Thread_group_addr, Real_cred_addr, Cred_addr, Comm_addr, Fs_struct_addr, Files_addr], #<),

    tuples_in(Ptr_profile, Ptr),
    tuples_in(Str_profile, Str),
    tuples_in(Int_profile, Int),

    label([MM2_addr, MM2_val]),
    label([MM_addr, MM_val]),
    
    % check object type
    query_mm_struct(MM2_val),

    labeling([], [Tasks_addr, Tasks_val, Comm_addr, Comm_val, Pid_addr, Tgid_addr]),

    Comm_offset #= Comm_addr - Base_addr,
    Tasks_offset #= Tasks_addr - Base_addr,
    Tasks_val #> 0,
    query_list_head(Tasks_val, Comm_offset, Tasks_offset),
    

    labeling([enum], [Tasks2_addr, Tasks2_val]),

    labeling([enum], [Real_parent_addr, Real_parent_val, Group_leader_addr, Group_leader_val, Child_addr, Child_val]),
    Real_parent_val #> 0,
    Group_leader_val #> 0,
    query_ts(Real_parent_val, Comm_offset, Tasks_offset),

    labeling([enum], [Real_cred_addr, Real_cred_val, Cred_addr, Cred_val]),
    Cred_val #> 0,
    query_cred(Real_cred_val),
    query_cred(Cred_val),


    label([Fs_struct_addr, Fs_struct_val, Files_addr, Files_val]),
    query_fs_struct(Fs_struct_val),

    get_time(Now),
    Time_past is Now - Current,
    statistics(real_time, [End|_]),

    log("./profile/task_struct", "tasks", Tasks_addr, Base_addr),
    log("./profile/task_struct", "mm", MM_addr, Base_addr),
    log("./profile/task_struct", "active_mm", MM2_addr, Base_addr),
    log("./profile/task_struct", "comm", Comm_addr, Base_addr),
    log("./profile/task_struct", "parent", Parent_addr, Base_addr),
    log("./profile/task_struct", "group_leader", Group_leader_addr, Base_addr),
    log("./profile/task_struct", "cred", Cred_addr, Base_addr),
    log("./profile/task_struct", "pid", Pid_addr, Base_addr),
    log("./profile/task_struct", "fs_struct", Fs_struct_addr, Base_addr),
    log("./profile/task_struct", "files", Files_addr, Base_addr),

    log("./profile/task_struct", "task_struct time", End, Start).

possible_mm_struct(Current_addr) :- 
    statistics(real_time, [Start|_]),
    pointer(Ptr),
    long(Ulg),

    Ptr_profile = [
        [Mmap_addr, Mmap_val],
        [Pgd_addr, Pgd_val]  
    ],
    Ulong_profile = [
        [Mmap_base_addr, Mmap_base_val],
        [Task_size_addr, Task_size_val],
        [Start_brk_addr, Start_brk_val],
        [Brk_addr, Brk_val],
        [Start_stack_addr, Start_stack_val],
        [ARG_start_addr, ARG_start_val],
        [ARG_end_addr, ARG_end_val],
        [ENV_start_addr, ENV_start_val],
        [ENV_start_addr, ENV_start_val]
    ],
    Mmap_addr #= Current_addr,
    Mmap_base_val #> 0x7f0000000000,
    chain([Mmap_addr, Mmap_base_addr, Task_size_addr, Pgd_addr], #<),
    Pgd_addr #> Task_size_addr,
    Pgd_addr #=< Task_size_addr + 40,
    
    Start_brk_addr #> Pgd_addr,
    Start_stack_val #> Mmap_base_val,
    ARG_start_addr #< Current_addr + 500,
    ARG_end_addr #= ARG_start_addr + 8,
    ENV_end_addr #= ENV_start_addr + 8,
    ARG_start_val #> Start_stack_val,
    ARG_start_val #< ARG_end_val,
    ENV_start_val #>= ARG_end_val,
    ENV_end_val #>= ENV_start_val,

    chain([Start_brk_addr, Brk_addr, Start_stack_addr, ARG_start_addr], #<),
    
    tuples_in(Ptr_profile, Ptr),
    tuples_in(Ulong_profile, Ulg),

    Mmap_val #> 0,
    Pgd_val #> 0,
    labeling([enum], [Mmap_addr, Mmap_val, Mmap_base_addr, Pgd_addr, Pgd_val]),
    
    % object type constraint: mmap should point to a vm_area_struct object
    process_create(path('python'),
                    ['subquery.py', Mmap_val, "vm_area_struct", Current_addr],
                    [stdout(pipe(In))]),
    
    print(In),
    read_string(In, Len, X),
    string_codes(X, Result),
    close(In),
    isTrue(Result),
    label([Start_brk_addr, Brk_addr, Start_stack_addr, ARG_start_addr]),
    statistics(real_time, [End|_]),

    log("./profile/mm_struct", "mmap", Mmap_addr, Current_addr),
    log("./profile/mm_struct", "mmap_base", Mmap_base_addr, Current_addr),
    log("./profile/mm_struct", "pgd", Pgd_addr, Current_addr),
    log("./profile/mm_struct", "start_brk", Start_brk_addr, Current_addr),
    log("./profile/mm_struct", "brk", Brk_addr, Current_addr),
    log("./profile/mm_struct", "start_stack", Start_stack_addr, Current_addr),
    log("./profile/mm_struct", "arg_start", ARG_start_addr, Current_addr),
    log("./profile/mm_struct", "arg_end", ARG_end_addr, Current_addr),
    log("./profile/mm_struct", "env_start", ENV_start_addr, Current_addr),
    log("./profile/mm_struct", "env_end", ENV_end_addr, Current_addr),

    log("./profile/mm_struct", "mm_struct time", End, Start).


possible_vm_area_struct(Base_addr, MM_addr) :-
    statistics(real_time, [Start|_]),
    pointer(Ptr),
    long(Ulg),
    int(Int),
    Ptr_profile = [
        [VM_next_addr, VM_next_val],
        [Vm_mm_addr, Vm_mm_val],
        [VM_file_addr, VM_file_val]
    ],
    Ulong_profile = [
        [VM_start_addr, VM_start_val],
        [VM_end_addr, VM_end_val],
        [VM_flag_addr, VM_flag_val],
        [VM_pgoff_addr, VM_pgoff_val]
    ],
    Int_profile = [
        [Vm_page_prot_addr, Vm_page_prot_val]
    ],
    VM_start_addr #>= Base_addr,
    chain([VM_start_addr, VM_end_addr, VM_next_addr, Vm_mm_addr, Vm_page_prot_addr, VM_flag_addr, VM_file_addr], #<),
    VM_end_addr #= VM_start_addr + 8,
    VM_next_addr #= VM_end_addr + 8,
    VM_next_addr #< Base_addr + 32,
    
    VM_file_addr #< Base_addr + 180,
    VM_pgoff_addr #= VM_file_addr - 8,
    VM_flag_addr #=< Vm_page_prot_addr + 8,

    VM_READ #= 0x00000001,
    VM_WRITE #= 0x00000002,
    VM_EXEC #= 0x00000004,
    VM_SHARED #= 0x00000008,

    VM_MAYREAD #= 0x00000010,
    VM_MAYWRITE #= 0x00000020,
    VM_MAYEXEC #= 0x00000040,
    VM_MAYSHARED #= 0x00000080,
    
    %bitwise and operation
    VM_flag_val /\ VM_READ #= VM_flag_val /\ VM_MAYREAD,
    VM_flag_val /\ VM_WRITE #= VM_flag_val /\ VM_MAYWRITE,
    VM_flag_val /\ VM_EXEC #= VM_flag_val /\ VM_MAYEXEC,
    VM_flag_val /\ VM_SHARED #= VM_flag_val /\ VM_MAYSHARED,

    VM_file_addr #< Base_addr + 200,

    tuples_in(Ptr_profile, Ptr),
    tuples_in(Ulong_profile, Ulg),
    tuples_in(Int_profile, Int),

    label([VM_next_addr, VM_next_val]),
    labeling([enum], [VM_start_addr, VM_end_addr, Vm_mm_addr, Vm_mm_val, VM_flag_addr, VM_pgoff_addr, VM_file_addr, VM_file_val]),
    
    VM_file_val #> 0,
    process_create(path('python'),
                ['subquery.py', VM_file_val, "vm_file"],
                [stdout(pipe(In))]),
    read_string(In, Len, X),
    string_codes(X, Result),
    close(In),
    isTrue(Result),
    statistics(real_time, [End|_]),
    label([VM_flag_val]),

    log("./profile/vm_area_struct", "vm_start", VM_start_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_end", VM_end_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_next", VM_next_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_mm", Vm_mm_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_flag", VM_flag_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_flag value", VM_flag_val, 0),
    log("./profile/vm_area_struct", "vm_pgoff", VM_pgoff_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_file", VM_file_addr, Base_addr),
    log("./profile/vm_area_struct", "vm_area_struct time", End, Start).