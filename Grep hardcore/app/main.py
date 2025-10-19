import sys

def handle_digits(string, index):
    return string[index].isdigit()


def handle_word_characters(string, index):
    if string[index].isalnum():
        return True
    elif string[index] == "_":
        return True
    return False


def handle_character_groups(string, index, group):
    if group[1] == "^":
        if string[index] in group[2:-1]:
            return False
        return True
    else:
        if string[index] in group[1:-1]:
            return True
        return False
    
    
def handle_literal_characters(string, index, character):
    if string[index] == character:
        return True
    return False


def handle_oneormore(string, index, token):
    repeat_times = 0
    while string[index] == token:
        repeat_times += 1
        if index == len(string) - 1:
            return repeat_times
        index += 1
    return repeat_times


def convert_to_commands(unsorted):
    sorted_commands = []
    #so if howto is \d a[abc][^rsa]\ws then this is ['\d',' ', 'a', '[abc]', ...]u get it
    i_alt = 0
    i_add = 0
    for i in range(len(unsorted)):
        i_alt = i + i_add#this works
        if i_alt == len(unsorted):
            #if the alt is at the end then there's nothing to do that's it
            break
        elif unsorted[i_alt] == "\\":
            #backlash done but doesnt account for \\ or dumb use of \
            sorted_commands.append(unsorted[i_alt:i_alt+2])
            i_add += 1
        elif unsorted[i_alt] == "[":#complicated...
            close_brackets = unsorted.find("]", i_alt)
            #dont account for [](correct syntax is [[] or []])
            if close_brackets == -1:
                #this is not necessary but idk helps the code
                print("yo where are the close brackets bring em")
                sys.exit(1)
            else:
                sorted_commands.append(unsorted[i_alt:close_brackets+1])
                i_add += close_brackets - i_alt
        else:
            sorted_commands.append(unsorted[i_alt])
    return sorted_commands


def handleInput(theinput, howto):
    commands = convert_to_commands(howto)
    print(commands)
    still_trying = True
    a = ""#anchor
    if "^" in commands:
        if "$" in commands:
            a = "^$"
        else:
            a = "^"
    elif "$" in commands:
        a = "$"
    first_index = 0#for seeing if first one true
    test_index = 0#for continuing after first one
    while still_trying:
        for i in range(len(commands)):
            if commands[i] == "^":
                if test_index == 0:
                    print("passed start anchor")
                    a.replace("^","")
                else:
                    first_index = len(theinput)
                    break
            elif commands[i] == "$":
                if test_index == len(theinput):
                    print("passed end anchor")
                    a.replace("$", "")
                else:
                    first_index = len(theinput)
                    break
            elif commands[i] == "\d":
                if handle_digits(theinput, test_index):
                    print("passed digits")
                    test_index += 1
                else:
                    break
            elif commands[i] == "\w":
                if handle_word_characters(theinput, test_index):
                    print("passed alnum")
                    test_index += 1
                else:
                    break
            elif commands[i].startswith("["):
                if handle_character_groups(theinput, test_index, commands[i]):
                    print("passed groups")
                    test_index += 1
                else:
                    break
            elif commands[i] == "+":
                if b := handle_oneormore(theinput, test_index, commands[i-1]):
                    print("passed +")
                    commands[i] == ""
                    test_index += b
                    print(test_index)
            else:
                if handle_literal_characters(theinput, test_index, commands[i]):
                    print("passed character")
                    test_index += 1
                else:
                    break
            if test_index == len(theinput) and i != len(commands) - 1:
                print("cant reach the end anymore, because test_index reached the end")
                sys.exit(1)
            if i >= len(commands) - 1:
                still_trying = False
                print("success is near baby")
        first_index += 1
        test_index = first_index
    print("congrats u made ur way to success")
    sys.exit(0)

    
def main():
    '''if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        sys.exit(1)
    handleInput(sys.stdin.read(), sys.argv[2])'''
    handleInput("act", "ca+t")
        
if __name__ == "__main__":
    main()