#Copyright Bail 2021-2022
#bssenglish:install_requires 依赖安装
#2021.10.16-2022.7.20

PIP_REQUIRE = ['requests','playsound']
##LINUX_REQUIRE = ['python3-gst-1.0']

import sys,os

def isinst():
    if sys.argv[-1] == '-p':
        return True
    else:
        return False
"""def linux_install():
    res = os.system('sudo apt install '+' '.join(LINUX_REQUIRE))
    if res != 0:
        res = os.system('sudo yum install '+' '.join(LINUX_REQUIRE))
        if res != 0:
            raise OSError('Linux依赖安装失败')"""
def pip_install():
    os.system(f'{sys.executable} -m pip install '+' '.join(PIP_REQUIRE))
def main():
##    if os.name == 'posix' and not isinst():
##        linux_install()
    pip_install()
    return 0

if __name__ == '__main__':
    sys.exit(main())

