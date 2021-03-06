import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import datetime
from textwrap import wrap
from matplotlib.ticker import FormatStrFormatter

def GraphOne(counties, start, end, connection):
        plt.clf()
        legend = []

        for county in counties:
                legend.append(str(county))
                whereClause = f"WHERE name = \'" + str(county) + '\''

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
                        string = row[2] + ' ' + str(row[1])
                        dtValue = datetime.datetime.strptime(string, "%B %Y").date()
                        x.append(dtValue)
                        y.append(row[3])

                plt.plot(x, y, marker='o')

        plt.legend(labels=legend, fancybox=True, shadow=True)
        plt.xlabel('Month/Year')
        plt.ylabel('Average Monthly Heat Index')

        startMonth = ''
        endMonth = ''
        monthNum = [
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September')]

        for month in monthNum:
                if str(start)[5:7] == month[0]:
                        startMonth = month[1]
                if str(end)[5:7] == month[0]:
                        endMonth = month[1]
        title = "\n".join(wrap('Average Heat Index value From ' + startMonth + ', ' + str(start)[0:4] + " To " + endMonth + ', ' + str(end)[0:4] + ', by month', 50))
        plt.title(title)
        """ plt.tick_params(
                axis='x',          # changes apply to the x-axis
                labelbottom=False  # labels along the bottom edge are off
        ) """

        buf = BytesIO()
        plt.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc

def GraphTwo(county, ethnicities, start, end, connection):

        plt.clf()

        legend = []

        for ethnicity in ethnicities:
                ethnicName = ''
                ethnicCode = [
                ('1', 'White including Hispanic'),
                ('2', 'Black including Hispanic'),
                ('3', 'Asian/Pacific Islander including Hispanic'),
                ('4', 'American Indian/Alaskan Native including Hispanic'),
                ('5', 'Hispanic All Races'),
                ('6', 'All Non-White Races including Hispanic'),
                ('7', 'Other including Hispanic')]
                for code in ethnicCode:
                        if str(ethnicity) == code[0]:
                                ethnicName = code[1]

                legend.append(ethnicName)
                outerWhereClause = f"WHERE countyFIPS = " + str(county)

                # ethnicities2 = str(ethnicities).replace('[', '').replace(']', '').replace("'", '')
                outerWhereClause = outerWhereClause + f" AND (eID = {ethnicity})"

                if start != '':
                        outerWhereClause = outerWhereClause + f" AND (startYear >= {str(start)[0:4]})"

                if end != '':
                        outerWhereClause = outerWhereClause + f" AND (endYear <= {str(end)[0:4]})"

                dbQuery = """
                        SELECT countyFIPS, startYear, endYear, eID, name AS ethnicity, percentChange --Joins with Ethnicity table to get the full names of the ethnicities
                        FROM(
                            SELECT d1.countyFIPS, d1.year AS startYear, d2.year AS endYear, d1.ethnicity, (d2.ethnicPercent - d1.ethnicPercent) AS percentChange --Joins the two tables and calculates the difference(change) in ethnic percentage
                            FROM
                                (
                                SELECT countyFIPS, year, ethnicity, (ethnicPop / totalPop) AS ethnicPercent --Calculates the percentage of total population for each ethnicity
                                FROM(
                                    SELECT countyFIPS, demo_year AS year, ethnicity, SUM(population) as ethnicPop --Gets the population for each ethnicity for each county by year
                                    FROM rc4.Demographic
                                    GROUP BY countyFIPS, demo_year, ethnicity
                                    )
                                NATURAL JOIN(
                                    SELECT countyFIPS, demo_year AS year, SUM(population) AS totalPop --Gets the total population for each county by year
                                    FROM rc4.Demographic
                                    GROUP BY countyFIPS, demo_year
                                    )
                                ) d1
                            JOIN
                                (
                                SELECT countyFIPS, year, ethnicity, (ethnicPop / totalPop) AS ethnicPercent --Calculates the percentage of total population for each ethnicity
                                FROM(
                                    SELECT countyFIPS, demo_year AS year, ethnicity, SUM(population) as ethnicPop --Gets the population for each ethnicity for each county by year
                                    FROM rc4.Demographic
                                    GROUP BY countyFIPS, demo_year, ethnicity
                                    )
                                NATURAL JOIN(
                                    SELECT countyFIPS, demo_year AS year, SUM(population) AS totalPop --Gets the total population for each county by year
                                    FROM rc4.Demographic
                                    GROUP BY countyFIPS, demo_year
                                    )
                                ) d2
                            ON (d1.countyFIPS = d2.countyFIPS) AND (d2.year = (d1.year + 1)) AND (d1.ethnicity = d2.ethnicity)
                            )
                        JOIN
                            rc4.Ethnicity
                        ON ethnicity = ethnicity.eid
                        %s
                        ORDER BY countyFIPS ASC, startYear ASC, eID ASC --For some reason, trying to order causes it to process forever(table probably too large)
                                """ % (outerWhereClause)

                cursor = connection.cursor()

                data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

                x = []
                y = []

                for row in data:
                        x.append(row[2])
                        y.append(row[5])

                plt.plot(x, y, marker='o')

        plt.xlabel('Year')
        plt.ylabel('Percent Ethnicity Change')
        plt.legend(labels=legend, loc='lower center', ncol=1, fancybox=True, shadow=True)
        title = "\n".join(wrap('Percent change in ethnic population From ' + str(start) + " To " + str(end) + ', from year to year', 40))
        plt.title(title)
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                #labelbottom=False  # labels along the bottom edge are off
        )

        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc

