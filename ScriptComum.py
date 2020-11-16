from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)       

@app.route('/scriptComum/<string:arquivo>', methods=['POST'])
def ViaCsv(arquivo):
    csv = pd.read_csv('..\\..\\..\\ThinkBitcoin\\CSVTransacoes (executando)\\' + arquivo)

    csv = (np.array(csv)[0:len(csv)-52])
    index = np.array(csv)[len(csv)-51:len(csv)-1]

    xPred = pd.DataFrame({'QUANTIDADE': index[:, 1], 'TIPO': index[:, 2], 'SEGUNDOS': index[:, 3]})
    x = pd.DataFrame({'QUANTIDADE': csv[:, 1], 'TIPO': csv[:, 2], 'SEGUNDOS': csv[:, 3]})
    y = pd.DataFrame({'PRECO': csv[:, 0]})

    reglin = LinearRegression()
    reglin.fit(x,y)

    pred = reglin.predict(xPred)
    predData = pd.DataFrame({'PRECO': pred[:, 0]})

    transJson = [{"ID": i, "PRECO": 0, 'QUANTIDADE': 0, 'TIPO': 0, 'SEGUNDOS': 0 } for i in range(1,51)]

    print(transJson)

    for index, row in predData.iterrows():
        for dev in transJson:
            if dev['ID'] == int(index)+1:
                dev['PRECO'] = row['PRECO']

    for index, row in xPred.iterrows():
        for dev in transJson:
            if dev['ID'] == int(index)+1:
                print('')
                dev['QUANTIDADE'] = row['QUANTIDADE']
                dev['TIPO'] = row['TIPO']
                dev['SEGUNDOS'] = row['SEGUNDOS']

    return jsonify(transJson), 200

if __name__ == '__main__':
    app.run(debug=True) 
