from data.init_db import initialize_database
from views.insight_view import insightView
from views.authentication_view import employeeView, clientView

if __name__ == "__main__":
    initialize_database()
    print()

    print("System start with sucess!")
    print()




    while True:
        try:
            #print("<-----Commands to manager insights----->")
            #print()
            #print("Type 1 to create a insight")
            #print("Type 2 to return all insights")
            #print()

            print("<-----Commands to manager users----->")
            print()
            print("Type 3 to create a employee")
            print("Type 4 to return all employees")
            print("Type 5 to create a client")
            print("Type 6 to return all clients")
            print()
            command = input("Type a command (or 'Ctrl+C' to close): ")
            print()

            match command:
                case "1":   insightView().create()
                case "2":   insightView().get_all()
                case "3":   employeeView().create()
                case "4":    ...
                case "5":   clientView().create()
                case "6":   clientView().get_all()
                    

        except KeyboardInterrupt:
            print("System close")
            break