# FxWordlist main file
# Version : 1.0

if __name__ == "__main__":

    try:
        from modules_import import check_installation
        check_installation('tqdm')
        check_installation('colorama')
        from all_functions import (read_information_from_file, generate_permutation, generate_maj,
        generate_lower, start_symbol_digit, add_char, save_passwords_to_file, start_all_upper,
        start_merge, start_ext_merge,add_double_letter)
        from error_processing import verif_path, verif_nb_permutation, keyboard_interruption, check_ext_merge
        from fmode import mode_config

        import argparse
        from colorama import Fore, Style, init
        from time import time

    except KeyboardInterrupt:
        keyboard_interruption(color=False)
    except Exception as e:
        print(f'[!] Error: {e}.')
        exit(1)

    try:

        init(autoreset=True)

        # VALEURS PAR DEFAUT (celles du mode OPTIMIZED)
        combination_length = 2 # Spécifier la longueur de la combinaison d'informations pour le mot de passe (en permutation)
        nb_symbol = 2 # Spécifie le nombre de remplacements maximal de lettre par un symbole sur chaque mot de passe, a=@
        nb_digit = 2 # Spécifie le nombre de remplacements maximal de lettre par un chiffre sur chaque mot de passe, a=4
        first_upper=True # True = On fait une capitalisation des mots de passe
        nb_all_maj=None # Spécifie le nombre de remplacements maximal de lettre par sa majuscule par mot de passe
        lowercase=True # True = Lower() sur les mots de passe
        only_mode_activated=True # Est-ce qu'un mode a été activé (y compris le mode par défaut)
        character="1"
        add_wordlist = None
        merge = None
        double_letter=True
        mode = "optimized"

        class MyHelpFormatter(argparse.HelpFormatter):
            def _format_action(self, action):
                if not action.option_strings:
                    # Positional argument
                    arg_string = action.dest  # Utilisez le nom de l'argument comme texte
                    formatted_help = self._expand_help(action)
                    help_text = f"{Fore.RESET}{formatted_help}\n"
                    return f"{Fore.LIGHTGREEN_EX}{arg_string.ljust(25)}{help_text}"
                else:
                    # Optional argument
                    arg_string = ', '.join(action.option_strings)
                    formatted_help = self._expand_help(action)
                    help_text = f"{Fore.RESET}{formatted_help}\n"
                    return f"{Fore.LIGHTGREEN_EX}{arg_string.ljust(25)}{help_text}\n"


        class MyArgumentParser(argparse.ArgumentParser):
            def error(self, message):
                print(f"{Fore.RED}[!] Error: {message}{Style.RESET_ALL}")
                exit(1)


        def verif_bool(value):
            if value.lower() in ['yes','y', '1']:
                return True
            elif value.lower() in ['no','n', '0']:
                return False
            else:
                raise argparse.ArgumentTypeError("The value must be Yes or No = 1 or 0 (capital letters are not required).")

        # Utilisez MyArgumentParser au lieu de argparse.ArgumentParser
        parser = MyArgumentParser(formatter_class=MyHelpFormatter, description=Fore.LIGHTYELLOW_EX + "Description : Powerful tool for generating a personal password list." + Style.RESET_ALL,
                                epilog=Fore.LIGHTYELLOW_EX + "Reading the documentation is highly recommended to use the program to its full potential.")

        # Spécifier le chemin du fichier contenant les informations
        parser.add_argument("information_file", nargs="?", type=str, help="Path to the file containing target information.")

        # Mode intéractif avec les questions à la place du fichier d'informations
        parser.add_argument("-i", "--interactive", action="store_true", help="The program asks you questions instead of the informations file.")

        # Affiche les détails de la configuration
        parser.add_argument("-v", "--verbosity", action="store_true", help="Displays all the details of your configuration.")

        # Choisir le mode de génération de mot de passe
        parser.add_argument("-m", "--mode", choices=["soft", "optimized", "advanced", "deep"], help="Choose the generation mode.")

        # Nombre de combinaisons pour les permutations d'informations
        parser.add_argument("-p", "--permutation", type=int, help="Number of combinations for information permutations.")

        # Nombre de remplacements par des symboles (test de toutes les combinaisons)
        parser.add_argument("-s", "--symbol", type=int, help="Number of replacements with symbols, ex: a = @ (testing all combinations).")

        # Nombre de remplacements par des chiffres (test de toutes les combinaisons)
        parser.add_argument("-d", "--digit", type=int, help="Number of replacements with digits, ex: a = 4 (testing all combinations).")

        # Nombre correspondant au niveau d'ajout de caractère, niv1,niv2,niv3,niv4 = low,mid,max,all
        parser.add_argument("-c", "--character", choices=["1","2","3","0"],
                            help="Level of adding additional character like '1','*' ... | Type 0 to disable the feature.\n"+" "*26+"Each level increases the number possibility, by default lvl 1 for all mode (max=3).")

        # Activer la fonction pour mettre en majuscule uniquement la première lettre
        parser.add_argument("-f", "--firstupper", type=verif_bool, help="Enable/Disable (Y/N) the function to uppercase the first letter only.")

        # Activer la fonction pour mettre en minuscule l'ensemble du mot de passe
        parser.add_argument("-l", "--lowercase", type=verif_bool, help="Enable/Disable (Y/N) the function to lowercase the entire password.")

        # Activer la fonction pour doubler les voyelles en fin de mots
        parser.add_argument("-b", "--double_letter", type=verif_bool,help="Enable/Disable (Y/N) the function to double the last letter if it is a vowel, ex: Mia = Miaa.")

        # Nombre de remplacements par des lettres majuscules (test de toutes les combinaisons)
        parser.add_argument("-a", "--allupper", type=int, help="Number of replacements with uppercase letters (testing all combinations).")

        # Ajouter une wordlist externe à notre wordlist générée via les infos
        parser.add_argument("-w", "--wordlist", type=str,
                            help="Add one or more additional wordlists that we will add to our generation\n"+" "*26+"(put a ',' to separate if there are several).")
        
        # Fichier de sortie
        parser.add_argument("-o", "--output_file", type=str, default='fw_output.txt',
                            help = "The path for the output file wordlist,\n"+" "*26+"by default the output file will be located in the directory where you started the program." )

        # Fusionner la wordlist générée via les infos avec une wordlist externe
        parser.add_argument("--merge", type=str,
                            help="Merge one or more extra word lists with our generated content from target information,\n"+" "*26+"creating multiple combinations between the two (put a ',' to separate if there are several).")

        # Fusionner deux wordlist externe, donc aucun rapport avec les infos
        parser.add_argument("--ext_merge", type=str,
                            help="Merge various external wordlists while excluding the use of target information,\n"+" "*26+"duplicates are automatically removed (put a ',' to separate).")

        # Définir toutes les options à la même valeur choisie
        parser.add_argument("--all_option", type=int, help="Set all values to the same chosen value and enable all functions (except -w, --merge).")

        # Affiche la version du programme
        parser.add_argument("--version", action="version",version="FxWordlist Version 1.0", help="Print the version and exit.")

        args = parser.parse_args()

        # Si ext_merge alors aucun autre parametre
        check_ext_merge(args)

        print(Fore.LIGHTWHITE_EX + '================================================')
        print(Fore.LIGHTWHITE_EX + "Project : " + Fore.LIGHTRED_EX + "FxWordlist.py")
        print(Fore.LIGHTWHITE_EX + "Author : " + Fore.LIGHTRED_EX + "Flegh")
        print(Fore.LIGHTWHITE_EX + "Github : " + Fore.LIGHTRED_EX + "https://github.com/flegh113/FxWordlist")
        print(Fore.LIGHTWHITE_EX + '================================================\n')

        # Vérification du fichier d'informations
        if args.information_file:
            if args.interactive:
                print(Fore.RED + "[!] Logical Error: You cannot specify both information_file and interactive mode (-i).")
                exit(1)
            # Vérifier si le fichier d'informations existe
            verif_path(args.information_file)
            # Lire les informations à partir du fichier
            passwords = read_information_from_file(args.information_file)
        elif args.interactive:
            # Demander à l'utilisateur d'entrer les informations manuellement
            print(Fore.LIGHTYELLOW_EX + "[+] Information file not provided. Please enter the target information manually.")
            print(Fore.LIGHTYELLOW_EX + "[+] Leave blank to specify nothing.")
            passwords=set()
            information_labels = ["firstname", "lastname", "nickname/pseudonym", "birthdate (YEAR)",
                                  "birthdate (MONTH)","birthdate (DAY)", "city of residence"]  # Ajoutez d'autres informations au besoin
            # Boucle pour demander chaque information à l'utilisateur
            for label in information_labels:
                information = input(f"{Fore.LIGHTGREEN_EX}[?] Enter the target's {label}: {Style.RESET_ALL}").capitalize()
                information = information.replace(" ","")
                if information != "":
                    passwords.add(information)
            while True:
                information = input(f"{Fore.LIGHTGREEN_EX}[?] Any other information (leave blank for none): {Style.RESET_ALL}").capitalize()
                information = information.replace(" ","")
                if information != "":
                    passwords.add(information)
                else:
                    break
            print("")

        elif args.ext_merge:
            passwords = start_ext_merge(args.ext_merge)
            # print(Fore.LIGHTGREEN_EX + "** The merge was generated successfully **")

        else:
            print(Fore.RED + "[!] Error: the following arguments are required: information_file or interactive mode (-i), for help type -h, --help.")
            exit(1)

        # Vérifier si les variable d'informations contiennent au moins une information
        if len(passwords) == 0:
            print(Fore.RED + "[!] Error: You must have at least one piece of information.")
            exit(1)

        # Verif, Une commande ne doit pas contenir un parametre --mode et en même temps des autres parametres (pas logique)
        # check_mode_and_options(args)

        if args.all_option == 0:
            print(Fore.RED + "[!] Error: the all_option function must take a value greater than 0 as an argument.")
            exit(1)
        if args.all_option:
            print(Fore.LIGHTBLUE_EX + f"[+] ALL OPTION SET ON : {args.all_option}.")
            combination_length = args.all_option
            nb_symbol = args.all_option
            nb_digit = args.all_option
            nb_all_maj = args.all_option
            lowercase = True
            first_upper = True
            double_letter = True
            only_mode_activated=False
            if args.all_option>3:
                character = 3
            else:
                character = args.all_option

        else:
            # Vérification mode ou pas de mode
            if args.mode: # != None
                mode = args.mode
                # Appeler la fonction mode_config pour mettre à jour les variables
                combination_length, nb_symbol, nb_digit, first_upper, nb_all_maj, lowercase,character, double_letter=(
                mode_config(passwords,args.mode,combination_length,nb_symbol,
                nb_digit,first_upper,nb_all_maj,lowercase,character,double_letter))             

            elif all(arg == 0 or arg is None or arg == False for key, arg in vars(args).items() if key not in ['information_file','interactive','output_file',"verbosity"]):
                print(Fore.LIGHTBLUE_EX + "[+] Default Mode : OPTIMIZED.")

            else:
                print(Fore.LIGHTBLUE_EX + "[+] Mode : No Mode Selected")
                combination_length = args.permutation
                nb_symbol = args.symbol
                nb_digit = args.digit
                first_upper = args.firstupper
                nb_all_maj = args.allupper
                lowercase = args.lowercase
                character = args.character
                add_wordlist = args.wordlist
                merge = args.merge
                double_letter=args.double_letter
                only_mode_activated=False
                
        # Verif, même s'il y'a un mode ou all_option, on peut modifier une/plusieurs valeurs tout en gardant toutes les autres règles du mode
        if args.permutation:
            combination_length=args.permutation
            only_mode_activated=False
        if args.symbol is not None: # is not None permet aussi le =0 qui annule donc une fonctionnalité d'un mode
            nb_symbol=args.symbol
        if args.digit is not None:
            nb_digit=args.digit
        if args.firstupper is not None:
            first_upper=args.firstupper
        if args.allupper is not None:
            nb_all_maj=args.allupper
        if args.lowercase is not None:
            lowercase=args.lowercase
        if args.character:
            character=args.character
        if args.wordlist:
            add_wordlist=args.wordlist
        if args.merge:
            merge=args.merge
        if args.double_letter is not None:
            double_letter=args.double_letter
        # peut etre afficher si y'en a au moins 1 en not None :  Mode : [MODE] with options
        
        # Pour éviter le 0
        if args.permutation == 0:
            combination_length = 1

    except KeyboardInterrupt:
        keyboard_interruption(color=True)
    try:

        if args.verbosity:
            print(
f"""{Fore.LIGHTBLUE_EX}Permutations  : {Style.RESET_ALL}{combination_length}
{Fore.LIGHTBLUE_EX}Symbols       : {Style.RESET_ALL}{nb_symbol}
{Fore.LIGHTBLUE_EX}Digits        : {Style.RESET_ALL}{nb_digit}
{Fore.LIGHTBLUE_EX}All Upper     : {Style.RESET_ALL}{nb_all_maj}
{Fore.LIGHTBLUE_EX}Lvl character : {Style.RESET_ALL}{character}
{Fore.LIGHTBLUE_EX}Double letter : {Style.RESET_ALL}{double_letter}
{Fore.LIGHTBLUE_EX}First Upper   : {Style.RESET_ALL}{first_upper}
{Fore.LIGHTBLUE_EX}Lowercase     : {Style.RESET_ALL}{lowercase}
""")

        # Enregistrement du temps de début
        start_time = time()

        if combination_length is not None:
            # Pour éviter de lancer la def generate_permutation en boucle pour rien
            combination_length = verif_nb_permutation(combination_length, passwords, only_mode_activated)
            # Générer les mots de passe avec les permutations
            passwords= generate_permutation(passwords, combination_length)
            

        # Doubler la derniere lettre si c'est une voyelle, Mia=Miaa
        if double_letter is True:
            passwords = add_double_letter(passwords)

        # Modifier les mots de passe en mettant tout le mot de passe en minuscule
        func_low=False
        if lowercase is True:
            func_low=True
            passwords = passwords.union(generate_lower(passwords))


        # Fonction pour générer toutes les combinaisons de lettre majuscule
        if nb_all_maj is not None and nb_all_maj != 0:
            passwords = start_all_upper(passwords,nb_all_maj,func_low)


        if mode == "soft" or mode == "optimized":
            # En mode soft ou optimized on ne combine pas les remplacements par digit et symbol pour la génération
            # Modifier les mots de passe en remplaçant des lettres par leur équivalents symboliques a=@
            password_initial = passwords
            if nb_symbol is not None and nb_symbol != 0:
                password_generated = start_symbol_digit(password_initial, {"a":"@","e":"€","s":"$"} ,nb_symbol, "[>] Generation with symbols")
                passwords = passwords.union(password_generated)
            
            # Modifier les mots de passe en remplaçant des lettres par leur équivalents symboliques en chiffre a=4
            if nb_digit is not None and nb_digit != 0:
                password_generated = start_symbol_digit(password_initial, {"a":"4","e":"3","i":"1","o":"0"}, nb_digit, "[>] Generation with digits")
                passwords = passwords.union(password_generated)
        else:
            # Modifier les mots de passe en remplaçant des lettres par leur équivalents symboliques a=@
            if nb_symbol is not None and nb_symbol != 0:
                passwords = start_symbol_digit(passwords, {"a":"@","e":"€","s":"$"} ,nb_symbol, "[>] Generation with symbols")

            # Modifier les mots de passe en remplaçant des lettres par leur équivalents symboliques en chiffre a=4
            if nb_digit is not None and nb_digit != 0:
                passwords = start_symbol_digit(passwords, {"a":"4","e":"3","i":"1","o":"0"}, nb_digit, "[>] Generation with digits")


        if first_upper is True and (nb_all_maj is None or nb_all_maj == 0):
            # Modifier les mots de passe en mettant uniquement la première lettre en majuscule
            passwords = passwords.union(generate_maj(passwords))


        ############# A SAVOIR OU LE PLACER VERITABLEMENT
        # A CONTINUER CHAR SUPPLEMENTAIRE
        if character is not None and character != "0":
            passwords = passwords.union(add_char(passwords,character))

        # #Ajouts dans les passwords des ajouts de caractères
        # if character is not None and character != "0":
        #     passwords = passwords.union(passwords_end)


        if merge is not None:
            passwords = start_merge(passwords, merge)


        if add_wordlist is not None:
            wl_files = add_wordlist.split(",")
            for file in wl_files:
                convert_file = read_information_from_file(file)
                passwords = passwords.union(convert_file)
            

        nb_passwd=len(passwords)
        print(Fore.LIGHTGREEN_EX + f"[>] Wordlist currently being written...\n")
     
        # Enregistrer les mots de passe modifiés dans un fichier
        save_passwords_to_file(passwords, args.output_file) # le fichier de sortie (wordlist)
        # Affichage
        print(Fore.LIGHTGREEN_EX + "** Wordlist generated successfully **")
        print(Fore.LIGHTYELLOW_EX + f'--> It contains {nb_passwd} passwords.')

        print(Fore.LIGHTYELLOW_EX + "--> Output file :",args.output_file)

        # Enregistrement du temps de fin
        end_time = time()
        # Affichez la durée totale
        print(Fore.LIGHTBLUE_EX + f"\n[+] The program took {round(end_time-start_time,5)} seconds to run.")


    except KeyboardInterrupt:
        keyboard_interruption(color=True)
    except Exception as e:
        print(e)
        
#9