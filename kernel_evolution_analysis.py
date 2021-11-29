import os
import re
import random

versions1 = ["v4.11", "v4.12", "v4.13", "v4.14", "v4.15", "v4.16", "v4.17", "v4.18", "v4.19", "v4.20", "v5.0", "v5.1", "v5.2", "v5.3", "v5.4", "v5.5"]
versions2 = ["v3.11", "v3.12", "v3.13", "v3.14", "v3.15", "v3.16", "v3.17", "v3.18", "v3.19"]
versions3 = ["v4.0", "v4.1", "v4.2", "v4.3", "v4.4", "v4.5", "v4.6", "v4.7", "v4.8", "v4.9", "v4.10"]
versions4 = ["v3.0", "v3.1", "v3.2", "v3.3", "v3.4", "v3.5", "v3.6", "v3.7", "v3.8", "v3.9", "v3.10"]
versions = versions4 + versions2 + versions3 + versions1
key_start = {
    "task_struct": "struct task_struct {",
    "mm_struct": "struct mm_struct {",
    "vm_area_struct": "struct vm_area_struct {",
    "fs_struct": "struct fs_struct {",
    "kernel_param": "struct kernel_param {",
    "kparam_array": "struct kparam_array",
    "mount": "struct mount {",
    "dentry": "struct dentry {",
    "neigh_table": "struct neigh_table {",
    "neigh_hash_table": "struct neigh_hash_table {",
    "neighbour": "struct neighbour {",
    "net_device": "struct net_device {",
    "in_ifaddr": "struct in_ifaddr {",
    "socket": "struct socket {",
    "sock": "struct sock {",
    "inet_sock": "struct inet_sock {",
    "resource": "struct resource {",
    "in_device": "struct in_device {",
    "pid": "struct pid",
    "fdtable": "struct fdtable {",
    "files_struct": "struct files_struct {",
    "file": "struct file {",
    "tty_driver": "struct tty_driver {",
    "proc_dir_entry": "struct proc_dir_entry {",
    "nsproxy": "struct nsproxy {",
    "gate_struct64": "struct gate_struct64 {",
    "kset": "struct kset {",
    "kobject": "struct kobject {",
    "module_kobject": "struct module_kobject {",
    "inode": "struct inode {",
    "module": "struct module",
    "vfsmount": "struct vfsmount {",
    'timekeeper': "struct timekeeper {", "pid_namespace": 'struct pid_namespace {', 'pid': 'struct pid', 'qstr': 'struct qstr',
    'seq_operations': 'struct seq_operations', 'tty_struct': 'struct tty_struct',
    'file_operations': 'struct file_operations', 'rb_root': 'struct rb_root', 'file_system_type': 'struct file_system_type',
    'kref': 'struct kref',
    'ipv6_pinfo': 'struct ipv6_pinfo',
    'unix_sock': 'struct unix_sock', 'sockaddr_un': 'struct sockaddr_un',
    'cpuinfo_x86': 'struct cpuinfo_x86', 'radix_tree_node': 'struct radix_tree_node', 'tcp_seq_afinfo': 'struct tcp_seq_afinfo',
    'udp_seq_afinfo': 'struct udp_seq_afinfo', 'hlist_head': 'struct hlist_head', 'upid': 'struct upid', 'hlist_node': 'struct hlist_node',
    'rb_node': 'struct rb_node', 'sock_common': 'struct sock_common', 'unix_address': 'struct unix_address', 'in6_addr': 'struct in6_addr',
    'super_block': 'struct super_block', 'pid_link': 'struct pid_link', 'tty_ldisc': 'struct tty_ldisc', 'module_layout': 'struct module_layout',
    'cred': 'struct cred'
}

