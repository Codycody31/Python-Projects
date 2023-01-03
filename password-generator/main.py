# A simple password generator.

import random

# Define the characters that will be used to generate the password.
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
chars_alphanumeric = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
chars_alphabetical = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
chars_numeric = '1234567890'
chars_special = '!@#$%^&*()_+'

# Define the length of the password.
length = input('Password length? ')

# Define the number of passwords to generate.
number = input('Number of passwords? ')

# Define the type of characters to use.
print('''
Choose the type of characters to use:
1. Alphanumeric
2. Alphabetical
3. Numeric
4. Special
''')

choice = input('Choice? ')
if choice == '1':
    chars = chars_alphanumeric
elif choice == '2':
    chars = chars_alphabetical
elif choice == '3':
    chars = chars_numeric
elif choice == '4':
    chars = chars_special
else:
    print('Invalid choice. Using default characters.')
    quit()

# Convert the length and number variables to integers.
length = int(length)
number = int(number)

# Generate the passwords.
for p in range(number):
    password = ''
    for c in range(length):
        password += random.choice(chars)
    print(password)

# Save the passwords to a text file.
with open('passwords.txt', 'a') as f:
    for p in range(number):
        password = ''
        for c in range(length):
            password += random.choice(chars)
        f.write(password + '\n')
# End of script.
