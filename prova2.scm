; foldl
(define n 5)  ; Definim una constant

(define (suma x y)
  (+ x y))

(define (foldl f acc lst)
  (if (null? lst)
      acc
      (foldl f (f acc (car lst)) (cdr lst))))

(define (sumar-elements lst)
  (foldl suma 0 lst))

(define (main)
  (let ((i 3) (llista '(1 2 i 4 n)))
    (display "Suma de elements: ")
    (display (sumar-elements llista))
    (newline)))