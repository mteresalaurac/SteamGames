from fastapi import FastAPI
app = FastAPI()


import pandas as pd

games=pd.read_csv("Archivos_Comprimidos/games.csv",encoding="latin-1")
reviews= pd.read_parquet("Archivos_Comprimidos/reviews_final.parquet")
items=pd.read_parquet("Archivos_Comprimidos/items.parquet")

#DataFrame joineado para funciones 1) y 2). Voy a unir games con items
items['item_id'] = items['item_id'].astype(float) #Necesito igualar el tipo de dato para poder joinear las tablas 
df= pd.merge(items, games, on='item_id', how='inner')

@app.get("/")
async def ruta_prueba():
    return "BOCA"

#Primera Funcion
@app.get("/PlayTimeGenre")
async def PlayTimeGenre( genero : str ):
    items['item_id'] = items['item_id'].astype(float) #Necesito igualar el tipo de dato para poder joinear las tablas 
    df= pd.merge(items, games, on='item_id', how='inner')
    df.tail(3)   #df que voy a utlizar en la funcion
    genero=genero.lower() #lo paso a minusculas por si esta escrito con mayusculas
    # 1) Paso toda al columna de generos a minuscula
    df['genres'] = df['genres'].str.lower()
    
    # 2) Filtro los valores que contienen el genero que me interesa
    genero="stra" # a modo prueba
    df_filtrado = df[df.filter(like='genres').apply(lambda x: x.str.contains(genero)).any(axis=1)] 
    
    #3) Agrupo los valores por año.
    df_ordenado=df_filtrado[["date","horas"]].groupby(["horas"]).sum().sort_values(by='horas',ascending=False)
    
    #4) Reseteo con indices numericos
    df_ordenado.reset_index(inplace=True) #Agrego el indice para ver las posiciones
    
    #5) Imprimo resultado de funcion
    print(f"Cantidad de horas jugadas en dicho año: {int(df_ordenado.horas.iloc[0])}")
    return f"Cantidad de horas jugadas en dicho año: {int(df_ordenado.horas.iloc[0])}"


#Segunda Funcion
@app.get("/UserForGenre")
async def UserForGenre( genero : str ):
    # 1) Paso toda la columna de generos a minuscula y el parametro tambien
    df['genres'] = df['genres'].str.lower()
    genero=genero.lower()
    
    # 2) Filtro los valores que contienen el genero que me interesa
    #genero="action"
    df_filtrado = df[df.filter(like='genres').apply(lambda x: x.str.contains(genero)).any(axis=1)]
    
    #3) Creo un nuevo df para ver la cant de horas por jugador/userid
    df_ordenado=df_filtrado[["user_id","horas"]].groupby(["horas"]).sum().sort_values(by='horas',ascending=False)
    
    # 4)Como ordene de Mayor a Menor, obtengo el primer valor de user_id que corresponde al que mas horas jugo
    userid_maxhoras=df_ordenado["user_id"].iloc[0]
    print(f"Usuario con mas horas jugadas para género {genero.upper()}: {userid_maxhoras}")
    
    # 5)Renombro la columna que contiene el anio, para evitar confusiones
    df_filtrado.rename(columns={'date': 'year'}, inplace=True)
    
    # 6)Ya conozco el user id, creo una mascara para quedarme solamente con los datos del user id max horas
    df_filtrado = df_filtrado[df_filtrado["user_id"]==userid_maxhoras]
    
    #5) Agrupo las horas por anio
    horas_por_anio = df_filtrado.groupby('year')['horas'].sum()
    
    #6) Creo un dataframe con los valores de la serie que cree
    df_horas_por_anio = pd.DataFrame({'Año': horas_por_anio.index, 'Horas': horas_por_anio.values})
    
    #7) Recorro el diccionario para 
    for indice, fila in df_horas_por_anio.iterrows():
        año = int(fila['Año'])
        horas_jugadas = int(fila['Horas'])
        print(f"El Año: {año} jugó {horas_jugadas} horas ")
        
    return (f"Usuario con mas horas jugadas para género {genero.upper()}: {userid_maxhoras}")

UserForGenre("Action")
