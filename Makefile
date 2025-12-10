ANTLR=antlr4
GRAMMAR=scheme.g4

default:
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR)

clean:
	@echo "Cleaning generated files..."
	@rm -f *.interp *.tokens schemeParser.py schemeVisitor.py schemeLexer.py
