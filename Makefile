a: clean venal execute

clean:
	rm venal || true

venal:
	g++ -o venal venal.cpp

execute:
	./venal
