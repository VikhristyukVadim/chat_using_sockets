# from client_socket import client

if __name__ == '__main__':
    print("US")

    login = int(111)
    password = int(222)


    def logining():
        print("Введите логин:")
        log = input()
        print("Введите пароль:")
        pas = input()
        if int(log) == login and int(pas) == password:
            print("Вот вы и вошли")
            # client()

        else:
            print("try again")
            logining()


    logining()