file_name = {
    "task_struct": "/include/linux/sched.h",
    "mm_struct": "/include/linux/mm_types.h",
    "vm_area_struct": "/include/linux/mm_types.h",
    "fs_struct": "/include/linux/fs_struct.h",
    "kernel_param": "/include/linux/moduleparam.h",
    "kparam_array": "/include/linux/moduleparam.h",
    "mount": "/fs/mount.h",
    "dentry": "/include/linux/dcache.h",
    "neigh_table": "/include/net/neighbour.h",
    "neigh_hash_table": "/include/net/neighbour.h",
    "neighbour": "/include/net/neighbour.h",
    "net_device": "/include/linux/netdevice.h",
    "in_ifaddr": "/include/linux/inetdevice.h",
    "socket": "/include/linux/net.h",
    "sock": "/include/net/sock.h",
    "inet_sock": "/include/net/inet_sock.h",
    "resource": "/include/linux/ioport.h",
    "in_device": "/include/linux/inetdevice.h",
    "pid": "/include/linux/pid.h",
    "fdtable": "/include/linux/fdtable.h",
    "files_struct": "/include/linux/fdtable.h",
    "file": "/include/linux/fs.h",
    "tty_driver": "/include/linux/tty_driver.h",
    "proc_dir_entry": "/fs/proc/internal.h",
    "nsproxy": "/include/linux/nsproxy.h",
    "gate_struct64": "/arch/x86/include/asm/desc_defs.h",
    "kset": "/include/linux/kobject.h",
    "kobject": "/include/linux/kobject.h",
    "module_kobject": "/include/linux/module.h",
    "inode": "/include/linux/fs.h",
    "module": "/include/linux/module.h",
    "vfsmount": "/include/linux/mount.h",
    'timekeeper': '/include/linux/timekeeper_internal.h', "pid_namespace": '/include/linux/pid_namespace.h', 'pid': '/include/linux/pid.h',
    'qstr': '/include/linux/dcache.h', 'seq_operations': '/include/linux/seq_file.h', 'tty_struct': '/include/linux/tty.h',
    'file_operations': '/include/linux/fs.h', 'rb_root': '/include/linux/rbtree.h', 'file_system_type': '/include/linux/fs.h',
    'kref': '/include/linux/kref.h',
    'ipv6_pinfo': '/include/linux/ipv6.h',
    'unix_sock': '/include/net/af_unix.h',
    'sockaddr_un': '/include/uapi/linux/un.h', 'cpuinfo_x86': '/arch/x86/include/asm/processor.h',
    'radix_tree_node': '/include/linux/radix-tree.h',
    'tcp_seq_afinfo': '/include/net/tcp.h', 'udp_seq_afinfo': '/include/net/udp.h', 'hlist_head': '/include/linux/types.h',
    'upid': '/include/linux/pid.h', 'hlist_node': '/include/linux/types.h', 'rb_node': '/include/linux/rbtree.h',
    'sock_common': '/include/net/sock.h', 'unix_address': '/include/net/af_unix.h', 'in6_addr': '/include/uapi/linux/in6.h',
    'super_block': '/include/linux/fs.h', 'pid_link': '/include/linux/pid.h', 'tty_ldisc': '/include/linux/tty_ldisc.h',
    'module_layout': '/include/linux/module.h',
    'cred': '/include/linux/cred.h'

}
all_accessed_object = [
    'task_struct', 'list_head', 'timekeeper', 'pid_namespace', 'pid', 'file', 'dentry', 'qstr',
    'vfsmount', 'mount', 'inode', 'vm_area_struct', 'mm_struct', 'module', 'module_layout', 'seq_operations', 'tty_driver',
    'tty_struct', 'proc_dir_entry', 'file_operations', 'rb_root', 'file_system_type', 'kset', 'kobject',
    'module_kobject', 'kref', 'neigh_table', 'neigh_hash_table', 'neighbour', 'net_device', 'in_device', 'in_ifaddr',
    'socket', 'inet_sock', 'sock', 'ipv6_pinfo', 'unix_sock', 'sockaddr_un', 'cpuinfo_x86', 'resource',
    'radix_tree_node', 'files_struct', 'tcp_seq_afinfo', 'udp_seq_afinfo', 'hlist_head', 'upid', 'hlist_node',
    'rb_node', 'sock_common', 'unix_address', 'in6_addr', 'super_block', 'pid_link', 'fs_struct', 'tty_ldisc'
]
key_end = {
    "task_struct": "};",
    "mm_struct": "} __randomize_layout;",
    "vm_area_struct": "} __randomize_layout;",
    "fs_struct": "} __randomize_layout;",
    "kernel_param": "};",
    "kparam_array": "};",
    "mount": "};",
    "dentry": "};",
    "neigh_table": "};",
    "neigh_hash_table": "};",
    "neighbour": "};",
    "net_device": "};",
    "in_ifaddr": "};",
    "socket": "};",
    "sock": "};",
    "inet_sock": "};",
    "resource": "};",
    "in_device": "};",
    "pid": "};",
    "fdtable": "};",
    "files_struct": "};",
    "file": "}",
    "tty_driver": "};",
    "proc_dir_entry": "};",
    "nsproxy": "};",
    "gate_struct64": "}",
    "kset": "}",
    "kobject": "}",
    "module_kobject": "}",
    "inode": "}",
    "module": "}",
    "vfsmount": "}"
}
tmp = [
    'tasks', 'next', 'parent', 'cred', 'uid', 'val', 'gid', 'real_start_time', 'wall_to_monotonic', 'offs_real', 'offs_boot',
    'tv_sec', 'tv_nsec', 'mm', 'pgd', 'comm', 'arg_start', 'arg_end', 'euid', 'children', 'sibling', 'idr', 'idr_rt', 'xa_head',
    'shift', 'slots', 'first', 'pid_links', 'real_parent', 'group_leader', 'exit_state', 'files', 'fdt', 'fd', 'max_fds', 'f_path',
    'd_op', 'd_dname', 'fs', 'root', 'mnt', 'd_inode', 'd_name', 'name', 'mnt_root', 'd_parent', 'mnt_parent', 'mnt_mountpoint',
    'i_ino', 'mmap', 'vm_start', 'vm_end', 'vm_pgoff', 'mmap_base', 'vm_file', 'i_sb', 's_dev', 'vm_flags', 'vm_next', 'brk',
    'start_brk', 'start_stack', 'vm_mm', 'context', 'vdso', 'module', 'core_layout', 'base', 'size', 'list', 'tcp_seq_afinfo',
    'start', 'stop', 'show', 'ttys', 'num', 'tty_drivers', 'ldisc', 'ops', 'receive_buf', 'f_op', 'lock', 'iterate_shared',
    'iopoll', 'compat_ioctl', 'llseek', 'flush', 'flock', 'poll', 'open', 'fadvise', 'remap_file_range', 'write', 'read',
    'setlease', 'fasync', 'fallocate', 'sendpage', 'write_iter', 'read_iter', 'splice_read', 'show_fdinfo', 'iterate',
    'splice_write', 'copy_file_range', 'unlocked_ioctl', 'fsync', 'get_unmapped_area', 'release', 'check_flags', 'nsproxy',
    'pid_ns_for_children', 'proc_mnt', 'i_fop', 'd_child', 'd_subdirs', 'proc_fops', 'subdir_node', 'subdir', 'rb_node',
    'proc_net', 'mnt_hash', 'mnt_child', 'mnt_devname', 'mnt_list', 'mnt_sb', 's_type', 's_root', 'mnt_flags', 's_flags',
    'i_mode', 'latch_tree_root', 'state', 'text_size', 'kobject', 'mod', 'entry', 'refcount', 'refs', 'counter', 'nht',
    'hash_shift', 'hash_buckets', 'dev', 'ip_ptr', 'tbl', 'family', 'primary_key', 'ha', 'addr_len', 'dev_base_head',
    'perm_addr', 'dev_addr', 'flags', 'ifa_list', 'ifa_address', 'ifa_label', 'ifa_next', 'dev_list', 'sk', 'sk_protocol',
    '_task_struct__sk_common', 'skc_family', '_inet_sock__sk_common', 'pinet6', 'saddr', 'addr', 'sun_path', 'inet_sport',
    '__sk_common', 'skc_portpair', 'skc_rcv_saddr', 'skc_daddr', 'skc_state', 'skc_v6_daddr', 'x86_vendor_id', 'x86_model_id',
    'ts_nsec', 'len', 'text_len', 'child', 'end', 'mnt_ns', 'owner', 'radix_tree_root', 'rnode', 'pids', 'seq_fops',
    'dedupe_file_range', 'mmap_supported_flags', 'clone_file_range', 'seq_ops', 'tty_driver', 'rb_left', 'rb_right', 'namelen', 'kref',
    'pid_link', 'numbers', 'hlist_node', 'pid_chain', 'pprev', 'net', 'setfl'
]

