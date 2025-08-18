# AWS Sagemaker Canvas

Az AWS Sagemaker Canvas egy vizuális eszköz, amely lehetővé teszi a felhasználók számára, hogy gépi tanulási modelleket építsenek és tanítsanak anélkül, hogy kódolniuk kellene. A Canvas segítségével könnyedén importálhatók adatok, előkészíthetők és modellek hozhatók létre.

## Fájlok

- **Bolti_eladasok.csv**: Példa adathalmaz, amelyet a modellek tanításához használhatunk.
- **Deployment_teszt.csv**: Tesztadatok, amelyeket a modellek kiértékelésére használhatunk.
- **README.md**: A mappa tartalmának leírása és használati útmutató.

## Fontos

Kapcsold be a közvetlen deployt Canvasból: Admin configurations → Domains → a domainod → Canvas settings → kapcsold be: Enable direct deployment of Canvas models.

## Deployment tesztelése

Parancs:

```bash
export AWS_DEFAULT_REGION=eu-north-1
export ENDPOINT_NAME="A TE ENDPOINT-OD NEVE"
```

```bash
aws sagemaker-runtime invoke-endpoint \
  --region $AWS_DEFAULT_REGION \
  --endpoint-name $ENDPOINT_NAME \
  --content-type text/csv \
  --accept application/json \
  --body fileb://Deployment_teszt.csv   \
  response.json
```
