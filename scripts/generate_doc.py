import os
import subprocess

with open('README.rst', 'w') as readme:
    for module in os.listdir(os.path.dirname(__file__)):
        if module == os.path.basename(__file__) or module == '__init__.py' or module[-3:] != '.py':
            continue
        readme.write('\n')
        readme.writelines('\n'.join(['='*len(module),module,'='*len(module)]))
        process=subprocess.Popen([module,'-h'],shell=True,stdout=subprocess.PIPE)
        readme.write('\n')
        for line in process.stdout:
            readme.write(line)

