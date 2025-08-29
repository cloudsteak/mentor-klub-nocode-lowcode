# AWS Sagemaker Canvas

Az AWS Sagemaker Canvas egy vizuális eszköz, amely lehetővé teszi a felhasználók számára, hogy gépi tanulási modelleket építsenek és tanítsanak anélkül, hogy kódolniuk kellene. A Canvas segítségével könnyedén importálhatók adatok, előkészíthetők és modellek hozhatók létre.

## Példa

Egy üzletlánc több városban működik, és az eladásokat szeretnék előre jelezni. Az adatok tartalmazzák a hónapot, a forgalmat és a bolt nevét. Vannak visszamenőleges adatok is, amelyek segítenek a modellek tanításában. Miért hasznos ez egy cégnek? Azért, mert a pontos előrejelzések segíthetnek a készletezés optimalizálásában, a marketingkampányok hatékonyságának növelésében és a bevételek maximalizálásában.
Fontos, hogy a Canvas felülete NoCode, de a végeredmén nem egy grafikus felületen jelenik meg, hanem egy API-n keresztül érhető el. Miért? Mert így a fejlesztők és az adatelemzők könnyen integrálhatják a modelleket más alkalmazásokba és folyamatokba, anélkül, hogy mélyebb technikai ismeretekre lenne szükségük. 
Ebből is látszik, hogy a Canvas az adatelemzők és Data Scientist-ek számára egy NoCode megoldás és nem egy E2E NoCode megoldás.

## Fájlok

- **Bolti_eladasok.csv**: Példa adathalmaz, amelyet a modellek tanításához használhatunk.
- **Deployment_teszt.csv**: Tesztadatok, amelyeket a modellek kiértékelésére használhatunk.
- **README.md**: A mappa tartalmának leírása és használati útmutató.

## Szolgáltatás létrehozás és konfigurálás

1. Első lépésként hozz létre egy SageMaker domaint. ("Create a SageMaker domain")
  - Set up for single user (Quick setup)
  - App configurations → Domains → a domainod → Canvas settings → kapcsold be: Enable direct deployment of Canvas models.
  - App configurations → Domains → a domainod → Canvas settings → kapcsold be: Enable local file upload.
  - User Profiles → Launch → Canvas

2. Dataset-ek (adathalmazok) létrehozása és feltöltése
  - Ha CSV-ből szeretnéd, akkor használd a Bolti_eladasok.csv fájlt. Töltsd fel a Datasets részben.

3. Modell létrehozása
  - My models
  - Create new model → Predictive analysis
  - Select Dataset → Bolti_eladasok
  - Select a column to predict → Forgalom
  - Configure model:
    - Choose the column that uniquely identifies the items in your dataset.: Bolt
    - Choose the column that contains the time stamps.: Honap
    - Specify the number of months you want to forecast into the future.: 6
    - You can use a holiday schedule to improve your prediction accuracy.
  - Quick build (14-20 perc)
  - Deploy model (5-10 perc)



## Fontos

1. Kapcsold be a közvetlen deployt Canvasból: App configurations → Domains → a domainod → Canvas settings → kapcsold be: Enable direct deployment of Canvas models.
2. Engedélyezd a helyi fájlok feltöltését is. App configurations → Domains → a domainod → Canvas settings → kapcsold be: Enable local file upload.
3. Deployment-nél, ha ezt az üzenetet kapod:
```
Your AWS account's usage for the 'ml.m5.4xlarge' transform instance has reached its limit, and you're requesting 1 additional instance. Contact your administrator to increase the quota for your account. If you're an administrator or an individual user, use the AWS Service Quotas console to request an increase for the 'Maximum number of instances' quota.
```
    Akkor azt javaslom válassz másik instance-t, pl. `ml.m5.large` vagy `ml.m5.xlarge`.

3. A p10 / p50 / p90: előrejelzési intervallum percentilisek

    - **p10**: pesszimistább, alsó 10% eset
    - **p50**: medián (a legvalószínűbb érték)
    - **p90**: optimistább, felső 10% eset

## Deployment tesztelése

CloudShell-ben teszteld. 

1. Hozd létre a szükséges környezeti változókat.


```bash
export AWS_DEFAULT_REGION=eu-central-1
export ENDPOINT_NAME="A TE ENDPOINT-OD NEVE. Pl.: bolti-bevetelek"
```

2. Hozd létre a csv fájlt

```bash
echo "Honap,Forgalom,Bolt" > Deployment_teszt.csv
echo "2025-08,,Eger" >> Deployment_teszt.csv
```

3. Futtasd a következő parancsot:

```bash
aws sagemaker-runtime invoke-endpoint \
  --region $AWS_DEFAULT_REGION \
  --endpoint-name $ENDPOINT_NAME \
  --content-type text/csv \
  --accept application/json \
  --body fileb://Deployment_teszt.csv   \
  elorejelzes.csv
```

4. Ellenőrizd az eredményeket az `elorejelzes.csv` fájlban.

```bash
cat elorejelzes.csv
```

Azt látod, hogy a modell előrejelzései megjelennek a fájlban, annak megfelelően, hogy milyen bemeneti adatokat adtál meg. A Forgalom memzőben mutatott érték a modell előrejelzése a forgalomra vonatkozóan. Előfordul, hogy a modell 1000-es nagyságrendben adja vissza az értékeket. Ez azt jelenti, hogy ha azt látod, hogy az előrejelzett forgalom: 4381.987158840129, akkor az azt jelenti, hogy a modell szerint a forgalom körülbelül 4 381 987 Ft lesz, mivel meg kell szoroznod a kapott értéket 1000-el.
