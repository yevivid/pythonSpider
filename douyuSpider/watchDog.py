import psutil


def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            print(pid)
            break
    else:
        print("not found")


if judgeprocess('main.py') == 0:
    print('success')
else:
    pass