all_accessed_field = [
    'tasks', 'next', 'parent', 'uid', 'val', 'gid', 'real_start_time', 'wall_to_monotonic', 'offs_real', 'offs_boot',
    'tv_sec', 'tv_nsec', 'mm', 'pgd', 'comm', 'arg_start', 'arg_end', 'euid', 'children', 'sibling', 'idr', 'idr_rt', 'xa_head',
    'shift', 'slots', 'first', 'pid_links', 'real_parent', 'group_leader', 'exit_state', 'files', 'fdt', 'fd', 'max_fds', 'f_path',
    'd_op', 'd_dname', 'fs', 'root', 'mnt', 'd_inode', 'd_name', 'name', 'mnt_root', 'd_parent', 'mnt_parent', 'mnt_mountpoint',
    'i_ino', 'mmap', 'vm_start', 'vm_end', 'vm_pgoff', 'mmap_base', 'vm_file', 'i_sb', 's_dev', 'vm_flags', 'vm_next', 'brk',
    'start_brk', 'start_stack', 'vm_mm', 'context', 'vdso', 'module', 'core_layout', 'base', 'size', 'list', 'tcp_seq_afinfo',
    'start', 'stop', 'show', 'ttys', 'num', 'tty_drivers', 'ldisc', 'ops', 'receive_buf', 'f_op', 'lock', 'iterate_shared',
    'iopoll', 'compat_ioctl', 'llseek', 'flush', 'flock', 'poll', 'open', 'fadvise', 'remap_file_range', 'write', 'read',
    'setlease', 'fasync', 'fallocate', 'sendpage', 'write_iter', 'read_iter', 'splice_read', 'show_fdinfo', 'iterate', 'splice_write',
    'copy_file_range', 'unlocked_ioctl', 'fsync', 'get_unmapped_area', 'release', 'check_flags', 'nsproxy', 'pid_ns_for_children',
    'proc_mnt', 'i_fop', 'd_child', 'd_subdirs', 'proc_fops', 'subdir_node', 'subdir', 'rb_node', 'proc_net', 'mnt_hash', 'mnt_child',
    'mnt_devname', 'mnt_list', 'mnt_sb', 's_type', 's_root', 'mnt_flags', 's_flags', 'i_mode', 'latch_tree_root', 'state', 'text_size',
    'kobject', 'mod', 'entry', 'refcount', 'refs', 'counter', 'nht', 'hash_shift', 'hash_buckets', 'dev', 'ip_ptr', 'tbl', 'family',
    'primary_key', 'ha', 'addr_len', 'dev_base_head', 'perm_addr', 'dev_addr', 'flags', 'ifa_list', 'ifa_address', 'ifa_label', 'ifa_next',
    'dev_list', 'sk', 'sk_protocol', '_task_struct__sk_common', 'skc_family', '_inet_sock__sk_common', 'pinet6', 'saddr', 'addr',
    'sun_path', 'inet_sport', '__sk_common', 'skc_portpair', 'skc_rcv_saddr', 'skc_daddr', 'skc_state', 'skc_v6_daddr', 'x86_vendor_id',
    'x86_model_id', 'ts_nsec', 'len', 'text_len', 'child', 'end', 'mnt_ns', 'p_filINFO', 'owner', 'radix_tree_root', 'rnode', 'pids',
    'seq_fops', 'dedupe_file_range', 'mmap_supported_flags', 'clone_file_range', 'seq_ops', 'tty_driver', 'rb_left', 'rb_right', 'namelen',
    'pid_link', 'numbers', 'hlist_node', 'pid_chain', 'pprev', 'total_sleep_time', 'line', 'timestamp', 'init_size', 'core_size',
    'module_core', 'aio_read', 'aio_write', 'aio_fsync', 'd_u', 'core_text_size', 'tv64', 'init_layout', 'address', 'net', 'readdir',
    'pid_ns', 'vfsmount', 'chain', 'dst', 'rt_next', 'rt_dst', 'rt_gateway', 'inet_dport', 'daddr', 'setfl'
]

