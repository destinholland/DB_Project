import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def GraphOne(counties, start, end, connection):

        whereClause = f"WHERE name IN ({str(counties).replace('[', '').replace(']','')})"

        if start != '':
            whereClause = whereClause + f" AND (year >= {str(start)[0:4]})"

        if end != '':
            whereClause = whereClause + f" AND (year <= {str(end)[0:4]})"

        dbQuery = """
        SELECT name, year, month, Month_Average --Retrieves relevant information (Removes mnum that was used for ordering)
        FROM 
                (
                SELECT rc4.County.name, year, month, Month_Average, mnum --Joins with county to get county names and orders data
                FROM (
                        SELECT countyFIPS, year, month, AVG(heat_value) as Month_Average, mnum --Calculates monthly averages
                        FROM (  SELECT t.*, EXTRACT(YEAR FROM HI_Date) as year, TO_CHAR(HI_Date, 'Month') as month, TO_CHAR(HI_Date, 'mm') as mnum --Extracts year and month
                                FROM rc4.Heat_Index t
                                )
                        GROUP BY countyFIPS, year, month, mnum
                        )
                        NATURAL JOIN
                                rc4.County
                ORDER BY rc4.County.name ASC, year ASC, mnum ASC
                )
        %s
        """ % (whereClause)

        cursor = connection.cursor()

        data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

        x = []
        y = []

        for row in data:
            x.append(row[2] + str(row[1]))
            y.append(row[3])

        plt.clf()
        plt.plot(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                labelbottom=False  # labels along the bottom edge are off
        ) 

        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc

def GraphThree(counties, start, end, threshold, connection):

        outerWhereClause = f"WHERE name IN ({str(counties).replace('[', '').replace(']','')})"

        if start != '':
                outerWhereClause = outerWhereClause + f" AND (year >= {str(start)[0:4]})"

        if end != '':
                outerWhereClause = outerWhereClause + f" AND (year <= {str(end)[0:4]})"

        if threshold == '':
                heatThreshold = "85"
        else:
                heatThreshold = threshold

        dbQuery = """
        SELECT name, year, month, numHotDays --Gets relevant information (Removes mnum that was used for ordering)
        FROM 
                (
                SELECT name, countyFIPS, year, month, count(*) as numHotDays, mnum --Counts the number of days hotter than 85 degrees (variable: user input)
                FROM (  SELECT rc4.County.name, t.*, EXTRACT(YEAR FROM HI_Date) as year, TO_CHAR(HI_Date, 'Month') as month, TO_CHAR(HI_Date, 'mm') as mnum --Extracts year and month
                        FROM rc4.Heat_Index t, rc4.County
                        WHERE t.countyFIPS = rc4.County.countyFIPS
                        )
                WHERE heat_value > %s
                GROUP BY name, countyFIPS, year, month, mnum
                ORDER BY countyFIPS ASC, year ASC, mnum ASC
                )
        %s
        """ % (heatThreshold, outerWhereClause)

        cursor = connection.cursor()

        data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

        x = []
        y = []

        for row in data:
                x.append(row[2] + str(row[1]))
                y.append(row[3])

        plt.clf()
        plt.plot(x, y)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                labelbottom=False  # labels along the bottom edge are off
        )

        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc