from pprint import pprint
import time
CREATE_ACCOUNT = """CREATE TABLE IF NOT EXISTS account 
(id_account SERIAL PRIMARY KEY, nick TEXT, password TEXT, admin BOOLEAN);"""

CREATE_CONVERSATION = """CREATE TABLE IF NOT EXISTS conversation
(id_conversation SERIAL PRIMARY KEY, id_receiver INTEGER, id_sender INTEGER,
FOREIGN KEY(id_sender) REFERENCES account (id_account),
FOREIGN KEY(id_receiver) REFERENCES account (id_account));"""

CREATE_MESSAGE = """CREATE TABLE IF NOT EXISTS message
(id_message SERIAL PRIMARY KEY, receiver_sender TEXT, content TEXT, time TEXT, is_read BOOLEAN,
id_conversation INTEGER, FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation));"""

SELECT_LIST_USERS = """select nick from account;"""
SELECT_BASE_INFO = """select a.nick, a."password", a."admin"  from account a 
where nick = %s;"""
SELECT_NICKS_CONVERSATION = """SELECT
    CASE
        WHEN %s = c.id_receiver THEN (SELECT aa.nick FROM account aa WHERE aa.id_account = c.id_sender)
        WHEN %s = c.id_sender THEN (SELECT aa.nick FROM account aa WHERE aa.id_account = c.id_receiver)
    END AS return_value
FROM conversation c
WHERE %s IN (c.id_receiver, c.id_sender);"""
SELECT_ID_ACCOUNT_BY_NICK = """select id_account from account where nick = %s;"""
SELECT_COUNT_UNREAD_MESSAGES = """select a.nick, (select aa.nick as _from from
account aa
where aa.id_account = (select case 
	when cc.id_receiver = a.id_account then cc.id_sender
	else cc.id_receiver
end as return_value
from conversation cc 
where cc.id_conversation = c.id_conversation)), count(m.is_read is null) as unread_messages
from account a, conversation c 
inner join message m on m.id_conversation = c.id_conversation 
where (a.nick = %s and ((c.id_receiver = a.id_account and m.receiver_sender = 'send_to_receiver')
or (c.id_sender = a.id_account and m.receiver_sender = 'from_receiver')) and m.is_read = False)
group by a.nick, _from;"""
SELECT_UNREAD_MESSAGES = """select a.nick, c.id_conversation, m.id_message, (select aa.nick as _from from
account aa
where aa.id_account = (select case 
	when cc.id_receiver = a.id_account then cc.id_sender
	else cc.id_receiver
end as return_value
from conversation cc 
where cc.id_conversation = c.id_conversation)),
m."content" as unread_message
from account a, conversation c 
inner join message m on m.id_conversation = c.id_conversation 
where (a.nick = %s and ((c.id_receiver = a.id_account and m.receiver_sender = 'send_to_receiver')
or (c.id_sender = a.id_account and m.receiver_sender = 'from_receiver')) and m.is_read = FALSE)
order by c.id_conversation, m."time" ;"""
SELECT_CONVERSATION_WITH_SB = """select (select nick from account a
where a.id_account = c.id_receiver) as receiver, (select nick from account a
where a.id_account = c.id_sender) as sender, m.receiver_sender, m."content", m."time"from conversation c 
inner join message m on m.id_conversation = c.id_conversation 
where (select a2.id_account from account a2 where a2.nick = %s) in (id_receiver,id_sender) 
and (select a2.id_account from account a2 where a2.nick = %s) in (id_receiver,id_sender)
order by m."time";"""
SELECT_COUNTER_UNREAD_WITH_SB = """create OR REPLACE view count_unread as select a.nick, (select aa.nick as _from from
account aa
where aa.id_account = (select case 
	when cc.id_receiver = a.id_account then cc.id_sender
	else cc.id_receiver
end as return_value
from conversation cc 
where cc.id_conversation = c.id_conversation)) as _from, count(m.is_read is null) as unread_messages
from account a, conversation c 
inner join message m on m.id_conversation = c.id_conversation 
where (a.nick = %s and ((c.id_receiver = a.id_account and m.receiver_sender = 'send_to_receiver')
or (c.id_sender = a.id_account and m.receiver_sender = 'from_receiver')) and m.is_read = False)
group by a.nick, _from;
select * from count_unread where _from = %s;"""
SELECT_SENDER_OR_RECEIVER = """select nick, case 
	when a4.id_account = c.id_receiver then 'from_receiver'
	when a4.id_account = c.id_sender  then 'send_to_receiver'
end as return_value
from conversation c
inner join account a4 on a4.id_account = (select a2.id_account from account a2 where a2.nick = %s)
where a4.id_account in (id_receiver,id_sender) and 
(select a3.id_account from account a3 where a3.nick = %s) in (id_receiver,id_sender);"""
SELECT_ID_CONVERSATION = """select c.id_conversation  from conversation c 
where (select a.id_account from account a where a.nick=%s) in (c.id_receiver, c.id_sender) and 
(select a2.id_account from account a2 where a2.nick=%s) in (c.id_receiver, c.id_sender)"""
INSERT_NEW_USER = """INSERT INTO account (nick, password, admin) 
VALUES (%s, %s, %s) RETURNING id_account;"""
INSERT_NEW_CONVERSATION = """insert into conversation (id_receiver, id_sender)
VALUES((select a.id_account from account a where a.nick=%s), 
(select a2.id_account from account a2 where a2.nick=%s)) returning id_conversation;"""
INSERT_MESSAGE = """insert into message (receiver_sender, content, time, is_read, id_conversation) 
values (%s, %s, %s, %s, %s) RETURNING id_message;"""
UPDATE_UNREAD_MESSAGES = """update message 
set is_read = True
where id_message = %s;"""

