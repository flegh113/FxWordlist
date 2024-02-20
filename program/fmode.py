from colorama import Fore
from error_processing import verif_max_for_mode

def mode_config(passwords,mode,combination_length, nb_symbol, nb_digit, first_upper, nb_all_maj,lowercase,character, double_letter):
    print(Fore.LIGHTYELLOW_EX + f"[+] Mode : {mode.upper()}.") 
    if mode=="soft":
        combination_length = 2
        nb_symbol = 1
        nb_digit = 1
        first_upper=True
        nb_all_maj=None
        lowercase=True
        character="1"
        double_letter=True

    elif mode=="advanced":
        verif_max_for_mode(passwords, "advanced")
        #print(Fore.LIGHTMAGENTA_EX + "[?] Be careful with this mode, it drastically increases the size of the wordlist and the generation time.")
        combination_length = 2
        nb_symbol = 4
        nb_digit = 4
        first_upper= False # False car nb_all_maj =! None ou 0, c'est logique
        nb_all_maj= 3
        lowercase=True
        character="1"
        double_letter=True

    elif mode=="deep":
        verif_max_for_mode(passwords, "deep")
        #print(Fore.LIGHTMAGENTA_EX + "[?] Be careful with this mode, it drastically increases the size of the wordlist and the generation time.")
        combination_length = 3
        nb_symbol = 10
        nb_digit = 10
        first_upper= False # False car nb_all_maj =! None ou 0, c'est logique
        nb_all_maj= 10
        lowercase=True
        character="1"
        double_letter=True

    return combination_length, nb_symbol, nb_digit, first_upper, nb_all_maj, lowercase, character, double_letter

