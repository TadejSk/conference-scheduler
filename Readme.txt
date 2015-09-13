Navodila za namestitev:

Namestitev je na žalost precej zapletena, saj je potrebno pravilno naložiti vse potrebne knjižnice in
podatkovno bazo. Sledeče korake sem preveril na operacijskem sistemu Ubuntu 12.04, čeprav aplikacija
lahko teče tudi na drugih operacijskih sistemih.

1.) Potrebni programi
	Za namestitev aplikacije je najprej potrebno namestiti sledeča programska okolja:
		-Python 3.4 ali novejši (https://www.python.org/downloads/)
            Pri operacijskem sistemu Ubuntu je python 3.4 že nameščen, vendar ga je treba pognati z ukazom
                python3, in ne z ukazom python
		-PostgreSQL (http://www.postgresql.org/download/)
			Potrebno je namestiti namestiti vse razvijalske knjižnice PostgreSQL (postgres in postgres-client)
			
2.) Namestitev izvorne kode
	Izvorno kodo namestite v poljuben direktorij (lahko preko githuba, ali pa samo s kopiranjem iz dropboxa).
	
3.) Nastavitev virtualnega okolja
	V direktoriju, v katerem se nahaja izvorna koda poženite ukaz "virtualenv ENV".
	Virtualno okolje zaženite z ukazom:
		source  bin/activate (na sistemih POSIX)
    Uporaba virtualnega okolja ni nujno potrebna, vendar je lahko koristna, saj ustvari
        novo okolje jezika python, brez predhodno namečšenih knjižnic  

	Nato je potrebno namestiti knjižnice, ki jih aplikacija potrebuje delovanje.
    Potrebne knjižnice so navedene v datoteki requirements.txt
	Večino knjižnic se lahko preprosto namesti z ukazom "pip install -r requirements.txt"
	Za scipy je potrebno malo več, navodila so na http://www.scipy.org/install.html

4.) Namestitev podatkovne baze
	Za ustrezno delovanje aplikacije je najprej potrebno ustvariti podatkovno bazo PostgreSQL.
	Navodila za to so na straneh http://www.postgresql.org/docs/manuals/, specifično za ubuntu
	pa na https://help.ubuntu.com/community/PostgreSQL. Na sistemu Windows je to najlažje 
    storiti s pomočjo vmesnika pgadmin3. Podrobnejši napotki za namestitev na sistemu Windows
    so na https://wiki.postgresql.org/wiki/Running_%26_Installing_PostgreSQL_On_Native_Windows.

5.) Konfiguracija nastavitev
    V datoteki diploma/settings_secret.py je potrebno spremeniti nastavitve za podatkovno bazo
    (NAME, USER, PASSWORD, PORT in HOST). Za zagotovitev varnosti je pred deployanjem aplikacije
    na splet potrebno spremenit še secret key (https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY)

6.) Migracije
    Za končno namestitev podatkovne baze je potrebno pognati ukaz python manage.py migrate

7.)Zagon strežnika
    Strežnik se zažene z ukazom python manage.py runserver.
    Aplikacija je nato dostopna na naslovu 127.0.0.1:8000/app/login/

8.) Dodajanje uporabnikov
    V aplikacijo je najprej potrebno dodati administratorja z ukazom python manage.py createsuperuser --username=ime --email=ime@primer.com
    Dodatne uporabnike lahko dodamo preko spletnega vmesnika na naslovu http://127.0.0.1:8000/admin 


Kje je kaj:

Korenski imenik vsebuje štiri imenike:
    1.) Templates:
        Imenik hrani kodo v šablonskem jeziku, ki ga za prikaz HTML strani uporablja ogrodje Django.
        Datoteke v tem imeniku skrbijo za prikaz spletnih strani, pri čimer vsaka datoteka opisuje
        eno stran.
    2.) Static:
        Imenik vsebuje vso kodo v jezikih CSS in Javascript, in sicer:
            - Podimeniki bootstrap, bootstrap-switch, d3 in nvd3 vsebujejo kodo knjižnic, ki jih aplikacija
            uporablja.
            - Podimenik export vsebuje stil css, ki se uporabi pri izvozu urnika
            - Podimenik js vsebuje kodo jezika javascript, ki skrbi za prikaz vizualizacije (datoteka
            clustering_results.js), funkcionalnost povleci in spusti (datoteka index.js) ter spreminjanje
            možnih parametrov gručenja (datoteka clustering_settings.js)
    3.) Diploma:
        Imenik vsebuje nastavitve aplikacije v datotekah settings.py (večina nastavitev) in settings_secret.py
        (nastavitve podatkovne baze). Ostale datoteke v tem imeniku so potrebne za delovanje ogrodja Django.

Imenik App:
Imenik vsebuje večino programske kode. Razdeljen je na sledeče podimenike:
    1.) classes:
        Tukaj se nahajajo pomožni razredi aplikacije, in sicer:
            - clusterer.py vsebuje vse funkcije, ki so potrebne za samodejno razvrščanje člankov.
            - model_forms.py hrani kodo, ki je potrebna za samodejno generacijo obrazcev.
            - paper.py se uporablja v datoteki raw_data.py za hranjenje podatkov o člankih.
            - raw_data.py vsebuje funkcije za uvoz člankov in podatkov o ocenjevalcih.
            - schedule_manager.py in schedule_settings.py hranita funkcije za spreminjanje urnika konference
                (dodajanje/premikanje/brisanje/zaklepanje člankov in časovnih rezin, dodajanje dnevov, ipd.).
    2.) migrations:
        Vsebuje migracije podatkovne baze, ki jih Django ustvari z ukazom makemigrations. Preko njih ukaz
        migrate ustrezno posodobi podatkovno bazo
    3.) templetetags:
        Vsebuje pomožne funkcije, ki razširijo šablonski jezik ogrodja Django za prikaz spletnih strani
    4.) views:
        Vsebuje skoraj vso programsko logiko aplikacije. Vsaka spletna stran ima v tem imeniku funkcije,
        ki se izvršijo ob prikazu te spletne strani.
            - views_clustering vsebuje funkcije za samodejno razvrščanje člankov in za prikaz rezultatov
                gručenja
            - views_conference vsebuje funkcije za upravljanje s konferencami (dodajanje, brisanje, preimenovanje,
                kopiranje)
            - views_login vsebuje funkcije za prijavo uporabnika
            - views_main vsebuje funkcije za prikaz glavnega uporabniškega vmesnika in za uvoz podatkov
            - views_papers vsebuje funkcije za upravljanje s članki (ustvarjanje, brisanje, dodajanje v urnik, ipd.)
            - views_settings vsebuje funkcije za spreminjanje strukture urnika (dodajanje/brisanje/premikanje
                časovnih rezin, spreminjanje začetnega časa konference, ipd.) 
    Imenik vsebuje še datoteke:
        - admin.py, ki je potrebna za delovanje administrativne spletne strani
        - models.py, ki hrani modele, ki jih ogrodje Django uporabi za shranjevanje podatkov v podatkovno bazo
        - urls.py, ki vsakemu spletnemu naslovu priredi ustrezno funkcijo iz imenika views
 
              
    

    
        
		  
