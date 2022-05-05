import re
import sqlparse
import pyodbc
import build
"""
Run a database trace with "RPC Completed" and "SP Completed" selected.  Save the trace in XML format.  Use that file's 
name and path in the 'open' statement below.
"""

connPlay = pyodbc.connect(
    '''
    DRIVER={{SQL Server}};
    SERVER={2};
    DATABASE={0};
    UID=Avatar;
    PWD={1};
    '''.format(build.play_database, build.avatar_password, build.play_server)
)


#  https://regex101.com/

CLEANR = re.compile('<.*?>')
# csv with a single quote (') as the string delimiter
CSV = re.compile(r"(?:,|\n|^)('(?:(?:'')*[^']*)*'|[^',\n]*|(?:\n|$))")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file1 = open(r'C:\Users\geoff.ritchey\Documents\GitHub\campus\db\trace.xml', 'r', encoding='utf-16', newline="\r\n")
    while True:
        line = file1.readline()
        if not line:
            break
        if "exec sp_executesql N'" in line:
            line = re.sub(CLEANR, '', line)
            line = line.replace("\r", " ")
            line = line.replace("exec sp_executesql N'", "'")
            line = line.replace(",N'", ",'")

            match = re.findall(CSV, line.strip(" "))
            query = match[0]
            query = query.replace("&lt;", "<")
            query = query.replace("&gt;", ">")
            query = query.replace("''", "'")
            params = match[1]
            print(params)
            variables = []
            i = 2
            while i < len(match)-1:
                variables.append(match[i])
                i = i+1
            print("variables: ", variables)
            i = 1
            query = query.strip("'")
            query2 = str(query)
            for variable in variables:
                query = query.replace("@P" + str(i), variable)
                query2 = query2.replace("@P" + str(i), "#{P" + str(i) + "}")
                i = i + 1
            print("")
            print("Parameter QUERY: ")
            print(sqlparse.format(query, reindent=True, keyword_case="upper"))
            print("")
            print(sqlparse.format(query2, reindent=True, keyword_case="upper"))
            print("")

            if query.lower().startswith("select"):
                cur = connPlay.cursor()
                try:
                    cur.execute(query)
                    for x in cur.fetchall():
                        print(x)
                    cur.close()
                    print()
                    print()
                    print()
                except:
                    pass
        elif 'name="TextData"' in line:
            line = re.sub(CLEANR, '', line)
            line = line.replace("\r", " ")
            line = line.strip(" ")
            query = line
            query = query.replace("&lt;", "<")
            query = query.replace("&gt;", ">")
            print("")
            print(sqlparse.format(query, reindent=True, keyword_case="upper"))
            print("")
            try:
                if query.lower().startswith("select") and '@' not in query:
                    cur = connPlay.cursor()
                    cur.execute(query)
                    for x in cur.fetchall():
                        print(x)
                    cur.close()
                    print()
                    print()
                    print()
            except:
                pass



    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
