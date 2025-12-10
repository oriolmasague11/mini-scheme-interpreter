; Operacions amb llistes
(define (main)
  (let ((llista '(1 2 3 4 5))) 
    (let ((primer-element (car llista))  
          (resta-de-la-llista (cdr llista)) 
          (nova-llista (cons 0 llista)))   
      (display "Llista original: ")
      (display llista)
      (newline)
      
      (display "Primer element: ")
      (display primer-element)
      (newline)
      
      (display "Resta de la llista: ")
      (display resta-de-la-llista)
      (newline)
      
      (display "Nova llista (amb 0 al principi): ")
      (display nova-llista)
      (newline))))