def process_configuration(struct_name, version):
    file_name = version
    configs = []
    with open(file_name, 'r') as f:
        tmp = f.read()
        tmp = tmp.split('\n')
        for index in range(len(tmp)):
            if " CONFIG_" in tmp[index]:
                content = tmp[index] + ' '
                tmp_idx = content.index("CONFIG_")
                tmp_idx2 = tmp_idx
                while content[tmp_idx2].isupper() or content[tmp_idx2] == '_':
                    tmp_idx2 += 1
                if content[tmp_idx:tmp_idx2] not in configs:
                    configs.append(content[tmp_idx:tmp_idx2])
    with open(file_name+"_config", 'w') as f:
        for item in configs:
            f.write(item+'\n')
    return configs

def download(struct_name):
    for v in versions:
        link = " https://raw.githubusercontent.com/torvalds/linux/" + v + file_name[struct_name]
        if not os.path.exists(v):
            os.system("wget -O " + v + link)

object_diff = []
objects = {}
all_field_in_config = []
def find_config(struct_name):
    for v in versions:
        file_name = v
        ts_struct = []
        ts_token = []
        current_line = 0
        ts_line = 0
        count = 0
        with open(file_name, 'r') as f:
            tmp = f.read()
            tmp = tmp.split('\n')
            if key_start[struct_name] in tmp:
                idx1 = tmp.index(key_start[struct_name])
            elif key_start[struct_name]+' {' in tmp:
                idx1 = tmp.index(key_start[struct_name]+' {')
            else:
                return
            idx2 = 0
            for index in range(idx1, len(tmp)):
                if '{' in tmp[index]:
                    count += 1
                if '}' in tmp[index]:
                    count -= 1
                if count == 0:
                    idx2 = index
                    break
            content = tmp[idx1: idx2+1]
            flag = 0
            config = []
            for index in range(len(content)):
                idx1 = 0
                idx2 = 0
                if '#if' in content[index]:
                    flag = 1
                    continue
                if '#endif' in content[index]:
                    flag = 0
                    continue
                if flag == 1:
                    all_field_in_config.append(content[index])

