import subprocess


def build_binary():
    build_log_file = '/binary/build.log'

    command = [
        'pyinstaller',
        '--name=executable_module',
        '--onefile',
        '--distpath=/binary',
        './app/services/sec_dev_scanner/template.py'
    ]

    with open(build_log_file, 'w') as f:
        try:
            result = subprocess.run(
                command, stdout=f, stderr=subprocess.STDOUT, text=True, check=True)
            print(f"Build success, details in {build_log_file}")

        except subprocess.CalledProcessError as e:
            print(f"Build fail, details in {build_log_file}")
