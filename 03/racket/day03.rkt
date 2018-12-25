#lang racket

;; Advent of Code 2018
;; Day 3

(struct claim (id x y width height) #:transparent)
(struct fabric (map claims) #:transparent)

(define (parse-claim string-data)
  (let* ([tokens (string-split string-data)]
         [id (string->number (substring (first tokens) 1))]
         [coordinates (map string->number (string-split (string-trim (third tokens) ":") ","))]
         [dimensions (map string->number (string-split (fourth tokens) "x"))])
    (claim id (first coordinates) (second coordinates) (first dimensions) (second dimensions))))

(define (map-claim claim fabric-map)
  (for ([y (in-range (claim-y claim) (+ (claim-y claim) (claim-height claim)))])
    (let ([row (vector-ref fabric-map y)])
      (for ([x (in-range (claim-x claim) (+ (claim-x claim) (claim-width claim)))])
        ;(fprintf (current-output-port) "~a ~a ~a\n" x y claim)
        (vector-set! row x (cons (claim-id claim) (vector-ref row x)))))))

(define (map-claims claims size)
  (define fabric-map (for/vector ([y size]) (for/vector ([x size]) '())))
  (define (map-claims0 claims0)
    (if (empty? claims0)
        (fabric fabric-map (length claims))
        (begin
          (map-claim (first claims0) fabric-map)
          (map-claims0 (rest claims0)))))
  (map-claims0 claims))

(define (solveA fabric)
  (foldl + 0 (for/list ([row (fabric-map fabric)])
               (vector-count (lambda (x) (> (length x) 1)) row))))

(define (add-conflicts conflicts claim-ids)
  (for ([c (in-list claim-ids)])
    (vector-set! conflicts (- c 1) #t)))

(define (solveB fabric)
  (let ([conflicts (make-vector (fabric-claims fabric) #f)])
    (for ([row (in-vector (fabric-map fabric))])
      (for ([claims (in-vector row)])
        (when (> (length claims) 1)
            (add-conflicts conflicts claims))))
    (+ 1 (vector-member #f conflicts))))

(module+ test
  (require rackunit)
  (define test-data (list
                     (parse-claim "#1 @ 1,3: 4x4")
                     (parse-claim "#2 @ 3,1: 4x4")
                     (parse-claim "#3 @ 5,5: 2x2")))
  (check-equal? (parse-claim "#123 @ 3,2: 5x4") (claim 123 3 2 5 4))
  (check-equal? (solveA (map-claims test-data 10)) 4)
  )

(module+ main
  (define main
    (let* ([claims (map parse-claim (file->lines "../input03.txt"))]
           [fabric (map-claims claims 1000)])
      (fprintf (current-output-port) "~a\n" (solveA fabric))
      (fprintf (current-output-port) "~a\n" (solveB fabric)))))