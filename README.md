# FxWordlist Project - *Powerful Wordlist Generator.*

**Note:** The tool's efficiency is greatly enhanced when used proficiently. Adapt your configuration based on available information.

## Getting Started

To use this program effectively, follow these steps:

1. Write down all target information in a .txt file (firstname, lastname, date of birth, etc.). One piece of information per line.

    Example in "informations.txt":
    ```
    Alice
    Bob
    1990
    [...]
    ```

    OR

2. Use the -i command for interactive questions without a file.

    ```bash
    python main.py -i [options, e.g., -m soft]
    ```

## Usage

Don't forget to specify your "informations_file.txt" or use the -i command in your command line.

Examples:
1. `python main.py informations.txt -m soft`
2. `python main.py -m soft informations.txt`
3. `python main.py -i -m soft`
4. `python main.py -m soft -i`

---------------------------------------------------------------------------------------------------------

## This tool contains 4 modes for easy configuration:

`-m, --mode {soft;optimized;advanced;deep} || Choose the generation mode.`

- **_SOFT_**
command: python main.py informations.txt -m soft

1. Description :
>> Soft mode is used to generate small password lists. As a result, most of the program's functions will be toned down, allowing you to do less work.

2. Why use this mode ?
>> This mode doesn't involve any great complexity of passwords, which means it can be used as a basis for breaking a password that isn't very complex/robust.

---------------------------------------------------------------------------------------------------------

- **_OPTIMIZED_** (default mode)

`command: python main.py informations.txt (no need to specify mode, it's already the default if there's no option)`

1. Description :
>> Optimized mode is the default mode. It aims to generate password lists that optimize both quantity and quality. As a result, most of the program's features are probabilistically designed to retain only the most likely passwords. 

2. Why use this mode ?
>> This mode is widely preferred because it facilitates the creation of password lists that are not excessively voluminous, while focusing as much as possible on the probability of the passwords' existence.

---------------------------------------------------------------------------------------------------------

- **_ADVANCED_**
  
`command: python main.py informations.txt -m advanced`

1. Description :
>> This mode pushes generation further by implementing additional functions and increasing generation parameters, thus creating larger wordlists.

2. Why use this mode ?
>> If you really want to increase your chances of finding a password without worrying about its size, this may be the mode for you.

---------------------------------------------------------------------------------------------------------

- **_DEEP_**
  
`command: python main.py informations.txt -m deep`

1. Description :
>> This mode is very heavy, it will test a very large number of possibilities, which can easily make the wordlist absolutely enormous.

2. Why use this mode?
>> This mode should only be used if you have very little information about a person. That's why maximum rules have been included in its programming.
Beyond 3-4 pieces of information, it will generate so many passwords that it won't necessarily be useful (this also depends on the size of each piece of information).
However, if you don't have much information, it can be very useful for testing countless combinations.

---------------------------------------------------------------------------------------------------------

# CONFIGURATION

This tool is highly flexible, allowing you to tailor word lists to your specific needs using a variety of available options. You can also specify a mode and modify one or more of its values with commands, for example: `-m soft -p3 -a1 -s0` (0 disables)...

When you input any of these commands without specifying a mode, all other options will be automatically disabled, ensuring precise execution aligned with your intent. Feel free to combine them as needed:

For instance, using all commands:
```bash
main.py informations.txt -p2 -s3 -d2 -a3 -fY -lY -bY -c1 -w wordlist.txt --merge 0_2050.txt -o my_custom_wordlist.txt
```
## Available Options:

### - _Choose the generation mode._

>> `-m, --mode {soft;optimized;advanced;deep}`
```bash
>> python main.py informations.txt -m advanced
```
---

### - _Number of maximum combinations for information permutations._
>> `-p, --permutation [number_of_max_permutation]`
```bash
>> python main.py informations.txt -p 3
```
---

### - _Number of replacements with symbols, ex: @lice = Alic€, @lic€_
>> `-s, --symbol [number_of_maximum_symbol]`
```bash
>> python main.py informations.txt -s 3
```
---

### - _Number of replacements with digit, ex: Alice = 4lice, Al1c3_
>> `-d, --digit [number_of_maximum_digit]`
```bash
>> python main.py informations.txt -d 3
```
---

### - _Enable/Disable (Y/N) the function to uppercase the first letter only._
>> `-f, --firstupper [Yes;No] `
```bash
>> python main.py informations.txt -f Y
```
---

### - _Enable/Disable (Y/N) the function to lowercase the entire password._
>> `-l, --lowercase [Yes;No]`
```bash
>> python main.py informations.txt -l Y
```
---

### - _ Enable/Disable (Y/N) the function to double the last letter if it is a vowel, ex: Mia = Miaa._
>> `-b, --double_letter [Yes;No]`
```bash
>> python main.py informations.txt -b Y
```
---

### - _Number of replacements with uppercase letters (testing all combinations)._
>> `-a, --allupper [number_of_maximum_uppercase]`
```bash
>> python main.py informations.txt -a 2
```
---


### - _This feature introduces additional characters at each level, expanding the range of possibilities._
>> `-c, --character {1,2,3,0}`
- `Level 1 include ["1", "123", "0", "."]`
- `Level 2 includes ["1", "123", "0", ".", "!", "*"]`
- `Level 3 includes ["1", "123", "0", ".", "!", "*", "00","2000"]`
- `Level 0 simply deactivates the functionality.`
```bash
>> python main.py informations.txt -c 1
```
---

### - _Add one or more additional wordlists that we will add to our generation (put a ',' to separate if there are several)._
>> `-w, --wordlist [wordlist_file,wordlist_file2,...]`
```bash
>> python main.py informations.txt -w digit_passwords.txt
```
---

### - _Set all values to the same chosen value and enable all functions (except -w, --merge)._
>> `--all_option [number_of_maximum_for_all_value]`
```bash
>> python main.py informations.txt --all_option 2
```
---

### - _The path for the output file wordlist, by default the output file will be located in the directory where you started the program._
>> `-o, --output_file [output_file_path] | default='./FxWordlist.txt'`
```bash
>> python main.py informations.txt -m soft -o my_file.txt
```
---

### - _Merge one or more extra word lists with our generated content from user information, creating multiple combinations between files (put a ',' to separate if there are several)._
>> `--merge [file_to_merge,file_to_merge2,...]`
```bash
>> python main.py informations.txt --merge digit_passwords.txt
```
---

### - _ Merge various external wordlists while excluding the use of target information, creating multiple combinations between files (put a ',' to separate if there are several)._
>> `--ext_merge [file1.txt,file2.txt,file3.txt...]  `
```bash
>> python main.py --ext_merge wordlist1.txt,0_2050.txt,digit_passwords.txt
```
---


#  IMPORTANT :

  - In cases of minimal information, consider experimenting with the '--merge' option using various wordlists.
    This approach can prove beneficial in diversifying password combinations by incorporating external sources.
    The program provides 2 wordlists which can be very useful for the merge (digit_passwords.txt & 0_2050.txt). 

  - If you use the "--merge" option or "-m deep", the number of passwords may increase significantly.
    To reduce this impact you can disable features like "character" and "double_letter" or reduce "all_upper":
    'python main.py information.txt -c0 -b0 ...'
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Future updates will add several new features, such as the ability to create your own mode without having to retype your entire setup.
Note: Always consider ethical and legal aspects when creating and using password lists.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Flegh113.
