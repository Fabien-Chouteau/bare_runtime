import shutil
import subprocess
import os
import sys

def replace_in_file(filename, target, replacement):
    # Read in the file
    filedata = None
    with open(filename, 'r') as file:
        filedata = file.read()

    # Replace the target string
    newdata = filedata.replace(target, replacement)

    # Write the file out again
    with open(filename, 'w') as file:
        file.write(newdata)


configurations = \
{
    'gnat_arm_elf':
    {'target': 'arm-elf',
     'switches': [
         '-mlittle-endian -mthumb -mfloat-abi=soft -mcpu=cortex-m0plus -fno-auto-inc-dec -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=soft -mcpu=cortex-m0 -fno-auto-inc-dec -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=soft -mcpu=cortex-m1 -fno-auto-inc-dec -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=soft -mcpu=cortex-m3 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=soft -mcpu=cortex-m4 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=hard -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=hard -mcpu=cortex-m7 -mfpu=fpv5-d16 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=hard -mcpu=cortex-m7 -mfpu=fpv5-sp-d16 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=soft -mcpu=cortex-m23 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=hard -mcpu=cortex-m33 -mfpu=fpv5-d16 -fno-tree-loop-distribute-patterns',
         '-mlittle-endian -mthumb -mfloat-abi=hard -mcpu=cortex-m33 -mfpu=fpv5-sp-d16 -fno-tree-loop-distribute-patterns',
     ]
     },

    'gnat_riscv64_elf':
    {'target': 'riscv64-elf',
     'switches': [
         '-march=rv32i -mabi=ilp32 -fno-tree-loop-distribute-patterns',
         '-march=rv32iac -mabi=ilp32 -fno-tree-loop-distribute-patterns',
         '-march=rv32im -mabi=ilp32 -fno-tree-loop-distribute-patterns',
         '-march=rv32imac -mabi=ilp32 -fno-tree-loop-distribute-patterns',
         '-march=rv32imafc -mabi=ilp32f -fno-tree-loop-distribute-patterns',
         '-march=rv32imafdc -mabi=ilp32d -fno-tree-loop-distribute-patterns',
         '-march=rv64im -mabi=lp64 -fno-tree-loop-distribute-patterns',
         '-march=rv64imac -mabi=lp64 -fno-tree-loop-distribute-patterns',
         '-march=rv64imafc -mabi=lp64f -fno-tree-loop-distribute-patterns',
         '-march=rv64imafdc -mabi=lp64d -fno-tree-loop-distribute-patterns',
         '-march=rv64imc -mabi=lp64 -fno-tree-loop-distribute-patterns',
         '-march=rv64imfc -mabi=lp64f -fno-tree-loop-distribute-patterns',
     ]
     },

    'gnat_xtensa_esp32_elf':
    {'target': 'xtensa-esp32-elf',
     'switches': [
         '-mlongcalls',
     ]
     },

}

fail_count = 0
success_count = 0

for (gnat, conf) in configurations.items():

    target = conf['target']
    for switches in conf['switches']:
        conf_str = f"{gnat} {target} {switches}"
        print("----------------------------")
        print(f"Starting: {conf_str}")
        copy_dir = os.path.join('tmp/', f"{gnat}-{str(hash(conf_str))}")
        shutil.copytree("basic_project", copy_dir)

        replace_in_file(os.path.join(copy_dir, 'alire.toml'), 'INSERT_GNAT', gnat)
        replace_in_file(os.path.join(copy_dir, 'alire.toml'), 'INSERT_BARE_RUNTIME_SWITCHES', switches)
        replace_in_file(os.path.join(copy_dir, 'sanity_check.gpr'), 'INSERT_GNAT_TARGET', target)

        wd = os.getcwd()
        os.chdir(copy_dir)
        proc = subprocess.Popen(["alr", "-n", "build", "--", "-f"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc.wait()
        os.chdir(wd)

        output = proc.stdout.read().decode()
        if "Build finished successfully" not in output:
            print("======== BUILD FAILED ========")
            print(f"Conf: {conf_str}")
            print(output)
            fail_count += 1
        else:
            print(f"SUCCESS")
            success_count += 1

print("----------------------------")
print(f"PASS: {success_count}")
print(f"FAIL: {fail_count}")

if fail_count > 0:
    sys.exit(1)
