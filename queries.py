import pandas as pd
from matplotlib import pyplot as plt
from db_conn import connect
from sklearn.feature_extraction.text import CountVectorizer


def emailsPerMonth():
    conn = connect()

    query = '''SELECT strftime('%Y-%m', date) AS month, COUNT(*) as message_count
                FROM message
                WHERE month >= '1997-01' AND month <= '2002-12'
                GROUP BY month'''
    
    df = pd.read_sql_query(query, conn)

    month = df['month']
    count = df['message_count']

    plt.figure(figsize=(50,15))
    plt.title("Total Messages per Month")
    plt.ylabel("Messages")
    plt.xlabel("Month")
    plt.plot(month, count)
    plt.show()


def topSenders():
    conn = connect()

    query = '''SELECT COUNT(mid) as count, sender
FROM message
WHERE date BETWEEN '1979-12-30' AND '2002-12-31'
GROUP BY sender
ORDER BY count DESC
LIMIT 10'''
    
    df = pd.read_sql_query(query, conn)

    sender = df['sender']
    count = df['count']

    sender = sender[::-1]
    count = count[::-1]

    plt.title("Top 10 Senders")
    plt.ylabel("Sender")
    plt.xlabel("Emails")
    plt.barh(sender, count)
    for i, v in enumerate(count):
        plt.text(v, i, str(v), ha='right', va='center')
    plt.show()

def topRecipients():
    conn = connect()

    query = '''SELECT COUNT(rid) as count, rvalue
FROM recipientinfo NATURAL JOIN message
WHERE date BETWEEN '1979-12-30' AND '2002-12-31'
GROUP BY rvalue
ORDER BY count DESC
LIMIT 10'''
    
    df = pd.read_sql_query(query, conn)

    recipient = df['rvalue']
    count = df['count']

    recipient = recipient[::-1]
    count = count[::-1]

    plt.title("Top 10 Recipients")
    plt.ylabel("Recipient")
    plt.xlabel("Emails")
    plt.barh(recipient, count)
    for i, v in enumerate(count):
        plt.text(v, i, str(v), ha='right', va='center')
    plt.show()

def typeDis():
    conn = connect()

    query = '''SELECT COUNT(rtype) as count, rtype
FROM recipientinfo
GROUP BY rtype'''
    
    df = pd.read_sql_query(query, conn)

    rtype = df['rtype']
    count = df['count']

    plt.title("Email Type Distribution")
    plt.axis('equal')
    plt.pie(count, labels=rtype, autopct='%1.1f%%')
    plt.show()

def keywords():
    vect = CountVectorizer()

    conn = connect()

    query = '''SELECT date, subject
FROM message
WHERE date BETWEEN '1979-12-30' AND '2002-12-31'
ORDER BY date DESC'''
    
    df = pd.read_sql_query(query, conn)

    x = vect.fit_transform(df['subject'])

    keywords = vect.get_feature_names_out()

    keywords_count = x.sum(axis=0)

    df_keywords = pd.DataFrame({'Keyword': keywords, 'Count': keywords_count.tolist()[0]})

    df_keywords = df_keywords.sort_values('Count', ascending=False)

    df_keywords_10 = df_keywords.head(10)

    words = df_keywords_10['Keyword'].values
    count = df_keywords_10['Count'].values

    words = words[::-1]
    count = count[::-1]

    plt.title("Top 10 Subject Keywords")
    plt.ylabel("Keyword")
    plt.xlabel("Count")
    plt.barh(words, count)
    for i, v in enumerate(count):
        plt.text(v, i, str(v), ha='right', va='center')
    plt.show()


def extAndInt():
    conn = connect()

    query = '''SELECT SUM(CASE WHEN e.eid IS NULL THEN 1 ELSE 0 END) as external, SUM(CASE WHEN e.eid IS NOT NULL THEN 1 ELSE 0 END) as internal
FROM recipientinfo as ri
JOIN message as m ON m.mid = ri.mid
JOIN employeelist as e2 ON e2.Email_id = m.sender
LEFT JOIN employeelist as e ON e.Email_id = ri.rvalue
WHERE m.date BETWEEN '1979-12-30' AND '2002-12-31'
'''

    
    df = pd.read_sql_query(query, conn)

    type = ['Internal', 'External']
    count = [int(df['internal'].iloc[0]), int(df['external'].iloc[0])]
    print(count)

    plt.title("Email Type Distribution")
    plt.axis('equal')
    plt.pie(count, labels=type, autopct='%1.1f%%')
    plt.show()