def process_file(struct_name):
    for v in versions:
        file_name = v
        ts_struct = []
        ts_token = []
        current_line = 0
        ts_line = 0
        count = 0
        with open(file_name, 'r') as f:
            line = f.readline()
            while line:
                current_line += 1
                if line.strip() == key_start[struct_name] or line.startswith(key_start[struct_name]+' {'):
                    ts_line = current_line
                if ts_line:
                    line = line.strip()
                    if "{" in line:
                        count += 1
                    if "}" in line:
                        count -= 1
                    # Parse function pointer
                    if '(*' in line:
                        content = line[:line.index(')')]
                        while not ');' in line:
                            line = f.readline()
                        line = content + ';'

                    if ";" not in line:
                        line = f.readline()
                        continue
                    if ';' in line and '}' in line and not count == 0:
                        line = f.readline()
                        continue
                    line = line.split(';')[0]

                    # Unfold field definitions in one line
                    if ',' in line:
                        tmp_line = re.split(' |\t', line)
                        while '' in tmp_line:
                            tmp_line.remove('')
                        first_field_idx = 0
                        for idx in range(len(tmp_line)):
                            if ',' in tmp_line[idx]:
                                first_field_idx = idx
                                break
                        for item in tmp_line[first_field_idx:]:
                            new_line = ''
                            for i in tmp_line[:first_field_idx]:
                                new_line += str(i) + ' '
                            new_line += str(item.strip(','))

                            field_def, token = process_token(new_line)
                            ts_token.append(token)
                    else:
                        field_def, token = process_token(line)
                        ts_struct.append(field_def)
                        ts_token.append(token)
                    if "}" in line and count == 0:
                        break
                line = f.readline()
        token_remove_redudant = []
        for item in ts_token:
            if item not in token_remove_redudant:
                token_remove_redudant.append(item)
        objects[file_name] = token_remove_redudant
        #with open(file_name, 'w') as f:
        #    for value in ts_struct:
        #        f.write(value + '\n')
