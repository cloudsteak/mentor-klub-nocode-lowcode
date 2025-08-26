# AWS Glue DataBrew

Az AWS Glue DataBrew egy vizuális adat-előkészítő szolgáltatás, amely lehetővé teszi a felhasználók számára, hogy könnyedén előkészítsék az adataikat anélkül, hogy kódolniuk kellene. A DataBrew segítségével gyorsan és egyszerűen végezhetők el az adattisztítási és átalakítási feladatok.

## Példa

Egy vállalat Excel fájlokban kap ügyfél- vagy termékadatokat, amelyeket egységesíteni kell (pl. hibás formátumok, felesleges oszlopok, hiányzó értékek). A DataBrew segít ezt vizuálisan, kódírás nélkül megoldani.
A tisztított adatokat ezután feltölthetjük egy Amazon S3 bucket-be, ahol további feldolgozásra kerülhetnek (pl. Amazon QuickSight-ban történő vizualizáció).

## Fájlok

- **Hibás_adatok.xlsx**: Példa adathalmaz, amely hibás formátumokat, felesleges oszlopokat és hiányzó értékeket tartalmaz. Kiváló példa a DataBrew használatára.
- **Helyes_adatok.xlsx**: Példa adathalmaz, amely helyes formátumokat és szükséges oszlopokat tartalmaz.
- **README.md**: A mappa tartalmának leírása és használati útmutató.

## Ötletek adatok tisztítására

Általában a következő feladatokat érdemes elvégezni az adatok tisztításakor:

- Hiányzó értékek kitöltése (pl. "N/A")
- Duplikált sorok eltávolítása
- Dátum formátum egységesítése (YYYY-MM-DD)
- Szám mező konvertálása "integer" típusra
- Felesleges oszlop törlése (pl. "Megjegyzések")
- Telefon formátum egységesítése (pl. "+36 30 123 4567" → "06301234567")

## Néhány példa

### Irányítószám tisztítása

1. Példa: Az irányítóaszám az alábbi módon szerepel: H-1234

Javítása: Irányítószám oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

- **Find**: `H-`
- **Replace with**: _(üresen hagyva)_

2. Példa: Az irányítószám az alábbi módon szerepel: 01234

Javítása: Irányítószám oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

- **Find**: `^0+(\d{4})$` (regex)
- **Replace with**: `$1`

### Testmagasság tisztítása

1. Példa: A testmagasság az alábbi módon szerepel: 1,80 m
   Javítása: Testmagasság oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

   - **Find**: `\s*m` (regex)
   - **Replace with**: ` ` (üresen hagyva vagy szóköz)

2. Példa: A testmagasság az alábbi módon szerepel: 1,80
   Javítása: Testmagasság oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

   - **Find**: `,` (vessző)
   - **Replace with**: `` (üresen hagyva)

3. Példa: A testmagasság az alábbi módon szerepel: 180 cm
   Javítása: Testmagasság oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:
   - **Find**: `\s*cm` (regex)
   - **Replace with**: ` ` (üresen hagyva vagy szóköz)

### Testsúly tisztítása

1. Példa: A testsúly az alábbi módon szerepel: 80 kg
   Javítása: Testsúly oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

   - **Find**: `\s*kg` (regex)
   - **Replace with**: ` ` (üresen hagyva vagy szóköz)

2. Példa: A testsúly az alábbi módon szerepel: 80,5
   Javítása: Column > Change type

### Születési dátum tisztítása

Alábbi dátumformátumok vannak:

- 04.09.2003
- 2004-11-27
- 11 Jan 89
- 1965.11.29.

Helyes formátum: 1965-11-29

1. Példa: A születési dátum az alábbi módon szerepel: 04.09.2003
   Javítása: Születési dátum oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

- **Find**: `(\d{2})\.(\d{2})\.(\d{4})` (regex)
- **Replace with**: `$3-$2-$1`

2. Példa: A születési dátum az alábbi módon szerepel: 1965.11.29.
   Javítása: Születési dátum oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

- **Find**: `(\d{4})\.(\d{2})\.(\d{2})` (regex)
- **Replace with**: `$1-$2-$3`

3. Példa: A születési dátum az alábbi módon szerepel: 11 Jan 89
   Javítása: Születési dátum oszlopban válasszuk a "Clean > Replace value or pattern" műveletet, és állítsuk be a következőket:

- **Find**: `(\d{2})\s(\w{3})\s(\d{2})` (regex)
- **Replace with**: `19$3-$2-$1`  
  (Ez a példa feltételezi, hogy a 2000 előtti éveket használjuk, ha a dátum 89, akkor 1989-et jelent.)