"""
zerowanie licznika klucza głównego:
ALTER SEQUENCE conversation_id_conversation_seq RESTART WITH 1;

"""


def change_sth_test(connetion):
    with connetion.get_cursor() as cursor:
        cursor.execute("""update message
    set content = 'He Ol'
    where id_message = 1;""")


def get_list_nicks(connection):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_LIST_USERS)
        return cursor.fetchall()


def get_list_nicks2(connection):
    cursor = connection.cursor()
    cursor.execute(SELECT_LIST_USERS)
    time.sleep(1)
    return cursor.fetchall()


def get_base_info(connection, nick):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_BASE_INFO, (nick,))
        return cursor.fetchone()


def add_new_user(connection, nick, password, admin):
    with connection.get_cursor() as cursor:
        cursor.execute(INSERT_NEW_USER, (nick, password, admin))
        return cursor.fetchall()[0]


def get_nicks_conversation(connection, nick="Seba"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_ID_ACCOUNT_BY_NICK, (nick,))
        try:
            idd = cursor.fetchone()[0]
            cursor.execute(SELECT_NICKS_CONVERSATION, (idd, idd, idd))
        except TypeError:
            return []
        return cursor.fetchall()


def get_counter_unread_messages(connection, nick="Seba"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_COUNT_UNREAD_MESSAGES, (nick,))
        return cursor.fetchall()


def get_unread_messages(connection, nick="Seba"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_UNREAD_MESSAGES, (nick,))
        return cursor.fetchall()


def update_unread_message(connection, id_message):
    with connection.get_cursor() as cursor:
        cursor.execute(UPDATE_UNREAD_MESSAGES, (id_message,))


def get_conversation_by_nick(connection, my_account="Seba", with_nick="Olaf"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_CONVERSATION_WITH_SB, (my_account, with_nick))
        return cursor.fetchall()


def get_counter_unread_messages_with_sb(connection, my_nick="Seba", with_nick="Olaf"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_COUNTER_UNREAD_WITH_SB, (my_nick, with_nick))
        return cursor.fetchall()[0]


def determine_sender_or_receiver(connection, my_nick="Seba", with_nick="Olaf"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_SENDER_OR_RECEIVER, (my_nick, with_nick))
        return cursor.fetchall()


def add_conversation(connection, my_nick="Seba", with_nick="Default"):
    with connection.get_cursor() as cursor:
        cursor.execute(INSERT_NEW_CONVERSATION, (with_nick, my_nick))
        return cursor.fetchall()


def get_id_conversation(connection, nick1="Seba", nick2="Olaf"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_ID_CONVERSATION, (nick1, nick2))
        return cursor.fetchone()[0]


def add_message(connection, text, id_conversation):
    with connection.get_cursor() as cursor:
        cursor.execute(INSERT_MESSAGE, (text[0], text[2], text[1], "False", id_conversation))
        return cursor.fetchall()[0][0]
