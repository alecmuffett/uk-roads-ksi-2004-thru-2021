table.csv: ksi-table.py reduced.csv
	./ksi-table.py reduced.csv

reduced.csv: ksi-reduce.py data.csv
	./ksi-reduce.py data.csv
