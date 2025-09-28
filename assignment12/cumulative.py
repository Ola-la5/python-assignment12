import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

#task2
with sqlite3.connect("../db/lesson.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1") 
    
sql_statement = """SELECT o.order_id,
                 SUM(li.quantity * p.price) AS total_price
                 FROM orders o
                 JOIN line_items li ON o.order_id = li.order_id
                 JOIN products p ON li.product_id = p.product_id
                 GROUP BY o.order_id
                 ORDER BY o.order_id;"""


df=pd.read_sql_query(sql_statement, conn)

def cumulative(row):
    totals_above = df['total_price'][0:row.name+1]
    return totals_above.sum()

df['cumulative_apply'] = df.apply(cumulative, axis=1)


print(df)
df.plot(x="order_id", y=["total_price", "cumulative_apply"], kind="line", title="cumulative revenue vs. order_id")
plt.show()

#task3
import plotly.express as px
import plotly.data as pldata
df_3 = pldata.wind(return_type='pandas')

print(df_3.head(10))
print(df_3.tail(10))

df_3['strength'] = df_3['strength'].str.replace(r'[^\d.]', '', regex=True).astype(float)
fig = px.scatter(df_3, x='strength', y='frequency', color='direction',
                 title="strength vs. frequency", hover_data=["direction"])
fig.write_html("wind.html", auto_open=True)