from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct Country 
                    from go_sales.go_retailers gr 
                    """

        cursor.execute(query, )

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getResidenti(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from go_sales.go_retailers gr
                    where Country = %s """

        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProdottiComuni(r1, r2, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT count(distinct Product_number) as conta
                    FROM go_sales.go_daily_sales gds, go_sales.go_retailers gr
                    where gds.Retailer_code = gr.Retailer_code
                    and YEAR(gds.`Date`) = %s
                    AND gds.Retailer_code = %s
                    and gds.Product_number in (SELECT gds.Product_number 
                    FROM go_sales.go_daily_sales gds
                    where YEAR(gds.`Date`) = %s
                    AND gds.Retailer_code = %s)
                    """

        cursor.execute(query, (anno,r1,anno,r2))

        for row in cursor:
            result.append(row["conta"])

        cursor.close()
        conn.close()
        return result