def process_token(line):
    token = re.split(' |\t', line)
    while '' in token:
        token.remove('')
    #Remove attributes
    for index in range(len(token)):
        if '__' in token[index] and index > 0:
            del token[index]
            break
    #Remove const symbol
    for index in range(len(token)):
        if 'const' in token[index]:
            del token[index]
            break
    #Remove unsigned
    for index in range(len(token)):
        if len(token) <= 2:
            break
        if token[index] == "unsigned":
            del token[index]
            break
    #Combine * with field name
    #if '*' in token:
    if len(token) > 2 and token[-2] == '*':
        index = token.index('*')
        token[index+1] = '*' + token[index+1]
        del token[index]

    #for index in range(len(token)):
    #    if token[index] == '*':
    #        token[index+1] = '*' + token[index+1]
    #        del token[index]

    if token[0].endswith('_t'):
        token[0] = 'int'
    if token[0] == 'u64':
        token[0] = 'long'
    if token[0] == 'u32':
        token[0] = 'int'
    if token[0] == 'u16':
        token[0] = 'short'
    if token[0] == 'u8' or token[0] == '__u8':
        token[0] = 'char'
    #To remove pointer type
    #if token[0] == "struct":
    #    del token[1]
    s = ''
    for item in token:
        s += item + ' '
    return s, token

def count_used_field(struct_name):
    obj_name = []
    cnt = 0
    accessed_field = []
    f = open(struct_name+'.accessed_field', 'w')
    for index in range(len(versions)):
        key = versions[index]
        current_obj = objects[key]
        for item in current_obj:
            if item[-1] not in obj_name:
                obj_name.append(item[-1])
    for item in obj_name:
        for item2 in all_accessed_field:
            if item2 not in accessed_field:
                if item == item2 or item == '*'+item2:
                    cnt += 1
                    f.write("accessed field {0}\n".format(item))
                    accessed_field.append(item2)

    f.write("Total # of accessed field {0}\n".format(len(accessed_field)))
    f.close()

