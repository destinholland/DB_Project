

def GraphOne(counties, start, end):

        dbQuery = """
        SELECT name, year, month, Month_Average --Retrieves relevant information (Removes mnum that was used for ordering)
        FROM (
            SELECT rc4.County.name, year, month, Month_Average, mnum --Joins with county to get county names and orders data
            FROM (
                    SELECT countyFIPS, year, month, AVG(heat_value) as Month_Average, mnum --Calculates monthly averages
                    FROM (  SELECT t.*, EXTRACT(YEAR FROM HI_Date) as year, TO_CHAR(HI_Date, 'Month') as month, TO_CHAR(HI_Date, 'mm') as mnum --Extracts year and month
                            FROM rc4.Heat_Index t
                            )
                    GROUP BY countyFIPS, year, month, mnum
                    )
            NATURAL JOIN
                    (rc4.County
                    WHERE name IN %s
        ORDER BY rc4.County.name ASC, year ASC, mnum ASC
        """

        dbQuery = dbQuery + whereClause + orderByClause + ")"

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
        plt.xticks(rotation='vertical', fontsize=3)

        buf = BytesIO()
        plt.savefig(buf, format="png")

        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        imgSrc = f"src=data:image/png;base64,{data}"