# System Wspomagania Decyzji dla Analizy Przestępczości w województwie Dolnośląskim
## 1. Cel projektu
Celem projektu jest stworzenie systemu wspomagania decyzji dla administracji publicznej i służb porządkowych, który pozwoli na: - Identyfikację trendów przestępczości w różnych powiatach województwa Dolnośląskiego. - Prognozowanie liczby przestępstw na kolejne lata na podstawie danych historycznych z lat 2013-2023 - Wizualizację wyników dla lepszego zrozumienia sytuacji w regionach. - Optymalne rozmieszczenie zasobów policyjnych i społecznych na podstawie prognozowanych trendów przestępczości.
System może być wykorzystywany przez lokalne władze i służby policyjne do monitorowania dynamiki przestępczości i podejmowania decyzji dotyczących działań prewencyjnych.
## 2. Opis danych źródłowych
Dane pochodzą z Banku Danych Lokalnych (BDL), który jest oficjalnym systemem Głównego Urzędu Statystycznego (GUS) w Polsce(https://bdl.stat.gov.pl/bdl/start). Dane są przechowywane w pliku dane.csv.
Struktura danych:
1.Pierwsza kolumna (Nazwa) – zawiera nazwy powiatów.
2.Pierwszy wiersz – zawiera nazwy kategorii przestępstw oraz lata w formacie: "nazwa kategorii;rok;jednostka", np. "ogółem;2013;[-]".
3.Pozostałe wiersze – zawierają wartości statystyczne dla danej kategorii, powiatu i roku.
Kategorie przestępstw obejmują m.in.:
•Ogółem – całkowita liczba przestępstw w danym roku.
• Ogółem, Polska = 100 – wskaźnik porównawczy dla kraju.
•Przestępstwa kryminalne – obejmujące m.in. kradzieże, rozboje.
• Przestępstwa gospodarcze – np. oszustwa podatkowe, korupcja.
Dane obejmują okres od 2013 do 2023 roku.
Format pliku: CSV, wartości oddzielone średnikami ;.
