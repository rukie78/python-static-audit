# Makefile pentru audit static

install:
	pip install -r requirements.txt

audit:
	python audit_en_full.py .

test: audit
	@echo "Audit complete. Check the output report."

clean:
	rm -f audit_report_*.txt
