from flask import Flask, render_template, request
from decimal import Decimal, ROUND_HALF_UP

app = Flask(__name__)

def calculExportationTIR(annee, exportation_TIR_N1, DE_N1, taux_evolution):
    if annee == 2022:
        return exportation_TIR_N1
    else:
        DE_N = (1 + taux_evolution / 100) * DE_N1
        exportation_TIR_N = exportation_TIR_N1 + 4.974 * (DE_N - DE_N1)
        return calculExportationTIR(annee - 1, exportation_TIR_N, DE_N, taux_evolution)

def calculImportationTIR(annee, importation_TIR_N1, DI_N1, taux_evolution):
    if annee == 2022:
        return importation_TIR_N1
    elif annee < 2022:
        return 0
    else:
        DI_N = DI_N1 * (1 + taux_evolution / 100)
        importation_TIR_N = importation_TIR_N1 + 0.4903 * (DI_N - DI_N1)
        return calculImportationTIR(annee - 1, importation_TIR_N, DI_N, taux_evolution)

@app.route('/', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        annee = int(request.form['annee'])
        taux_evolutionES = float(request.form['taux_evolutionES'])
        taux_evolutionMA = float(request.form['taux_evolutionES'])
        choix = request.form['choix']

        exportation_TIR_2022 = 4281126.7
        DE_2022 = 231161.3
        importation_TIR_2022 = 899817.8
        DI_2022 = 1395720.8

        if choix == 'ES':
            exportation_TIR = calculExportationTIR(annee, exportation_TIR_2022, DE_2022, taux_evolutionES)
            autorisations_ES = Decimal(exportation_TIR * 0.0318 - 36811).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
            importation_TIR = None
            autorisations_MA = None
        elif choix == 'MA':
            exportation_TIR = None
            autorisations_ES = None
            importation_TIR = calculImportationTIR(annee, importation_TIR_2022, DI_2022, taux_evolutionMA)
            autorisations_MA = Decimal(importation_TIR * 0.0253 - 8609.6).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
        else:
            exportation_TIR = None
            autorisations_ES = None
            importation_TIR = None
            autorisations_MA = None

        return render_template('result.html', annee=annee, exportation_TIR=exportation_TIR,
                               autorisations_ES=autorisations_ES, importation_TIR=importation_TIR,
                               autorisations_MA=autorisations_MA)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
