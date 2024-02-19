##############################################################
#                                                            #
#  Hi, here is the documentation of the FxWordlist project.  #
#                                                            #
##############################################################

!! This tool will be infinitely more efficient if you really know how to use it. !!
!! You really have to adapt your configuration to the amount of information you have. !!

To use this program correctly, please do this :

You have two options :

1. Write down all the information you have about the target in a .txt file (firstname, lastname, date of birth, ...).

!! Don't forget that it's one information per line maximum !!

Here's an example:
In "informations.txt" file :
Alice
Bob
1990
[...]

OR

2. You can enter the -i command to have the program ask you the questions directly without passing the file containing the information.

python main.py -i [and option if u want, like -m soft]

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Now you can use the program.
Don't forget to specify your "[informations_file.txt]" file or the -i command when you type a command.
You can position them anywhere in your order :
1 : python main.py informations.txt -m soft
2 : python main.py -m soft informations.txt
Or
3 : python main.py -i -m soft
4 : python main.py -m soft -i

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This tool contains 4 modes for easy configuration:
-m, --mode {soft;optimized;advanced;deep} || Choose the generation mode.

- SOFT
command: python main.py informations.txt -m soft

1.Description :
>> Soft mode is used to generate small password lists. As a result, most of the program's functions will be toned down, allowing you to do less work.

2.Why use this mode ?
>> This mode doesn't involve any great complexity of passwords, which means it can be used as a basis for breaking a password that isn't very complex/robust.

---------------------------------------------------------------------------------------------------------

- OPTIMIZED (default mode)
command: python main.py informations.txt (no need to specify mode, it's already the default if there's no option)

1.Description :
>> Optimized mode is the default mode. It aims to generate password lists that optimize both quantity and quality. As a result, most of the program's features are probabilistically designed to retain only the most likely passwords. 

2.Why use this mode ?
>> This mode is widely preferred because it facilitates the creation of password lists that are not excessively voluminous, while focusing as much as possible on the probability of the passwords' existence.

---------------------------------------------------------------------------------------------------------

- ADVANCED
command: python main.py informations.txt -m advanced

1.Description :
>> This mode pushes generation further by implementing additional functions and increasing generation parameters, thus creating larger wordlists.

2.Why use this mode ?
>> If you really want to increase your chances of finding a password without worrying about its size, this may be the mode for you.

---------------------------------------------------------------------------------------------------------

- DEEP
command: python main.py informations.txt -m deep

1.Description :
>> This mode is very heavy, it will test a very large number of possibilities, which can easily make the wordlist absolutely enormous.

2.Why use this mode?
>> This mode should only be used if you have very little information about a person. That's why maximum rules have been included in its programming.
Beyond 3-4 pieces of information, it will generate so many passwords that it won't necessarily be useful (this also depends on the size of each piece of information).
However, if you don't have much information, it can be very useful for testing countless combinations.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CONFIGURATION
This tool is fully configurable, so you can create very specific word lists depending on what you want, using the various options available.
You can also specify a mode and modify one or more of its values ​​with commands, example: -m soft -p3 -a1 -s0 (0 disables) ...

If you input any of these commands without specifying a mode, all other options will be automatically disabled, ensuring the execution aligns precisely with your intent.
You can, of course, combine them as needed :
example with all commands --> main.py informations.txt -p2 -s3 -d2 -a3 -fY -lY -bY -c1 -w wordlist.txt --merge 0_2050.txt -o my_custom_wordlist.txt


-m, --mode {soft;optimized;advanced;deep}                      ||   Choose the generation mode.
Exemple : python main.py informations.txt -m advanced

-p, --permutation [number_of_max_permutation]         ||   Number of maximum combinations for information permutations.
exemple : main.py informations.txt -p 3


-s, --symbol [number_of_maximum_symbol]            ||   Number of replacements with symbols, exemple: @lice = Alic€, @lic€, ... (testing all combinations).
exemple : main.py informations.txt -s 3


-d, --digit [number_of_maximum_digit]              ||   Number of replacements with digit, exemple: Alice = 4lice, Al1ce, ... (testing all combinations).
exemple : main.py informations.txt -d 3


-f, --firstupper [Yes;No]                          ||   Enable/Disable (Y/N) the function to uppercase the first letter only.
exemple : main.py informations.txt -f


-l, --lowercase [Yes;No]                           ||   Enable/Disable (Y/N) the function to lowercase the entire password.
exemple : main.py informations.txt -l


-a, --allupper [number_of_maximum_uppercase]       ||   Number of replacements with uppercase letters (testing all combinations).
exemple : main.py informations.txt -a 2


-b, --double_letter [Yes;No]                       ||    Enable/Disable (Y/N) the function to double the last letter if it is a vowel, ex: Mia = Miaa.


-c, --character {1,2,3,0}                          ||   This feature introduces additional characters at each level, expanding the range of possibilities.
exemple : main.py informations.txt -c                               - Level 1 include ["1", "123", "0", "."]
                                                                    - Level 2 includes ["1", "123", "0", ".", "!", "*"]
                                                                    - Level 3 includes ["1", "123", "0", ".", "!", "*", "00","2000"]
				                                    --> The 0 simply deactivates the functionality.


-w, --wordlist [wordlist_file,wordlist_file2,...]              ||   Add one or more additional wordlists that we will add to our generation (put a ',' to separate if there are several).
exemple : main.py informations.txt -w digit_passwords.txt


--all_option [number_of_maximum_for_all_value]                 ||   Set all values to the same chosen value and enable all functions (except -w, --merge)
exemple : main.py informations.txt --all_option 2


-o, --output_file [output_file_path]                           ||   default='FxWordlist.txt', The path for the output file wordlist,
                                                                    by default the output file will be located in the directory where you started the program.
exemple : main.py informations.txt -m soft -o my_file.txt


--merge [file_to_merge,file_to_merge2,...]                     ||    Merge one or more extra word lists with our generated content from user information, creating multiple combinations between files
						    		     (put a ',' to separate if there are several).
exemple : main.py informations.txt --merge digit_passwords.txt


--ext_merge [file1.txt,file2.txt,file3.txt...]                 ||    Merge various external wordlists while excluding the use of target information, creating multiple combinations between files										     (put a ',' to separate if there are several).

exemple : main.py --ext_merge wordlist1.txt,0_2050.txt,digit_passwords.txt


############################################################################################################################################
#                                                                                                                                          #                 
#  IMPORTANT :                                                                                                                             #
#                                                                                                                                          #
#  - In cases of minimal information, consider experimenting with the "--merge" option using various wordlists.                            #
#    This approach can prove beneficial in diversifying password combinations by incorporating external sources.                           #
#    The program provides 2 wordlists which can be very useful for the merge (digit_passwords.txt & 0_2050.txt)                            #  
#                                                                                                                                          #
#  - If you use the "--merge" option or "-m deep", the number of passwords may increase significantly.                                     #
#    To reduce this impact you can disable features like "character" and "double_letter" or reduce "all_upper":                            #
#  --> python main.py information.txt -c0 -b0 ...                                                                                          #
#                                                                                                                                          #
############################################################################################################################################

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Future updates will add several new features, such as the ability to create your own mode without having to retype your entire setup.
Note: Always consider ethical and legal aspects when creating and using password lists.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Flegh113.