def reverse_diff(struct_name):
    f = open(struct_name+'.diff', 'w')
    total_unchanged_cnt = 0
    total_field_cnt = 0
    total_swap = 0
    total_swap_distance = 0
    total_add_cnt = 0
    total_change_cnt = 0
    total_delete_cnt = 0
    total_obj_size = 0
    changed_required_field = []
    for index in range(len(versions)-1):
        key = versions[index]
        next_key = versions[index+1]
        current_object = objects[key]
        next_object = objects[next_key]
        new_cnt = 0
        change_cnt = 0
        delete_cnt = 0
        swap_cnt = 0
        if len(current_object) == 0:
            f.write("{} is not supported in current version {}\n\n".format(struct_name, key))
            continue
        print "===========Start comparison: \t" + key + next_key + "================="
        #print "Number of field: ", len(current_object), len(next_object), len(next_object) - len(current_object)
        f.write("===========Start comparison: \t {0} {1} =================\n".format(key, next_key))
        f.write("Number of field: {0}, {1}, {2}\n".format(len(current_object), len(next_object), len(next_object) - len(current_object)))
        total_obj_size += len(current_object)
        #Check new fields:
        for item in next_object:
            flg = 0
            for tmp in current_object:
                if item[-1] == tmp[-1]:
                    flg = 1
            if flg == 0:
                #print "New field:", item
                f.write("New field: {0}\n".format(item))
                if item[-1] in all_accessed_field:
                    f.write("[---]: New field {0} in accessed fields\n".format(item[-1]))
                    if item[-1] not in changed_required_field:
                        changed_required_field.append(item[-1])
                new_cnt += 1
            #if item not in current_object:
            #    print "New field:", item
        #Check deleted or changed fields:
        for item in current_object:
            for tmp in next_object:
                if item[-1] == tmp[-1] and not item == tmp:
                    #print "Changed field:", item, tmp
                    f.write("Changed field: {0} {1}\n".format(item, tmp))
                    if item[-1] in all_accessed_field:
                        f.write("[---]: Changed field {0} in accessed fields\n".format(item[-1]))
                        if item[-1] not in changed_required_field:
                            changed_required_field.append(item[-1])
                    change_cnt += 1
        for item in current_object:
            flg = 0
            for tmp in next_object:
                if item[-1] == tmp[-1]:
                    flg = 1
                    break
            if flg == 0:
                #print "Deleted field: ", item
                f.write("Deleted field: {0}\n".format(item))
                if item[-1] in all_accessed_field:
                    f.write("[---]: Deleted field {0} in accessed fields\n".format(item[-1]))
                    if item[-1] not in changed_required_field:
                        changed_required_field.append(item[-1])
                delete_cnt += 1

        #Check order swap:
        '''
            To check order swap, remove all new fields and compare the sorted lists
        '''
        current_object_name = []
        next_object_name = []
        for item in current_object:
            current_object_name.append(item[-1])
        for item in next_object:
            next_object_name.append(item[-1])
        cnt = 0
        for item in current_object_name:
            if item in all_accessed_field:
                print(item)
                cnt += 1
        print("Number of used field", cnt, struct_name)

        obj_diff = [i for i in current_object_name+next_object_name if i not in current_object_name or i not in next_object_name]
        for item in obj_diff:
            if item in current_object_name:
                current_object_name.remove(item)
            if item in next_object_name:
                next_object_name.remove(item)

        while not current_object_name == next_object_name:
            for index in range(len(current_object_name)):
                if current_object_name[index] == next_object_name[index]:
                    continue
                if index<len(next_object_name)-1 and current_object_name[index] == next_object_name[index+1]:
                    swap_index = current_object_name.index(next_object_name[index])
                    swap_item = current_object_name[swap_index]
                    del current_object_name[swap_index]
                    current_object_name.insert(index, swap_item)
                    swap_cnt += 1
                    total_swap += 1
                    if swap_item in all_accessed_field:
                        f.write("[---]: Swapped field {0} in accessed fields\n".format(swap_item))
                        if item[-1] not in changed_required_field:
                            changed_required_field.append(item[-1])
                    break
                else:
                    next_index = next_object_name.index(current_object_name[index])
                    next_item = next_object_name[next_index]
                    del next_object_name[next_index]
                    next_object_name.insert(index, next_item)
                    f.write("Swapped field {0}".format(current_object_name[index]))
                    print("swap", current_object_name[index], current_object_name[next_index])
                    swap_cnt += 1
                    total_swap += 1
                    total_swap_distance += abs(index-next_index)
                    if next_item in all_accessed_field:
                        f.write("[---]: Swapped field {0} in accessed fields\n".format(next_item))
                        if item[-1] not in changed_required_field:
                            changed_required_field.append(item[-1])
                    break

        #Check pointer type change:
        '''
            If the field names are the same, compare their types
        '''
        #Check name changes:
        '''

        '''
        print("===========End comparison: \t" + key + next_key + "=================")
        f.write("newly added field: {0}, deleted field: {1}, changed field: {2}, swapped: {3}\n".format(new_cnt, delete_cnt, change_cnt, swap_cnt))
        unchanged_cnt = len(current_object) - delete_cnt - swap_cnt - change_cnt - new_cnt
        total_unchanged_cnt += unchanged_cnt
        total_field_cnt += len(current_object)
        f.write("unchanged cnt: {0}, unchanged percentage: {1}\n".format(unchanged_cnt, 1.0*unchanged_cnt/len(current_object)))
        f.write("# of changed required field{0}\n".format(len(changed_required_field)))
        f.write("===========End comparison: \t {0} {1} =================\n\n".format(key, next_key))
        total_delete_cnt += delete_cnt
        total_change_cnt += change_cnt
        total_add_cnt += new_cnt
    #print len(versions)
    f.write("Total field addition: {0}, field detelion {1}, changed field {2}, average obj size {3}\n".format(total_add_cnt, total_delete_cnt, total_change_cnt, total_obj_size/len(versions)))
    f.write("Average field addition: {0}, field detelion {1}, changed field {2}\n".format(1.0*total_add_cnt/len(versions), 1.0*total_delete_cnt/len(versions), 1.0*total_change_cnt/len(versions)))
    f.write("Total unchanged percentage: {0}, total swap: {1}\n".format(1.0*total_unchanged_cnt/total_field_cnt, total_swap))
    if total_swap > 0:
        f.write("Total swap cnt: {0}, total swap distance: {1}, average swap distance: {2}\n".format(total_swap, total_swap_distance, 1.0*total_swap_distance/total_swap))
    f.close()

    '''
    os.system("cp v4.11 result.h")
    for v in versions:
        file_name = v
        cmd = "grep -F -x -f result.h " + file_name
        print "diffing " + file_name
        result = commands.getstatusoutput(cmd)
        with open("result.h", "w") as output:
            output.write(result[1])
        #with open("temp" + v, 'w') as output:
        #    output.write(result[1])
    '''

