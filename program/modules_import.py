try:
    from subprocess import run
    from importlib import import_module
except:
    print(f"\n[!] Error: Import of modules failed")
    exit(1)

def check_installation(module_name):
    try:
        import_module(module_name)
    except ImportError:
        print(f"{module_name} is not installed. Installing...")
        try:
            run(["pip", "install", module_name], check=True)
            print(f"\n[?] The {module_name} module was successfully installed.\n")
        except:
            print(f"\n[!] Error: Installation of the '{module_name}' module failed.")
            exit(1)
9