# SteamGames
Trabajo realizado como "Proyecto Individual 1" para Bootcamp Henry - Data PT 08 -  Mayo 2024


Se realizó un proyecto que consiste en realizar un MVP sobre una base de datos correspondiente a juegos: Steam Games.
Los datos son recibidos en formato zip. 

ETL:
Para poder trabajar con los datos se realizó un ETL, realizando todas las transformaciones posibles, para lograr trabajar con datos limpios y legibles.
En el mismo se tuvieron en cuenta lo aprendido durante el curso.
Se analizaron los datos desanidando los datos primero, para lograr poder ver los mismos. 
A partir de ahí, se eliminaron nulos, duplicados, columnas que estaban de más. De esta forma se logró trabajar con datos de forma mas prolija y legible.
Se realizaron ademas, cambios en nombres de columnas para evitar confusiones, y se reemplazo la fecha por el año correspondiente en cada caso, dado que es la información que yo necesito para poder realizar las funciones.
Una vez realizado este proceso, re prosiguió a guardar los mismos en parquet, para poder guardar los datos limpios.
Dado que hay que optimizar la memoria para que pueda correr mejor, ee utilizó formato parquet para que los datos se compriman y ocupen menos memoria.
