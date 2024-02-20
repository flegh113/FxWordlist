try:
    from itertools import permutations
    from tqdm import tqdm
    from colorama import Fore, init
    init(autoreset=True)
except:
    print(f"\n[!] Error: Import of modules failed")
    exit(1)

def read_information_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Lire les informations depuis le fichier et les stocker dans une liste
            return {line.strip() for line in file}
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' n'existe pas.")
        exit(1)
    except Exception as e:
        print(e)


def generate_permutation(informations, combination_length):
    passwords_set = set()
    informations_list = list(informations)
    for r in tqdm(range(1, combination_length + 1), desc=Fore.LIGHTGREEN_EX + "[>] Generation with permutations", bar_format="{desc}: "+Fore.LIGHTWHITE_EX+"{percentage:.2f}%"):
        combinations = permutations(informations_list, r)
        passwords_set.update(map(''.join, combinations))
    return passwords_set

def generate_maj(passwords):
    passwords_maj_set = set()
    for passwd in passwords:
        passwd_capitalized = passwd.capitalize()
        if passwd_capitalized not in passwords:
            passwords_maj_set.add(passwd_capitalized)
    return passwords_maj_set

def generate_lower(passwords):
    passwords_low_set = set()
    for passwd in passwords:
        passwd_lower = passwd.lower()
        if passwd_lower not in passwords:
            passwords_low_set.add(passwd_lower)
    return passwords_low_set


############################################################################################################################################################

# Fonction pour générer toutes les combinaisons de lettre majuscule
def generate_all_maj(passwd, remaining_replacements, global_passwords):
    all_maj_set = set()
    queue = [(passwd, 0, remaining_replacements)]
    while queue:
        current_passwd, index, remaining_replacements = queue.pop()

        if current_passwd not in all_maj_set and current_passwd not in global_passwords:
            all_maj_set.add(current_passwd)

        if remaining_replacements > 0:
            for i in range(index, len(current_passwd)):
                char = current_passwd[i]
                if char.islower():
                    new_passwd = current_passwd[:i] + char.upper() + current_passwd[i + 1:]
                    queue.append((new_passwd, i + 1, remaining_replacements - 1))

    return all_maj_set

def start_all_upper(passwords,nb_all_maj,func_low):
    if nb_all_maj is not None and nb_all_maj != 0:
        if func_low is False:
            low_for_all_maj = passwords.union(generate_lower(passwords))
        else:
            low_for_all_maj = passwords
        # Modifier les mots de passe en remplaçant des lettres par la même en majuscule
        all_maj_sets = []
        for passwd in tqdm(low_for_all_maj, desc=Fore.LIGHTGREEN_EX + "[>] Generation with capital letters", bar_format="{desc}: "+Fore.LIGHTWHITE_EX+"{percentage:.2f}%"):
            all_maj_set = generate_all_maj(passwd, nb_all_maj, low_for_all_maj) # ex: nb_all_maj=2 : avec 2 remplacements de majuscule max
            all_maj_sets.append(all_maj_set)
        all_maj = set.union(*all_maj_sets)
        passwords = passwords.union(all_maj)
    return passwords

############################################################################################################################################################

# Fonction pour générer toutes les combinaisons de remplacements par symboles
def generate_symbol_digit(passwd, symbol_letter, remaining_replacements, global_passwords):
    passwd_symb = set()
    queue = [(passwd, 0, remaining_replacements)]
    while queue:
        current_passwd, index, remaining_replacements = queue.pop()

        if current_passwd not in passwd_symb and current_passwd not in global_passwords:
            passwd_symb.add(current_passwd)

        if remaining_replacements > 0:
            for i in range(index, len(current_passwd)):
                char = current_passwd[i]
                char = char.lower()
                if char in symbol_letter:
                    new_passwd = current_passwd[:i] + symbol_letter[char] + current_passwd[i + 1:]
                    queue.append((new_passwd, i + 1, remaining_replacements - 1))

    return passwd_symb

