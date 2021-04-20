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

def GraphFour(counties, start, end, connection):
    
        whereClause = f"WHERE name IN ({str(counties).replace('[', '').replace(']','')})"

        if start != '':
            whereClause = whereClause + f" AND (year >= {str(start)[0:4]})"

        if end != '':
            whereClause = whereClause + f" AND (year <= {str(end)[0:4]})"

        dbQuery = """
        SELECT countyFIPS, name, year, (sum_AB / SQRT(sum_a2 * sum_b2)) AS correlation_coefficient  --Computes correlation for each year
        FROM
                (
                SELECT countyFIPS, year, SUM(AB) AS sum_AB, SUM(a_sqr) AS sum_a2, SUM(b_sqr) AS sum_b2 --Sums up relevant values to compute correlation for each year
                FROM
                        (
                        SELECT countyFIPS, year, month, a, b, (a * b) AS AB, POWER(a, 2) AS a_sqr, POWER(b, 2) AS b_sqr --Calculates relevant values for correlation equation
                        FROM
                                (
                                SELECT countyFIPS, uv_year AS year, uv_month AS month, mean_uv, uv_value, (uv_value - mean_uv) AS a --Calculates difference of mean from value for correlation calculation
                                FROM
                                        (
                                        SELECT countyFIPS, uv_year, AVG(uv_value) AS mean_UV --Groups by county and year, calculates average UV value for the summer (May - September)
                                        FROM
                                                (
                                                SELECT countyFIPS, uv_year, uv_month, uv_value --For some reason cannot group in this SELECT statement? Selects summer months (May - September)
                                                FROM rc4.Average_UV_Irradiance
                                                WHERE uv_month >= 5 AND uv_month <= 9
                                                )
                                        GROUP BY countyFIPS, uv_year
                                        )
                                NATURAL JOIN
                                        (SELECT * FROM rc4.Average_UV_Irradiance WHERE uv_month >= 5 AND uv_month <= 9) --Joins with UV Irradiance to get the monthly values to calculate difference with mean
                                )  
                        NATURAL JOIN
                                (
                                SELECT countyFIPS, year, month, mean_heat_year, month_average, (month_average - mean_heat_year) AS b --Calculates difference of mean from value for correlation calculation
                                FROM
                                        (
                                        SELECT countyFIPS, year, AVG(heat_value) AS mean_heat_year --Calculates yearly heat averages
                                        FROM (  SELECT t.*, EXTRACT(YEAR FROM HI_Date) AS year, TO_CHAR(HI_Date, 'mm') AS month --Extracts year and month
                                                FROM rc4.Heat_Index t
                                                )
                                        WHERE year >= 2005
                                        GROUP BY countyFIPS, year
                                        )
                                NATURAL JOIN
                                        (
                                        SELECT countyFIPS, year, month, AVG(heat_value) AS Month_Average --Calculates monthly averages
                                        FROM (  SELECT t.*, EXTRACT(YEAR FROM HI_Date) AS year, TO_CHAR(HI_Date, 'mm') AS month --Extracts year and month
                                                FROM rc4.Heat_Index t
                                                )
                                        WHERE year >= 2005
                                        GROUP BY countyFIPS, year, month
                                        )
                                )
                        )
                GROUP BY countyFIPS, year
                )
        NATURAL JOIN
                rc4.County
        %s
        ORDER BY countyFIPS ASC, year ASC
        """ % (whereClause)

        cursor = connection.cursor()

        data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

        x = []
        y = []

        for row in data:
            x.append(row[2])
            y.append(row[3])

        plt.clf()
        plt.plot(x, y)
        plt.xlabel('Year')
        plt.ylabel('Correlation Coefficient')
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                labelbottom=False  # labels along the bottom edge are off
        ) 

        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc


def GraphFive(counties, start, end, connection):
        outerWhereClause = f"AND name IN ({str(counties).replace('[', '').replace(']','')})"   

        if start != '':
                outerWhereClause = outerWhereClause + f" AND (year <= {str(start)[0:4]})"
        if end != '':
                outerWhereClause = outerWhereClause + f" AND (year <= {str(end)[0:4]})"
        

        dbQuery = """
        SELECT rc4.Heat_Index.countyFIPS, name, year, COUNT(*) as numHotDays --Counts the number of days hotter than the lower bound (x SDs away from mean) and orders
        FROM 
                (SELECT countyFIPS, name, year, (AVG(heat_value) - 1 * STDDEV(heat_value)) as lowerBoundSummer --Calculates x Standard Deviations away from the year's summer mean heat value (lower bound only)
                FROM (  SELECT t.*, rc4.county.name, EXTRACT(YEAR FROM HI_Date) as year --Extracts year for grouping
                        FROM rc4.Heat_Index t, rc4.county
                        WHERE t.countyFIPS = rc4.county.countyFIPS
                        )
                GROUP BY name, countyFIPS, year
                ) summerStats
        JOIN
                rc4.Heat_Index ON rc4.Heat_Index.countyFIPS = summerStats.countyFIPS
                                AND TO_CHAR(rc4.Heat_Index.HI_Date, 'YYYY') = summerStats.year
        WHERE heat_value >= lowerBoundSummer %s
        GROUP BY rc4.Heat_Index.countyFIPS, name, year
        ORDER BY rc4.Heat_Index.countyFIPS ASC, year ASC
        """ % (outerWhereClause)

        cursor = connection.cursor()

        data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

        x = []
        y = []

        for row in data:
            x.append(row[2])
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