def check_swap(current_object, next_object):
    for current_index in range(len(current_object)):
        next_index = next_object.index(current_object[current_index])
        if current_index == 0:
            if current_object[current_index+1] == next_object[next_index+1]:
                continue
            else:
                swapped_field = current_object[current_index]
                del current_object[current_index]
                del next_object[next_index]
                return True, abs(next_index - current_index), current_object, next_object, swapped_field
        elif current_index == len(current_object)-1:
            if current_object[current_index-1] == next_object[next_index-1]:
                continue
            else:
                swapped_field = current_object[current_index]
                del current_object[current_index]
                del next_object[next_index]
                return True, abs(next_index - current_index), current_object, next_object, swapped_field
        else:
            if current_object[current_index-1]==next_object[next_index-1] and current_object[current_index+1]==next_object[next_index+1]:
                continue
            else:
                swapped_field = current_object[current_index]
                del current_object[current_index]
                del next_object[next_index]
                return True, abs(next_index - current_index), current_object, next_object, swapped_field
    return False, None, None, None, None

def start_process(struct_name):
    cwd = os.getcwd()
    if not os.path.isdir("./"+struct_name):
        os.system("mkdir " + struct_name)
    os.chdir("./" + struct_name)
    download(struct_name)
    process_file(struct_name)
    reverse_diff(struct_name)
    count_used_field(struct_name)

    #find_config(struct_name)
    os.chdir(cwd)
    #for item in all_field_in_config:
    #    print item
    #for item in all_accessed_field:
    #    if item in all_field_in_config:
    #        print "found", item, 'in config'
def start_process_configs(struct_name, version):
    cwd = os.getcwd()
    if not os.path.isdir("./"+struct_name):
        os.system("mkdir " + struct_name)
    os.chdir("./" + struct_name)

    #if not os.path.exists(version+'_config'):
    configs = process_configuration(struct_name, version)
    content = []
    with open("/home/zhenxiao/linux_source/defconfig", 'r') as f:
        content = f.read().split('\n')
        for item in configs:
            try:
                index = content.index(item+'=y')
                print(content[index])
            except ValueError:
                continue
            if index < 0:
                continue
            rand_num = random.randint(0, 10)
            if rand_num > 5:
                # print "skip replacement"
                continue
            tmp = '#' + content[index]
            content[index] = tmp
            # print "replace with ", content[index]
    with open("/home/zhenxiao/linux_source/defconfig", 'w') as f:
        for item in content:
            f.write(item+'\n')

    os.chdir(cwd)

def main():
    for key in key_start.keys():
        #print "processing ", key
        start_process_configs(key, "v4.6")
    #start_process_configs("task_struct", "v4.6")
    #    start_process(key)
    #start_process("cred")

if __name__ == '__main__':
    main()
