try:
    from os import path
    from colorama import Fore, init
    init(autoreset=True)
except:
    print(f"\n[!] Error: Import of modules failed")
    exit(1)


def keyboard_interruption(color):
    if color==True:
        print(Fore.RED + "\n[!] Keyboard Interruption, exiting.")
    else:
        print("\n[!] Keyboard Interruption, exiting.")
    exit(1)


def check_ext_merge(args):
    if args.ext_merge:
        for n,v in vars(args).items():
            if n not in ["ext_merge","output_file"]:
                if v is not None and v is not False:
                    print(Fore.RED + "[!] Error: If --ext_merge is specified, no other parameters (-m, informations_file...) should be added.")
                    exit(1)


def verif_path(file):        
    if not path.isfile(file):
        print(Fore.RED + f"[!] Error: File '{file}' does not exist.")
        exit(1) # Arrêt du programme s'il n'existe pas


def verif_nb_permutation(permutation, passwords, only_mode_activated):
    if permutation > len(passwords):
        nb_info = len(passwords)
        if only_mode_activated is False:
            print(Fore.LIGHTMAGENTA_EX + "[!] Logical Error : The number of permutations is greater than the number of information(s).")
            print(Fore.LIGHTMAGENTA_EX + f"[!] --> The --permutation parameter has been set to the maximum: {nb_info}.")
        return nb_info
    else:
        return permutation
    

def verif_max_for_mode(passwords, mode):
    max_length = len(max(passwords, key=len))
    if max_length > 15:
        print(Fore.LIGHTMAGENTA_EX + "Length of your informations =",max_length)
        print(Fore.RED + f"\n[!] Error: {mode} mode is heavy, your information(s) is too long for this mode (max_length:15).")
        print(Fore.RED + "[+] If you really want to continue with this informations you can use your own configuration (--help).")
        exit(1)

    total_length = sum(len(password) for password in passwords)
    if total_length > 40 and mode == "advanced":
        print(Fore.CYAN + "[+] Global length of informations =",total_length)
        print(Fore.RED + f"[!] Error: Advanced mode is heavy, your information(s) is too long for this mode (global_max_length:40).")
        print(Fore.CYAN + "[+] If you really want to continue with this informations you can use your own configuration (--help).")
        exit(1)
    if total_length > 30 and mode == "deep":
        print(Fore.CYAN + "[+] Global length of informations =",total_length)
        print(Fore.RED + f"\n[!] Error: Deep mode is heavy, your information(s) is too long for this mode (global_max_length:30)")
        print(Fore.CYAN + "[+] --> If you really want to continue with this informations you can use your own configuration (-h,--help).")
        exit(1)
