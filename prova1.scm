; Funció factoral
(define (factorial n)
  (if (< n 1)
      1
      (* n (factorial (- n 1)))))

(define (main)
  (let ((test-value (read))) 
    (display "El factorial de ")
    (display test-value)
    (display " és: ")
    (display (factorial test-value))
    (newline)))