def GraphThree(counties, start, end, threshold, connection):

        plt.clf()
        legend = []

        for county in counties:
                legend.append(str(county))
                outerWhereClause = f"WHERE name = \'" + str(county) + '\''
                #outerWhereClause = f"WHERE name IN ({str(counties).replace('[', '').replace(']','')})"

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
                        string = row[2] + ' ' + str(row[1])
                        dtValue = datetime.datetime.strptime(string, "%B %Y").date()
                        x.append(dtValue)
                        y.append(row[3])

                plt.plot(x, y, marker='o')

        plt.xlabel('Month/Year')
        plt.ylabel('Number of days above Threshold')
        title = 'Number of days with a Heat Index above ' + threshold + '???, by month'
        plt.title(title)
        plt.legend(labels=legend, fancybox=True, shadow=True)
        """ plt.tick_params(
                axis='x',          # changes apply to the x-axis
                labelbottom=False  # labels along the bottom edge are off
        ) """

        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc

def GraphFour(counties, start, end, connection):
        plt.clf()
        legend = []

        for county in counties:
                legend.append(str(county))

                outerWhereClause = f"WHERE name = \'" + str(county) + '\''

                if start != '':
                        outerWhereClause = outerWhereClause + f" AND (year >= {str(start)[0:4]})"

                if end != '':
                        outerWhereClause = outerWhereClause + f" AND (year <= {str(end)[0:4]})"

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
                """ % (outerWhereClause)

                cursor = connection.cursor()

                data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

                x = []
                y = []

                for row in data:
                        x.append(row[2])
                        y.append(row[3])

                plt.plot(x, y, marker='o')


        plt.xlabel('Year')
        plt.ylabel('Correlation Coefficient')
        plt.legend(labels=legend, fancybox=True, shadow=True)
        title = "\n".join(wrap('Correlation between Yearly UV Irradiance and Average Yearly Heat Index From ' + str(start) + " To " + str(end) + ', by year', 60))
        plt.title(title)
        #plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}')) # No decimal places
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                #labelbottom=False  # labels along the bottom edge are off
        )
        buf = BytesIO()
        plt.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc


def GraphFive(stdev, counties, start, end, connection):
        plt.clf()
        legend = []

        for county in counties:
                legend.append(str(county))

                outerWhereClause = f"WHERE heat_value >= lowerBoundSummer AND name = \'" + str(county) + '\''
                #outerWhereClause = f"AND name IN ({str(counties).replace('[', '').replace(']','')})"   
                numstdev = 1

                if stdev != '':
                        numstdev = stdev

                if start != '':
                        outerWhereClause = outerWhereClause + f" AND (year >= {str(start)[0:4]})"
                if end != '':
                        outerWhereClause = outerWhereClause + f" AND (year <= {str(end)[0:4]})"
                

                dbQuery = """
                SELECT rc4.Heat_Index.countyFIPS, name, year, COUNT(*) as numHotDays --Counts the number of days hotter than the lower bound (x SDs away from mean) and orders
                FROM 
                        (SELECT countyFIPS, name, year, (AVG(heat_value) - %s * STDDEV(heat_value)) as lowerBoundSummer --Calculates x Standard Deviations away from the year's summer mean heat value (lower bound only)
                        FROM (  SELECT t.*, rc4.county.name, EXTRACT(YEAR FROM HI_Date) as year --Extracts year for grouping
                                FROM rc4.Heat_Index t, rc4.county
                                WHERE t.countyFIPS = rc4.county.countyFIPS
                                )
                        GROUP BY name, countyFIPS, year
                        ) summerStats
                JOIN
                        rc4.Heat_Index ON rc4.Heat_Index.countyFIPS = summerStats.countyFIPS
                                        AND TO_CHAR(rc4.Heat_Index.HI_Date, 'YYYY') = summerStats.year
                %s
                GROUP BY rc4.Heat_Index.countyFIPS, name, year
                ORDER BY rc4.Heat_Index.countyFIPS ASC, year ASC
                """ % (numstdev, outerWhereClause)

                cursor = connection.cursor()

                data = cursor.execute(dbQuery)  # Cursor.execute returns an iterator that contains the results of the query

                x = []
                y = []

                for row in data:
                        x.append(row[2])
                        y.append(row[3])

                plt.plot(x, y, marker='o')

        plt.xlabel('Year')
        plt.ylabel('Number of days')
        title = "\n".join(wrap('Number of days hotter than ' + str(stdev) + ' standard deviation(s) less than the Summer Mean Heat Index From ' + str(start) + " To " + str(end) + ', by year', 60))
        plt.title(title)
        plt.legend(labels=legend, fancybox=True, shadow=True)
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                #labelbottom=False  # labels along the bottom edge are off
        ) 

        buf = BytesIO()
        plt.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        imgSrc = f"src=data:image/png;base64,{data}"

        return imgSrc