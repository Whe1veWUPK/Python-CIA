from subprocess import run

def run_cmd(cmd_str = '', echo_print = 1):
    if echo_print == 1:
        print('command run..'.format(cmd_str))
    run(cmd_str, shell=True)
