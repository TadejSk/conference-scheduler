Navodila za namestitev:

1.) Potrebni programi
	Za namestitev aplikacije je najprej potrebno namestiti sledča programska okolja:
		-Python 3.4 ali novejši (https://www.python.org/downloads/)
            Pri operacijskem sistemu Ubuntu je python 3.4 že nameščen, vendar ga je treba pognati z ukazom
                python3, in ne z ukazom python
		-PostgreSQL (http://www.postgresql.org/download/)
			Potrebno je namestiti namestiti vse razvijalske knjižnice PostgreSQL (postgres in postgres-client)
			
2.) Namestitev izvorne kode
	Izvorno kodo z ukazom git clone namestite v poljuben direktorij
	
3.) Nastavitev virtualnega okolja
	V direktoriju, v katerem se nahaja izvorna koda poženite ukaz "virtualenv ENV".
	Virtualno okolje zaženite z ukazom:
		source  bin/activate (na sistemih POSIX)
	Nato je potrebno namestiti knjižnice, ki jih aplikacija potrebuje delovanje.
		Večino knjižnic se lahko preprosto namesti z ukazom "pip install -r requirements.txt"
	Za scipy je potrebno malo več, navodila so na http://www.scipy.org/install.html

4.) Namestitev podatkovne baze
	Za ustrezno delovanje aplikacije je najprej potrebno ustvariti podatkovno bazo PostgreSQL
	Navodila za to so na straneh http://www.postgresql.org/docs/manuals/, specifično za ubuntu
		pa na https://help.ubuntu.com/community/PostgreSQL. Na sistemu Windows je to najlažje 
        storiti s pomočjo vmesnika pgadmin3,

5.) Konfiguracija nastavitev
    V datoteki diploma/settings_secret.py je potrebno spremeniti nastavitve za podatkovno bazo
        (NAME, USER, PASSWORD, PORT in HOST)

6.) Migracije
    Za končno namestitev podatkovne baze je potrebno pognati ukaz python manage.py migrate

7.)Zagon strežnika
    Strežnik se zažene z ukazom python manage.py runserver.
    Aplikacija je nato dostopna na naslovu 127.0.0.1:8000/app/login/

8.) Dodajanje uporabnikov
    V aplikacijo je najprej potrebno dodati administratorja z ukazom python manage.py createsuperuser --username=ime --email=ime@primer.com
    Dodatne uporabnike lahko dodamo preko spletnega vmesnika na naslovu http://127.0.0.1:8000/admin 
    

    
        
		  
