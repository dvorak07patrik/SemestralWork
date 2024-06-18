# Formula Racing Manager

## Deník projektu
Níže budou popsané základní kroky při tvoření projektu

### Výběr dat která budou vizualizována
- **Výběr podle dostupných zdrojů**: prolistování veřejně přístupných databází a výběr dat, která sedí na podstatu projektu.

### Databáze
- **Schéma datového skladu**: tvorba schéma datového skladu na základě dostupných dat a dat potřebných pro aplikaci.
- **Vužití PostgreSQL**: využijeme databázovou aplikaci PostgreSQL pro uchovávání dat

### Nahrání dat z datasetu v kagglu do mé databáze
- **Chunkování dat**: pro menší paměťovou náročnost je lepší data chunkovat, abychom do paměti zbytečně nenačítaly velké soubory, které se do ní nevejdou.
- **Nahrávání pomocí python scriptů**: pomocí python scriptů rozdělíme data na chunky, tranformujeme je a nahrajeme do vytvořené PostgreSQL databáze
- **Použité knihovny**: pandas, sqlalchemy

### Kontrola dat
- **Porovnání vybraných dat**: porovná nahraná data s dalšími dvěma datasety.
- **Pokud porovnání selže nahradí data**: pokud se budou naše data od kontrolních lišit a kontrolní se budou navzájem shodovat - nahradíme naše data kontrolními daty

### Tvorba ETL workflow

