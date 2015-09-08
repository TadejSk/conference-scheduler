Navodila za namestitev:

1.) Potrebni programi
	Za namestitev aplikacije je najprej potrebno namestiti sledča programska okolja:
		-Python 3.4 ali novejši (https://www.python.org/downloads/)
		-PostgreSQL (http://www.postgresql.org/download/)
			Na sistemu Windows je potrebno pod sistemsko spremenljivko PATH dodati /bin direktorij
			Na sistemu Linux je potrebno le namestiti vse razvijalske knjižnice PostgreSQL
			
2.) Namestitev izvorne kode
	Izvorno kodo z ukazom git clone namestite v poljuben direktorij
	
3.) Nastavitev virtualnega okolja
	V direktoriju, v katerem se nahaja izvorna koda poženite ukaz "virtualenv ENV".
	Virtualno okolje zaženite z ukazom:
		source  bin/activate (na sistemih POSIX)
		ENV\Scripts\activate (na sistemu Windows)
	Nato je potrebno namestiti knjižnice, ki jih aplikacija potrebuje delovanje.
		Najprej je potrebno namestiti knjižnico scipy.
			Na sistemu windows je na voljo na naslovu
		Večino knjižnic se lahko preprosto namesti z ukazom "pip install -r requirements.txt"
