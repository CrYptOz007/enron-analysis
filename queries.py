import pandas as pd
from matplotlib import pyplot as plt
from db_conn import connect
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text

####################################
## Number of Emails Sent Per Month
####################################
def emailsPerMonth():
    conn = connect()

    # Query
    query = '''SELECT strftime('%Y-%m', date) AS month, COUNT(*) as message_count
                FROM message
                WHERE month >= '1997-01' AND month <= '2002-12'
                GROUP BY month'''
    
    # Read the query and convert into dataframe
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    # Convert into array for x and y
    month = df['month']
    count = df['message_count']

    # Plot the line graph
    plt.figure(figsize=(50,15))
    plt.title("Total Messages per Month")
    plt.ylabel("Messages")
    plt.xlabel("Month")
    plt.plot(month, count)
    plt.show()

####################################
## Number of Emails Sent per Sender
####################################
def topSenders():
    conn = connect()

    # Query
    query = '''SELECT COUNT(mid) as count, sender
                FROM message
                WHERE date BETWEEN '1979-12-30' AND '2002-12-31'
                GROUP BY sender
                ORDER BY count DESC
                LIMIT 10'''
                    
    # Read the query and convert into dataframe
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    # Convert into array for x and y
    sender = df['sender']
    count = df['count']

    # Reorder into descending order for graph
    sender = sender[::-1]
    count = count[::-1]

    # Plot the horizontal bar graph
    plt.title("Top 10 Senders")
    plt.ylabel("Sender")
    plt.xlabel("Emails")
    plt.barh(sender, count)
    # Add labels for the bar graph
    ###############################
    # SOURCE: CHATGPT
    for i, v in enumerate(count):
        plt.text(v, i, str(v), ha='right', va='center')
    ###############################
    plt.show()


###########################################
## Number of Emails Recieved per Recipient
###########################################
def topRecipients():
    conn = connect()

    # Query
    query = '''SELECT COUNT(rid) as count, rvalue
                FROM recipientinfo NATURAL JOIN message
                WHERE date BETWEEN '1979-12-30' AND '2002-12-31'
                GROUP BY rvalue
                ORDER BY count DESC
                LIMIT 10'''
    
    # Read the query and convert into dataframe
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    # Convert into array for x and y
    recipient = df['rvalue']
    count = df['count']

    # Reorder into descending order for graph
    recipient = recipient[::-1]
    count = count[::-1]

    # Plot the horizontal bar graph
    plt.title("Top 10 Recipients")
    plt.ylabel("Recipient")
    plt.xlabel("Emails")
    plt.barh(recipient, count)
    # Add labels for the bar graph
    ###############################
    # SOURCE: CHATGPT
    for i, v in enumerate(count):
        plt.text(v, i, str(v), ha='right', va='center')
    ###############################
    plt.show()


####################################
## Distribution of Sent Email types
####################################
def typeDis():
    conn = connect()

    # Query
    query = '''SELECT COUNT(rtype) as count, rtype
                FROM recipientinfo
                GROUP BY rtype'''
    
    # Read the query and convert into dataframe
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    # Convert into array for label and data
    rtype = df['rtype']
    count = df['count']

    # Plot the pie graph
    plt.title("Email Type Distribution")
    plt.axis('equal')
    plt.pie(count, labels=rtype, autopct='%1.1f%%')
    plt.show()


#######################################
## Top 10 words used in Email subject
#######################################
def keywords():

    conn = connect()

    # Query
    query = '''SELECT date, LOWER(subject) as subject
                FROM message
                WHERE date BETWEEN '1979-12-30' AND '2002-12-31'
                ORDER BY date DESC'''
    
    # Read the query and convert into dataframe
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    ###############################
    # SOURCE: CHATGPT
    
    # Define a list of stopwords
    stopwords = list(text.ENGLISH_STOP_WORDS)

    # CountVectorizer with stopwords filtering
    vect = CountVectorizer(stop_words=stopwords)

    # Fit and transform the email messages
    x = vect.fit_transform(df['subject'])

    # Get feature names 
    keywords = vect.get_feature_names_out()

    # Calculate the number of occured keyword
    keywords_count = x.sum(axis=0)

    # Create a dataframe with the keyword and number of occurances
    df_keywords = pd.DataFrame({'Keyword': keywords, 'Count': keywords_count.tolist()[0]})

    # Sort into descesding order
    df_keywords = df_keywords.sort_values('Count', ascending=False)

    # Grab the top 10
    df_keywords_10 = df_keywords.head(10)

    # END SOURCE
    ################################

    # Convert into array for x and y
    words = df_keywords_10['Keyword'].values
    count = df_keywords_10['Count'].values

    # Reorder into descending order for graph
    words = words[::-1]
    count = count[::-1]

    # Plot the horizontal bar graph
    plt.title("Top 10 Subject Keywords")
    plt.ylabel("Keyword")
    plt.xlabel("Count")
    plt.barh(words, count)
    # Add labels for the bar graph
    ###############################
    # SOURCE: CHATGPT
    for i, v in enumerate(count):
        plt.text(v, i, str(v), ha='right', va='center')
    ###############################
    plt.show()

#######################################################
## Distribution of external and internal communication
#######################################################
def extAndInt():
    conn = connect()

    # Query
    query = '''SELECT SUM(CASE WHEN e.eid IS NULL THEN 1 ELSE 0 END) as external, SUM(CASE WHEN e.eid IS NOT NULL THEN 1 ELSE 0 END) as internal
                FROM recipientinfo as ri
                JOIN message as m ON m.mid = ri.mid
                JOIN employeelist as e2 ON e2.Email_id = m.sender
                LEFT JOIN employeelist as e ON e.Email_id = ri.rvalue
                WHERE m.date BETWEEN '1979-12-30' AND '2002-12-31'
                '''

    # Read the query and convert into dataframe
    df = pd.read_sql_query(query, conn)

    # Close connection
    conn.close()

    # Convert into array for label and data
    type = ['Internal', 'External']
    count = [int(df['internal'].iloc[0]), int(df['external'].iloc[0])]

    # Plot the pie graph
    plt.title("Internal vs External Communication")
    plt.axis('equal')
    plt.pie(count, labels=type, autopct='%1.1f%%')
    plt.show()