from connect_sql import GetConnection
import database
from threading import Thread
from time import perf_counter
import time
from concurrent.futures import ThreadPoolExecutor
from connection_pool import ConnectionPool, TooMuchConnections


def show_list_users2(connection):
    try:
        conn = connection.get_connection()
        return_list = [element[0] for element in database.get_list_nicks2(conn)]
        connection.release_connection(conn)
        print(return_list)
        return return_list
    except TooMuchConnections:
        print("To much connections")

if __name__ == "__main__":
    connection = ConnectionPool()
    check_connections = Thread(target=connection.check_amount_of_conections, daemon=True)
    check_connections.start()
    start_time = perf_counter()

    # with thread
    # 1 sposob
    # for _ in range(21):
    #     with ThreadPoolExecutor() as executor:
    #         executor.map(show_list_users2(connection))

    ######## zrobiem przerwy na inpucie zeby zobaczyc jak reagule program na przerwy (co 10 sekund)
    # 2 sposob
    input("something: ")
    threads = []
    for _ in range(330):
        t = Thread(target=show_list_users2, args=(connection,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    input("something: ")
    threads = []
    for _ in range(330):
        t = Thread(target=show_list_users2, args=(connection,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    input("something: ")

    end_time = perf_counter()
    print(f'It took {end_time - start_time :0.2f} second(s) to complete.')


"""
1 sposob:
klasa connection pool nie chciaa tworzyc nowych poczen, zamiast tego czekaa az sie zwolni polaczenie poprezednie
dziaa to bardziej po kolei nieli rwnolegle, dodajac 1 s delay w sqlu, program bedzie czeka tsekunde az sie zwolni polaczenie, mimo ze ma 19 polaczen
do dyspozycji


2 sposob: sephore max na 3/4 to wiecej sie zacina
na poczatku jest nawiazywana komunikacja, wszystkie polaczenia sa nawiazywane, potem dodawane sa kolejne az do 90 potem
dlugi okres gdzie sa zglaszane wyjatki(do poprawy, trwa to delay(1)), ale potem sa wypuszczane poprzednie polaczenia do 
kolejki i > 90 mozna przerabiac

"""