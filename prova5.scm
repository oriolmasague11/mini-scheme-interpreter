; Operacions amb and i or
(define (even? n)
  (= (mod n 2) 0))

(define (evaluar-condicio a b)
  (cond
    ((and (> a 0) (< b 0)) "positiu i negatiu") 
    ((or (= a 0) (= b 0)) "zero")              
    ((and (even? a) (even? b)) "tots dos parells")     
    (#t "altres")))  

(define (main) 
  (display (evaluar-condicio (read) (read)))  
  (newline)
  (display (evaluar-condicio (read) (read)))   
  (newline)
  (display (evaluar-condicio (read) (read)))  
  (newline)
  (display (evaluar-condicio (read) (read)))  
  (newline))