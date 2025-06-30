import sqlite3 
import pandas as pd
from groq import Groq
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SQL_PATH = "C:/Users/krish/Documents/VS Code Projects/Generative AI/Ecommerce Tool/app/db.sqlite"
GROQ_MODEL = os.getenv('GROQ_MODEL')
client_sql = Groq()

sql_prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: product 

fields: 
product_link - string (hyperlink to product)	
title - string (name of the product)	
brand - string (brand of the product)	
price - integer (price of the product in Indian Rupees)	
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
total_ratings - integer (total number of ratings for the product)

</schema>
Make sure whenever you try to search for the brand name, the name can be in any case so convert the case to lower. 
So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
Create a single SQL query for the question provided. 
The query should have all the fields in SELECT clause (i.e. SELECT *)
Make sure to return a proper statement like there is no proper question provided to generate a SQL query for the same if you see an invalid question being passed as an input.

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags."""

comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in the following format when asked about a product: 
Produt title, price in indian rupees, discount, and rating, and then product link. Take care that all the products are listed in list format, one line after the other. Not as a paragraph.
For example:
1. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
2. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
3. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>

"""

def generate_sql_query(question: str) -> str:

    #call LLM to generate the answer
    chat_completion = client_sql.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": sql_prompt
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        model = os.environ['GROQ_MODEL'],
        temperature=0.2,
        max_tokens=1024,
    )

    return chat_completion.choices[0].message.content

def sql_chain(question):
    sql_query = generate_sql_query(question=question)
    pattern = "<SQL>(.*?)</SQL>"

    matches = re.findall(pattern, sql_query, re.DOTALL)

    if len(matches) == 0:
        return "Sorry, no query generated for this question"
    
    print('SQL QUERY:', matches[0].strip())
    response = run_query(matches[0].strip())

    if response is None:
        return "Sorry, no query generated for this question"
    
    context = response.to_dict(orient='records')
    answer = data_comprehension(question, context)
    return answer

def data_comprehension(question: str, context: str) -> str:

    #call LLM to generate the answer
    chat_completion = client_sql.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": comprehension_prompt
            },
            {
                "role": "user", 
                "content": f"QUESTION: {question} DATA: {context}"
            }
        ],
        model = os.environ['GROQ_MODEL'],
        temperature=0.2,
        # max_tokens=1024,
    )

    return chat_completion.choices[0].message.content

def run_query(query):
        
    if query.strip().upper().startswith('SELECT'):
        conn = sqlite3.connect(SQL_PATH)
        df = pd.read_sql_query(query, conn)

        return df
    
if __name__ == '__main__':
    # question = "Show me PuMa products having discount greater than 50% and rating greater than 4.5"
    question = "asfasfas"
    print(sql_chain(question))
