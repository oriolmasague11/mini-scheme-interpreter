; Funcionament del cond
(define (even? n)
  (= (mod n 2) 0))

(define (numero-par-o-impar n)
  (cond
    ((= n 0) "zero")
    ((even? n) "par")
    (#t "impar")))

(define (main)
  (display "Introdueix un número: ")
  (let ((input (read)))
    (let ((resultat (numero-par-o-impar input)))
      (display "El número és: ")
      (display resultat)
      (newline))))