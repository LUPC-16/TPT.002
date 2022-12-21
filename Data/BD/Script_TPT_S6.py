import csv, uuid, dataset
from array import array
import sys
import os
import re
import sqlite3
import pandas as pd
import time
import pathlib
import numpy as np
import pandas.io.formats.excel
from openpyxl import load_workbook

def LeerArchivo(Ruta,Ruta2):
    print("Inicia ejecucion Script TPT.S6.1_RECONOCIMIENTO_DE_LA_COBRANZA")
    print("")
    global fiCHERO3
    Path='\\'.join(Ruta.split('\\')[:-1])
    Path2='\\'.join(Ruta2.split('\\')[:-1])
    ejemplo_dir = Path
    ListaTablas=[]
    directorio = pathlib.Path(ejemplo_dir)
    for fichero in directorio.iterdir():
        if "UUIDS" in str(fichero.name) and "$" not in str(fichero) :
            Fichero3 = str(fichero)
            
            dfuid = pd.read_csv(str(Fichero3),dtype=object)
            Fichero3=str(fichero).split('_')
            dfuid. to_sql ( 'DatatableUIDS' , cx, if_exists= 'replace' , index=None)
            df= pd.read_sql_query("SELECT APLICACION,ITEM_NO,MONTO_COMPLEMENTO,GROUP_CONCAT(CFDI_UUID_FACTURA) AS CFDI_UUID_FACTURA ,GROUP_CONCAT(CFDI_UUID_COMPLEMENTO_PAGO) AS CFDI_UUID_COMPLEMENTO_PAGO FROM DatatableUIDS  GROUP BY ITEM_NO,APLICACION;", cx)
            df.to_sql("TABLA_UIDS_CONCAT", cx, if_exists="replace")       
           
            for fichero in directorio.iterdir():
                if "PAGOS" in str(fichero) and "$" not in str(fichero):
                    Fichero2 = str(fichero)
                    Fichero2=str(fichero).split('_')
                    if (Fichero2[1]==Fichero3[1] and Fichero2[2]==Fichero3[2]):

                       print("Subiendo archivos PAGOS y UUIDS: "+Fichero2[1]+"_"+Fichero2[2]+" a la base de datos")
                       print("")
                       print("Procesando .....")
                       print("")

                       df = pd.read_csv(str(fichero),dtype=object)
                       df. to_sql ( 'DatatablePagos' , cx, if_exists= 'replace' , index=None)  
                       df= pd.read_sql_query('SELECT*FROM DatatablePagos WHERE COUNTRY="MX"',cx)
                       df. to_sql ( 'DatatablePagos_MX' , cx, if_exists= 'replace' , index=None)
                       df= pd.read_sql_query('SELECT*FROM DatatablePagos WHERE COUNTRY="MX_NORTE"',cx)
                       df. to_sql ( 'DatatablePagos_MX_NORTE' , cx, if_exists= 'replace' , index=None)

                       print("Data subida con exito")
                       print("")

                       print("-----------------------------------------------------------------------------------------")
            
                       print("INICIA CONCATENACION PAGOS VS UIDS MX_NORTE")
                       print("")
                       print("Procesando .....")
                       print("")
                       
                       df=pd.read_sql_query('SELECT  DatatablePagos_MX_NORTE.ITEM_NO,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX_NORTE.TPI_MONTO,DatatablePagos_MX_NORTE.TPI_IEPS,DatatablePagos_MX_NORTE.TPI_IVA,DatatablePagos_MX_NORTE.TB_MONTO,DatatablePagos_MX_NORTE.TB_IEPS,DatatablePagos_MX_NORTE.TB_IVA,DatatablePagos_MX_NORTE.TPT_MONTO,DatatablePagos_MX_NORTE.TPT_IEPS,DatatablePagos_MX_NORTE.TPT_IVA,DatatablePagos_MX_NORTE.HS_MONTO,DatatablePagos_MX_NORTE.HS_IEPS,DatatablePagos_MX_NORTE.HS_IVA,DatatablePagos_MX_NORTE.GO_MONTO,DatatablePagos_MX_NORTE.GO_IEPS,DatatablePagos_MX_NORTE.GO_IVA,DatatablePagos_MX_NORTE.TERCEROS,DatatablePagos_MX_NORTE.MONTO_PAGO FROM (( DatatablePagos_MX_NORTE INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX_NORTE.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX_NORTE.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TOTALPLAY"',cx)
                       df.to_sql( 'Tabla_MX_NORTE_TOTALPLAY' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_NORTE_TOTALPLAY',cx)
                       df.to_sql( 'Tabla_Diferencia_TOTALPLAY' , cx, if_exists= 'replace' , index=None)

                       df=pd.read_sql_query('SELECT  DatatablePagos_MX_NORTE.ITEM_NO,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX_NORTE.TPI_MONTO,DatatablePagos_MX_NORTE.TPI_IEPS,DatatablePagos_MX_NORTE.TPI_IVA,DatatablePagos_MX_NORTE.TB_MONTO,DatatablePagos_MX_NORTE.TB_IEPS,DatatablePagos_MX_NORTE.TB_IVA,DatatablePagos_MX_NORTE.TPT_MONTO,DatatablePagos_MX_NORTE.TPT_IEPS,DatatablePagos_MX_NORTE.TPT_IVA,DatatablePagos_MX_NORTE.HS_MONTO,DatatablePagos_MX_NORTE.HS_IEPS,DatatablePagos_MX_NORTE.HS_IVA,DatatablePagos_MX_NORTE.GO_MONTO,DatatablePagos_MX_NORTE.GO_IEPS,DatatablePagos_MX_NORTE.GO_IVA,DatatablePagos_MX_NORTE.TERCEROS,DatatablePagos_MX_NORTE.MONTO_PAGO FROM (( DatatablePagos_MX_NORTE INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX_NORTE.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX_NORTE.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TOTALBOX"',cx)
                       df.to_sql( 'Tabla_MX_NORTE_TOTALBOX' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_NORTE_TOTALBOX',cx)
                       df.to_sql( 'Tabla_Diferencia_TOTALBOX' , cx, if_exists= 'replace' , index=None)

                       df=pd.read_sql_query('SELECT  DatatablePagos_MX_NORTE.ITEM_NO,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX_NORTE.TPI_MONTO,DatatablePagos_MX_NORTE.TPI_IEPS,DatatablePagos_MX_NORTE.TPI_IVA,DatatablePagos_MX_NORTE.TB_MONTO,DatatablePagos_MX_NORTE.TB_IEPS,DatatablePagos_MX_NORTE.TB_IVA,DatatablePagos_MX_NORTE.TPT_MONTO,DatatablePagos_MX_NORTE.TPT_IEPS,DatatablePagos_MX_NORTE.TPT_IVA,DatatablePagos_MX_NORTE.HS_MONTO,DatatablePagos_MX_NORTE.HS_IEPS,DatatablePagos_MX_NORTE.HS_IVA,DatatablePagos_MX_NORTE.GO_MONTO,DatatablePagos_MX_NORTE.GO_IEPS,DatatablePagos_MX_NORTE.GO_IVA,DatatablePagos_MX_NORTE.TERCEROS,DatatablePagos_MX_NORTE.MONTO_PAGO FROM (( DatatablePagos_MX_NORTE INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX_NORTE.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX_NORTE.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TP_HS"',cx)
                       df.to_sql( 'Tabla_MX_NORTE_TP_HS' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_NORTE_TP_HS',cx)
                       df.to_sql( 'Tabla_Diferencia_TP_HS' , cx, if_exists= 'replace' , index=None)

                       df=pd.read_sql_query('SELECT  DatatablePagos_MX_NORTE.ITEM_NO,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX_NORTE.TPI_MONTO,DatatablePagos_MX_NORTE.TPI_IEPS,DatatablePagos_MX_NORTE.TPI_IVA,DatatablePagos_MX_NORTE.TB_MONTO,DatatablePagos_MX_NORTE.TB_IEPS,DatatablePagos_MX_NORTE.TB_IVA,DatatablePagos_MX_NORTE.TPT_MONTO,DatatablePagos_MX_NORTE.TPT_IEPS,DatatablePagos_MX_NORTE.TPT_IVA,DatatablePagos_MX_NORTE.HS_MONTO,DatatablePagos_MX_NORTE.HS_IEPS,DatatablePagos_MX_NORTE.HS_IVA,DatatablePagos_MX_NORTE.GO_MONTO,DatatablePagos_MX_NORTE.GO_IEPS,DatatablePagos_MX_NORTE.GO_IVA,DatatablePagos_MX_NORTE.TERCEROS,DatatablePagos_MX_NORTE.MONTO_PAGO FROM (( DatatablePagos_MX_NORTE INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX_NORTE.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX_NORTE.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TP_GO"',cx)
                       df.to_sql( 'Tabla_MX_NORTE_TP_GO' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_NORTE_TP_GO',cx)
                       df.to_sql( 'Tabla_Diferencia_TP_GO' , cx, if_exists= 'replace' , index=None)

                       print("Concatenacion terminada con exito")
                       print("")
                       print("-----------------------------------------------------------------------------------------")

                       print("INICIA CONCATENACION PAGOS VS UIDS MX")
                       print("")
                       print("Procesando .....")
                       print("")
                       df=pd.read_sql_query('SELECT DatatablePagos_MX.ITEM_NO,TABLA_UIDS_CONCAT.APLICACION,  DatatablePagos_MX.COUNTRY ,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX.TPI_MONTO,DatatablePagos_MX.TPI_IEPS,DatatablePagos_MX.TPI_IVA,DatatablePagos_MX.TB_MONTO,DatatablePagos_MX.TB_IEPS,DatatablePagos_MX.TB_IVA,DatatablePagos_MX.TPT_MONTO,DatatablePagos_MX.TPT_IEPS,DatatablePagos_MX.TPT_IVA,DatatablePagos_MX.HS_MONTO,DatatablePagos_MX.HS_IEPS,DatatablePagos_MX.HS_IVA,DatatablePagos_MX.GO_MONTO,DatatablePagos_MX.GO_IEPS,DatatablePagos_MX.GO_IVA,DatatablePagos_MX.TERCEROS,DatatablePagos_MX.MONTO_PAGO FROM (( DatatablePagos_MX INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TOTALPLAY"',cx)
                       df.to_sql( 'Tabla_MX_TOTALPLAY' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_TOTALPLAY',cx)
                       df.to_sql( 'Tabla_Diferencia_TOTALPLAY_MX' , cx, if_exists= 'replace' , index=None)


                       df=pd.read_sql_query('SELECT DatatablePagos_MX.ITEM_NO,TABLA_UIDS_CONCAT.APLICACION,  DatatablePagos_MX.COUNTRY ,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX.TPI_MONTO,DatatablePagos_MX.TPI_IEPS,DatatablePagos_MX.TPI_IVA,DatatablePagos_MX.TB_MONTO,DatatablePagos_MX.TB_IEPS,DatatablePagos_MX.TB_IVA,DatatablePagos_MX.TPT_MONTO,DatatablePagos_MX.TPT_IEPS,DatatablePagos_MX.TPT_IVA,DatatablePagos_MX.HS_MONTO,DatatablePagos_MX.HS_IEPS,DatatablePagos_MX.HS_IVA,DatatablePagos_MX.GO_MONTO,DatatablePagos_MX.GO_IEPS,DatatablePagos_MX.GO_IVA,DatatablePagos_MX.TERCEROS,DatatablePagos_MX.MONTO_PAGO FROM (( DatatablePagos_MX INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TOTALBOX"',cx)
                       df.to_sql( 'Tabla_MX_TOTALBOX' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_TOTALBOX',cx)
                       df.to_sql( 'Tabla_Diferencia_TOTALBOX_MX' , cx, if_exists= 'replace' , index=None)

                       df=pd.read_sql_query('SELECT DatatablePagos_MX.ITEM_NO,TABLA_UIDS_CONCAT.APLICACION,  DatatablePagos_MX.COUNTRY ,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX.TPI_MONTO,DatatablePagos_MX.TPI_IEPS,DatatablePagos_MX.TPI_IVA,DatatablePagos_MX.TB_MONTO,DatatablePagos_MX.TB_IEPS,DatatablePagos_MX.TB_IVA,DatatablePagos_MX.TPT_MONTO,DatatablePagos_MX.TPT_IEPS,DatatablePagos_MX.TPT_IVA,DatatablePagos_MX.HS_MONTO,DatatablePagos_MX.HS_IEPS,DatatablePagos_MX.HS_IVA,DatatablePagos_MX.GO_MONTO,DatatablePagos_MX.GO_IEPS,DatatablePagos_MX.GO_IVA,DatatablePagos_MX.TERCEROS,DatatablePagos_MX.MONTO_PAGO FROM (( DatatablePagos_MX INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TP_HS"',cx)
                       df.to_sql( 'Tabla_MX_TP_HS' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_TP_HS',cx)
                       df.to_sql( 'Tabla_Diferencia_TP_HS_MX' , cx, if_exists= 'replace' , index=None)

                       df=pd.read_sql_query('SELECT DatatablePagos_MX.ITEM_NO,TABLA_UIDS_CONCAT.APLICACION,  DatatablePagos_MX.COUNTRY ,TABLA_UIDS_CONCAT.CFDI_UUID_FACTURA,TABLA_UIDS_CONCAT.CFDI_UUID_COMPLEMENTO_PAGO ,TABLA_UIDS_CONCAT.MONTO_COMPLEMENTO,DatatablePagos_MX.TPI_MONTO,DatatablePagos_MX.TPI_IEPS,DatatablePagos_MX.TPI_IVA,DatatablePagos_MX.TB_MONTO,DatatablePagos_MX.TB_IEPS,DatatablePagos_MX.TB_IVA,DatatablePagos_MX.TPT_MONTO,DatatablePagos_MX.TPT_IEPS,DatatablePagos_MX.TPT_IVA,DatatablePagos_MX.HS_MONTO,DatatablePagos_MX.HS_IEPS,DatatablePagos_MX.HS_IVA,DatatablePagos_MX.GO_MONTO,DatatablePagos_MX.GO_IEPS,DatatablePagos_MX.GO_IVA,DatatablePagos_MX.TERCEROS,DatatablePagos_MX.MONTO_PAGO FROM (( DatatablePagos_MX INNER JOIN TABLA_UIDS_CONCAT as p1 ON  DatatablePagos_MX.ITEM_NO = p1.ITEM_NO) INNER JOIN TABLA_UIDS_CONCAT ON  DatatablePagos_MX.ITEM_NO = TABLA_UIDS_CONCAT.ITEM_NO)WHERE TABLA_UIDS_CONCAT.APLICACION="TP_GO"',cx)
                       df.to_sql( 'Tabla_MX_TP_GO' , cx, if_exists= 'replace' , index=None)
                       df=pd.read_sql_query('SELECT  ITEM_NO,printf("%.2f",TPI_MONTO+TPI_IEPS+TPI_IVA+TB_MONTO+TB_IEPS+TB_IVA+TPT_MONTO+TPT_IEPS+TPT_IVA+HS_MONTO+HS_IEPS+HS_IVA+GO_MONTO+GO_IEPS+GO_IVA+TERCEROS)- MONTO_PAGO AS RESTA FROM Tabla_MX_TP_GO',cx)
                       df.to_sql( 'Tabla_Diferencia_TP_GO_MX' , cx, if_exists= 'replace' , index=None)

                       print("Concatenacion terminada con exito"+"\n")
                       
                       print("-----------------------------------------------------------------------------------------")
                       print("Generando TABLA_FINAL_MX")
                       print("")
                       print("Procesando .....")
                       print("")
                       cu.execute('INSERT INTO TABLAFINAL(NUM,EMPRESA,ACCOUNT_NO,COMPANIA,NOMBRE,RFC,ITEM_NO,MONTO_PAGO,FECHA_LIQUIDADO,TPI_MONTO,TPI_IEPS,TPI_IVA,TB_MONTO,TB_IEPS,TB_IVA,TPT_MONTO,TPT_IEPS,TPT_IVA,HS_MONTO,HS_IEPS,HS_IVA,GO_MONTO,GO_IEPS,GO_IVA,TERCEROS,PENDIENTE,CANAL,CUENTA_BANCO,MONEDA,COUNTRY,UBICACION,CódigoPostal)SELECT NUM,EMPRESA,ACCOUNT_NO,COMPANIA,NOMBRE,RFC,ITEM_NO,MONTO_PAGO,FECHA_LIQUIDADO,TPI_MONTO,TPI_IEPS,TPI_IVA,TB_MONTO,TB_IEPS,TB_IVA,TPT_MONTO,TPT_IEPS,TPT_IVA,HS_MONTO,HS_IEPS,HS_IVA,GO_MONTO,GO_IEPS,GO_IVA,TERCEROS,PENDIENTE,CANAL,CUENTA_BANCO,MONEDA,COUNTRY,UBICACION,CódigoPostal FROM DatatablePagos_MX')
                       cx.commit()
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_TOTALPLAY WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA_TB = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO_TB=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO_TB=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_TOTALBOX WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA_TPGO = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO_TPGO=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO_TPGO=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_TP_GO WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA_HS = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO_HS=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO_HS=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_TP_HS WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO="UUID NO ENCONTRADO" ,MONTO_APLICADO="0.O" WHERE CFDI_UUID_FACTURA is NULL')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA_TB = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO_TB="UUID NO ENCONTRADO" ,MONTO_APLICADO_TB="0.O" WHERE CFDI_UUID_FACTURA_TB is NULL')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA_HS = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO_HS="UUID NO ENCONTRADO" ,MONTO_APLICADO_HS="0.O" WHERE CFDI_UUID_FACTURA_HS is NULL')
                       cu.execute('UPDATE TABLAFINAL SET CFDI_UUID_FACTURA_TPGO = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO_TPGO="UUID NO ENCONTRADO" ,MONTO_APLICADO_TPGO="0.O" WHERE CFDI_UUID_FACTURA_TPGO is NULL')
                       cu.execute('UPDATE TABLAFINAL SET DIFERENCIA=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TOTALPLAY_MX ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cu.execute('UPDATE TABLAFINAL SET DIFERENCIA_TB=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TOTALBOX_MX ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cu.execute('UPDATE TABLAFINAL SET DIFERENCIA_HS=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TP_HS_MX ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cu.execute('UPDATE TABLAFINAL SET DIFERENCIA_TPGO=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TP_GO_MX  ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       print("TABLA_FINAL_MX generada con exito"+"\n")

                       print("-----------------------------------------------------------------------------------------")

                       print("Generando TABLA_FINAL_MX_NORTE")
                       print("")
                       print("Procesando .....")
                       print("")
                       cu.execute('INSERT INTO TABLAFINAL_MX_NORTE(NUM,EMPRESA,ACCOUNT_NO,COMPANIA,NOMBRE,RFC,ITEM_NO,MONTO_PAGO,FECHA_LIQUIDADO,TPI_MONTO,TPI_IEPS,TPI_IVA,TB_MONTO,TB_IEPS,TB_IVA,TPT_MONTO,TPT_IEPS,TPT_IVA,HS_MONTO,HS_IEPS,HS_IVA,GO_MONTO,GO_IEPS,GO_IVA,TERCEROS,PENDIENTE,CANAL,CUENTA_BANCO,MONEDA,COUNTRY,UBICACION,CódigoPostal) SELECT NUM,EMPRESA,ACCOUNT_NO,COMPANIA,NOMBRE,RFC,ITEM_NO,MONTO_PAGO,FECHA_LIQUIDADO,TPI_MONTO,TPI_IEPS,TPI_IVA,TB_MONTO,TB_IEPS,TB_IVA,TPT_MONTO,TPT_IEPS,TPT_IVA,HS_MONTO,HS_IEPS,HS_IVA,GO_MONTO,GO_IEPS,GO_IVA,TERCEROS,PENDIENTE,CANAL,CUENTA_BANCO,MONEDA,COUNTRY,UBICACION,CódigoPostal FROM DatatablePagos_MX_NORTE')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_NORTE_TOTALPLAY WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA_TB = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO_TB=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO_TB=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_NORTE_TOTALBOX WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA_TPGO = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO_TPGO=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO_TPGO=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_NORTE_TP_GO WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA_HS = CFDI_UUID_FACTURA1 ,CFDI_UUID_COMPLEMENTO_PAGO_HS=CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_APLICADO_HS=MONTO_PAGO1 FROM(SELECT ITEM_NO AS ITEM_NOP1,CFDI_UUID_FACTURA AS CFDI_UUID_FACTURA1,CFDI_UUID_COMPLEMENTO_PAGO AS CFDI_UUID_COMPLEMENTO_PAGO1 ,MONTO_COMPLEMENTO AS MONTO_PAGO1 FROM Tabla_MX_NORTE_TP_HS WHERE ITEM_NO=ITEM_NOP1 ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1 ')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO="UUID NO ENCONTRADO" ,MONTO_APLICADO="0.O" WHERE CFDI_UUID_FACTURA is NULL')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA_TB = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO_TB="UUID NO ENCONTRADO" ,MONTO_APLICADO_TB="0.O" WHERE CFDI_UUID_FACTURA_TB is NULL')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA_HS = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO_HS="UUID NO ENCONTRADO" ,MONTO_APLICADO_HS="0.O" WHERE CFDI_UUID_FACTURA_HS is NULL')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET CFDI_UUID_FACTURA_TPGO = "UUID NO ENCONTRADO" ,CFDI_UUID_COMPLEMENTO_PAGO_TPGO="UUID NO ENCONTRADO" ,MONTO_APLICADO_TPGO="0.O" WHERE CFDI_UUID_FACTURA_TPGO is NULL')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET DIFERENCIA=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TOTALPLAY ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET DIFERENCIA_TB=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TOTALBOX ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET DIFERENCIA_HS=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TP_HS ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cu.execute('UPDATE TABLAFINAL_MX_NORTE SET DIFERENCIA_TPGO=RESTA FROM (SELECT ITEM_NO AS ITEM_NOP1,RESTA FROM Tabla_Diferencia_TP_GO ORDER BY ITEM_NO)WHERE ITEM_NO=ITEM_NOP1')
                       cx.commit()

                       print("TABLA_FINAL_MX_NORTE generada con exito"+"\n")
                       
                       print("-----------------------------------------------------------------------------------------")

                       print("Inicia divicion de archivo PAGOS a 4mgb")
                       print("")
                       print("Procesando archivos .....")
                       print("")
                       df_MX=pd.read_sql_query('SELECT*FROM TABLAFINAL',cx)
                       df_NORTE=pd.read_sql_query('SELECT*FROM TABLAFINAL_MX_NORTE',cx)
                     
                       cu.execute('DELETE FROM TABLAFINAL')
                       cu.execute('DELETE FROM TABLAFINAL_MX_NORTE')
                       cx.commit()
                       x = len (df_MX)
                       y = len (df_NORTE)
                       NORJ=5000
                       NORH=1
                       MXJ=5000
                       MXH=1
                       i=0
                       Complemento=str(Fichero2[2]).split('.')
                       os.mkdir(Path2+"\\PAGOS_"+Fichero2[1]+"_"+Complemento[0])
                       while y > 0 or x > 0:
                         i=i+1
                         
                         writer = pd.ExcelWriter(Path2+"\\PAGOS_"+Fichero2[1]+"_"+Complemento[0]+"\\PAGOS_"+Fichero2[1]+"_"+Complemento[0]+"_"+str(i)+'.xlsx',engine='xlsxwriter')
                         if y>0:
                             df1=df_NORTE.loc[NORH:NORJ]
                             
                             NORH=NORJ
                             NORJ=NORJ+5000
                             
                             df1.to_excel(writer,sheet_name= 'MX_NORTE', index=False)
                            
                             df1=[]
                             y=y-5000
                         if x > 0 :
                             df1=df_MX.loc[MXH:MXJ]
                             
                             MXH=MXJ
                             MXJ=MXJ+5000
                             df1.to_excel(writer,sheet_name= 'MX', index=False)
                             writer.save()
                             df1=[]
                             x=x-5000
     
                       print("Divicion realizada con exito"+"\n")
                            
                          
                         

                  








    print("Script ejecutado con exito")
    time.sleep(3)
    f=open(Path+'\\salida.abc','w')
    f.close()
    

if __name__ == '__main__':

    Tstart = time.time() 
    cx = sqlite3.connect('./avpig_sde.sqlite3') 
    cu = cx.cursor()
    cu.execute('CREATE TABLE IF NOT EXISTS DatatablePagos ([NUM]varchar, [EMPRESA]varchar , [ACCOUNT_NO]varchar, [COMPANIA]varchar, [NOMBRE]varchar, [RFC]varchar,[ITEM_NO]varchar, [MONTO_PAGO]float , [FECHA_LIQUIDADO]varchar, [TPI_MONTO]float , [TPI_IEPS]float, [TPI_IVA]float, [TB_MONTO]float, [TB_IEPS]float,[TB_IVA]float, [TPT_MONTO]float  ,[TPT_IEPS]float , [TPT_IVA]float, [HS_MONTO]float, [HS_IEPS]float, [HS_IVA]float, [GO_MONTO]float, [GO_IEPS]float, [GO_IVA]float,[TERCEROS]float, [PENDIENTE]varchar, [CANAL]varchar, [CUENTA_BANCO]varchar, [MONEDA]varchar, [COUNTRY]varchar, [UBICACION]varchar,[CódigoPostal]varchar)') #Create table
    cu.execute('CREATE TABLE IF NOT EXISTS DatatableUIDS ([EMPRESA]varchar, [ACCOUNT_NO]varchar,[ITEM_NO]varchar,[MONTO_PAGO]float,[MONTO_COMPLEMENTO]Float,[CFDI_UUID_COMPLEMENTO_PAGO]varchar,[APLICACION]varchar,[BILL_NO]varchar,[MONTO_APLICADO]float,[CFDI_UUID_FACTURA]varchar,[FECHA_FACTURA]varchar)') #Create table
    cu.execute('CREATE TABLE TABLAFINAL ([NUM]varchar, [EMPRESA]varchar , [ACCOUNT_NO]varchar, [COMPANIA]varchar, [NOMBRE]varchar, [RFC]varchar,[ITEM_NO]varchar, [MONTO_PAGO]float , [FECHA_LIQUIDADO]varchar, [TPI_MONTO]float , [TPI_IEPS]float, [TPI_IVA]float, [TB_MONTO]float, [TB_IEPS]float,[TB_IVA]float, [TPT_MONTO]float  ,[TPT_IEPS]float , [TPT_IVA]float, [HS_MONTO]float, [HS_IEPS]float, [HS_IVA]float, [GO_MONTO]float, [GO_IEPS]float, [GO_IVA]float,[TERCEROS]float, [PENDIENTE]varchar, [CANAL]varchar, [CUENTA_BANCO]varchar, [MONEDA]varchar, [COUNTRY]varchar, [UBICACION]varchar,[CódigoPostal]varchar,[CFDI_UUID_FACTURA] varchar,[CFDI_UUID_COMPLEMENTO_PAGO] varchar,	[MONTO_APLICADO] varchar,[DIFERENCIA] float ,[CFDI_UUID_FACTURA_TB] varchar ,[CFDI_UUID_COMPLEMENTO_PAGO_TB] varchar ,	[MONTO_APLICADO_TB] varchar 	,[DIFERENCIA_TB] float ,[CFDI_UUID_FACTURA_TPGO] varchar ,[CFDI_UUID_COMPLEMENTO_PAGO_TPGO] varchar ,[MONTO_APLICADO_TPGO] varchar ,[DIFERENCIA_TPGO] float ,[CFDI_UUID_FACTURA_HS]varchar,[CFDI_UUID_COMPLEMENTO_PAGO_HS]varchar,[MONTO_APLICADO_HS]varchar,[DIFERENCIA_HS]float)')
    cu.execute('CREATE TABLE TABLAFINAL_MX_NORTE ([NUM]varchar, [EMPRESA]varchar , [ACCOUNT_NO]varchar, [COMPANIA]varchar, [NOMBRE]varchar, [RFC]varchar,[ITEM_NO]varchar, [MONTO_PAGO]float , [FECHA_LIQUIDADO]varchar, [TPI_MONTO]float , [TPI_IEPS]float, [TPI_IVA]float, [TB_MONTO]float, [TB_IEPS]float,[TB_IVA]float, [TPT_MONTO]float  ,[TPT_IEPS]float , [TPT_IVA]float, [HS_MONTO]float, [HS_IEPS]float, [HS_IVA]float, [GO_MONTO]float, [GO_IEPS]float, [GO_IVA]float,[TERCEROS]float, [PENDIENTE]varchar, [CANAL]varchar, [CUENTA_BANCO]varchar, [MONEDA]varchar, [COUNTRY]varchar, [UBICACION]varchar,[CódigoPostal]varchar,[CFDI_UUID_FACTURA] varchar,[CFDI_UUID_COMPLEMENTO_PAGO] varchar,	[MONTO_APLICADO] varchar,[DIFERENCIA] float ,[CFDI_UUID_FACTURA_TB] varchar ,[CFDI_UUID_COMPLEMENTO_PAGO_TB] varchar ,	[MONTO_APLICADO_TB] varchar 	,[DIFERENCIA_TB] float ,[CFDI_UUID_FACTURA_TPGO] varchar ,[CFDI_UUID_COMPLEMENTO_PAGO_TPGO] varchar ,[MONTO_APLICADO_TPGO] varchar ,[DIFERENCIA_TPGO] float ,[CFDI_UUID_FACTURA_HS]varchar,[CFDI_UUID_COMPLEMENTO_PAGO_HS]varchar,[MONTO_APLICADO_HS]varchar,[DIFERENCIA_HS]float)') 
    argumentList = sys.argv
    #argumentList = ["C:\\Users\\Beecker\\Documents\\UiPath\\TPT.002\\Data\\BD\\Script_TPT_S6.py", "C:\\Users\\Beecker\\Documents\\UiPath\\TPT.002\\Data\\Input\\CSV\\", "C:\\Users\\Beecker\\Documents\\UiPath\\TPT.002\\Temporal\\PAGOS_PARTICION\\"]
    #argumentList =["C:\Users\Beecker\Documents\UiPath\TPT.002\Data\BD\Script_TPT_S6.py"]
    argumentList = sys.argv
    if len(argumentList) == 3:
        LeerArchivo(argumentList[1],argumentList[2])
       
    else:
         print('No se cumple con el número de argumentos (2)')
         
    Tdone = time.time()
    elapsed = Tdone - Tstart
    print('Tiempo de ejecución: '+str(elapsed))