# EPO patent process
Process EPO patent documents

| field              | from                   | example                       |
|:-------------------|:-----------------------|:------------------------------|
| publication_number | R>SDOBI>B100>B110      | 1289519                       |
| plain_designation  | R>SDOBI>B100>B120>B121 | EUROPEAN PATENT SPECIFICATION |
| kind               | R>SDOBI>B100>B130      | B1                            |
| country            | R>SDOBI>B100>B190      | EP                            |
| application_number | R>SDOBI>B200>B210      | 01935605.4                    |
| filing_date        | R>SDOBI>B200>B220>date | 20010515                      |

``` json
{
    "publication_number": "1289519",
    "plain_designation": "EUROPEAN PATENT SPECIFICATION",
    "kind": "B1",
    "country": "EP",
    "application_number": "01935605.4",
    "filing_date": 20010515
}
```