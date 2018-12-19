def main():
    "Python program to emulate assembly language from input."
    reg0 = 0
    reg1 = 867  # a
    # reg1 = 10551267   # b
    reg2 = 0
    reg3 = 1
    reg4 = 31   # a
    # reg4 = 10550400   # b
    reg5 = 0
    print(reg0, reg1, reg2, reg3, reg4, reg5)
    while True:
        reg2 = 1
        # print('reg3 =', reg3)
        while reg2 <= reg1:
            reg4 = reg3 * reg2
            if reg4 == reg1:
                reg0 += reg3
                print('!{} = {} * {}'.format(reg4, reg2, reg3))
                # print(reg0, reg1, reg2, reg3, reg4, reg5)
            else:
                reg2 += 1
            reg2 += 1
        # print('exited inner loop')
        reg3 += 1

        if reg3 > reg1:
            break
    print(reg0, reg1, reg2, reg3, reg4, reg5)


if __name__ == '__main__':
    main()