def start_symbol_digit(passwords,dictionary,nb,str_gen):
    # Modifier les mots de passe en remplaçant des lettres par leur équivalents symboliques
    symbols_list_sets=[]
    for passwd in tqdm(passwords, desc=Fore.LIGHTGREEN_EX + str_gen, bar_format="{desc}: "+Fore.LIGHTWHITE_EX+"{percentage:.2f}%"):
        symbols_list = generate_symbol_digit(passwd, dictionary, nb, passwords) # ex: nb for symbols=2 : avec 2 remplacements de symboles max
        symbols_list_sets.append(symbols_list)
    all_maj = set.union(*symbols_list_sets)
    passwords = passwords.union(all_maj)
    return passwords

############################################################################################################################################################


def add_char(passwords,lvl):
    char_sup = [["1", "123", "0", "."],
                ["1", "123", "0", ".", "!", "*"],
                ["1", "123", "0", ".", "!", "*", "00","2000"]]
    passwords_tmp=set()
    lvl=int(lvl)
    # Il faut ajouter plusieurs listes car ce n'est pas suffisant exemple celle-ci c'est uniquement pour le soft
    # Modifier les mots de passe en remplaçant des lettres par leur équivalents symboliques
    for passwd in tqdm(passwords, desc=Fore.LIGHTGREEN_EX + "[>] Generation with characters addition", bar_format="{desc}: "+Fore.LIGHTWHITE_EX+"{percentage:.2f}%"):
        passwd_save=passwd
        for char in char_sup[lvl-1]:
            passwd+=char
            passwords_tmp.add(passwd)
            passwd=passwd_save
    passwords = passwords.union(passwords_tmp)
    return passwords

############################################################################################################################################################

def generate_merge(passwords, to_merge):
    result = set()
    # Générer toutes les permutations entre le prénom et les éléments du set
    for passwd in tqdm(passwords, desc=Fore.LIGHTGREEN_EX + "[>] Merger in progress", bar_format="{desc}: "+Fore.LIGHTWHITE_EX+"{percentage:.2f}%"):
        for word in to_merge:
            # Ajouter les permutations au résultat
            result.add(passwd + word)
            result.add(word + passwd)
    return result

def start_merge(passwords, arg_merge):
    passwords_initial = passwords
    wl_files = arg_merge.split(",")
    # Fusionner les mots de passe avec la digit wordlist
    for file in wl_files:
        convert_file = read_information_from_file(file)
        passwords = passwords.union(generate_merge(passwords_initial, convert_file))
    print("")
    return passwords

def start_ext_merge(ext):
    wl_files = ext.split(",")
    passwords=set()
    convert_file=[]
    for file in wl_files:
        convert_file.append(read_information_from_file(file))
    for i,f in enumerate(convert_file):
        for n,f2 in enumerate(convert_file):
            if i!=n:
                passwords = passwords.union(generate_merge(f, f2))
    if len(passwords) == 0:
        print(Fore.RED + "[!] Error: With --ext_merge you must specify at least 2 non-empty wordlists (put a ',' to separate).")
        exit(1)
    print("")
    return passwords

############################################################################################################################################################


def add_double_letter(passwords):
    passwords_tmp = set()
    vowel = ["a","e","i","o","u","y"]
    for passwd in tqdm(passwords, desc=Fore.LIGHTGREEN_EX + "[>] Generation with double letter", bar_format="{desc}: "+Fore.LIGHTWHITE_EX+"{percentage:.2f}%"):
        if passwd[-1].lower() in vowel:
            passwords_tmp.add(passwd+passwd[-1])
    passwords = passwords.union(passwords_tmp)
    return passwords


############################################################################################################################################################


def save_passwords_to_file(passwords, filename):
    with open(filename, 'w') as file:
        for passwd in passwords:
            file.write(passwd + '\n')