import subprocess

print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)

'''
如果子进程还需要输入，则可以通过communicate()方法输入：...
上面的代码相当于在命令行执行命令nslookup，然后手动输入：

set q=mx
python.org
exit
运行结果如下：

$ nslookup
Server:        192.168.19.4
Address:    192.168.19.4#53

Non-authoritative answer:
python.org    mail exchanger = 50 mail.python.org.

Authoritative answers can be found from:
mail.python.org    internet address = 82.94.164.166
mail.python.org    has AAAA address 2001:888:2000:d::a6


Exit code: 0
'''