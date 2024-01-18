"""
Polaczenia do bazy sqlite przestawiono na tryb concurrency, poprzednia wersja postgresql dzialala po staremu,
tylko speedtesty byy zadeklarowane na concurrency.
1.) powstal nowy plik database_sqlite.py
2.) zmieniono w user_sql.py polaczenia do bazy sql oraz na tryb concurrency
3.) zmieniono w zapytaniach "%s" na "?" oraz SELECT_COUNTER_UNREAD_WITH_SB, mozna sobie porownac stara i nowa wersje
4.) w sql w obiekcie messenges kolumna is_read zmieniono na notacje 0/1 zamiast true/false-> zapisy i odczyty
5.) odczyt dziala, zapis juz nie. pojawia sie plik sqlite.db-journal ??? connection.commit() sqlite3.OperationalError:
cannot commit transaction - SQL statements in progress
Błąd sqlite3.OperationalError: cannot commit transaction - SQL statements in progress oznacza, że istnieje transakcja,
która jest w trakcie wykonywania i nie została zakończona, a próba wykonania kolejnej transakcji została podjęta. SQLite
nie pozwala na zagnieżdżanie transakcji, więc próba rozpoczęcia nowej transakcji w momencie, gdy już istnieje inna, może
prowadzić do tego rodzaju błędu.

Aby to naprawić, upewnij się, że poprzednia transakcja została zakończona przed rozpoczęciem nowej. Możesz to osiągnąć,
wykonując commit lub rollback na obecnej transakcji. Na przykład:

AKTUALIZACJA!
ad.5) dziala czyli wysylanie (send), ale w momencie jak sie kliknie show_conwersation, wtedy jakby tez zatwierdzana komunuikacja jakby
no i sie zapisuje w bazie danych!


"""