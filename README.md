# Mini Scheme:

Aquest projecte implementa un petit intèrpret per al llenguatge `Scheme` amb l'ús de la biblioteca ANTLR4. El codi avalua expressions de Scheme suportant operacions aritmètiques, lògiques, condicionals, funcions, llistes i entrada/sortida. 


### Compilació:

Per compilar hem d'executar l'ordre: 

 -``` make ```
 
Per executar un programa: 

 -``` python3 scheme.py <nom_programa.scm> ```
 
Es mostrarà la sortida per la sortida estàndard. 
Podem redirigir l'entrada i la sortida per mitjà de pipes:
 
 -``` python3 scheme.py <nom_programa.scm> < entrada.txt > sortida.txt ```
 

### Característiques:

Operacions aritmètiques: es suporten les operacions de suma (+), resta (-), multiplicació (*), divisió (/), potència (^), mòdul (mod).

Operacions lògiques: es suporten les operacions lògiques: >, <, =, <>, and, or, not. 

Funcions: es poden definir funcions amb la forma  -``` (define (function arg1 arg2 ...) expr) ```.
Les funcions es poden passar com a paràmetre; s'admeten funcions d'ordre superior. 

Condicionals: disposem dels condicionals `if` i `cond` (equivalent a `switch).

Llistes: les llistes es defineixen amb `'(` . Es suporten diferents operacions amb llistes com `car`, `cdr`, `cons` i la comprovació de llistes buides amb `null?`. 

Entrada i sortida: es suporta la lectura de dades pel canal estàndard d'entrada i la sortida pel canal estàndard. Es poden realitzar salts de línia amb `newline`. 


#### Breu explicació del codi

La clase principal `EcalVisitor` implementa el patró Visitor, recorrent l'arbre sintàctic generat per ANTLR i avaluant les expressions conforme a les regles del llenguatge. L'avaluador avalua expressions, operacions, llistes, condicionals i crides a funcions a més de gestionar els canvis de contexts mitjançant les taules de símbols: `ts` per variables locals i `tfs` per funcions definides. 


#### Explicació dels jocs de prova

Tots els jocs de prova estan pensats per ser executats com a: 

 -``` python3 scheme.py <provaX.scm> < <provaX.inp> ```
 
 Podeu veure un exemple de la sortida esperada al corresponent fitxer .out del joc de proves. 

Joc de proves `prova1.scm`: funció factorial que ens mostra com l'intèrpret permet recursivitat. A més es mostra el funcionament del `let` per definir variables locals així com el correcte funcionament amb caràcters estranys en strings i comentaris.

Joc de proves `prova2.scm`: s'implementa la funció d'ordre superior `foldl`. Mostra l'ús de funcions d'ordre superior i la definició de constants. També podem observar operacions amb llistes. Observem com els comentaris són ignorats per l'intèrpret. 

Joc de proves `prova3.scm`: funció que retorna si un número és parell o imparell. Mostra el funcionament de funcions dins d'altres funcions, així com el correcte funcionament del `cond`. Observem també que les funcions admeten caràcters com "-" o "?".

Joc de proves `prova4.scm`: programa que efectua diverses operacions amb llistes fent ús dels operadors `car`, `cons` i `cdr` i mostra els diferents resultats per pantalla. 

Joc de proves `prova5.scm`: Programa per calcular la paritat de dos nombres. Mostra el correcte funcionament del `cond` i dels operadors logics and i or. S'observa el correcte funcionament de la sortida estàndard així com del salt de línia `newline`.
