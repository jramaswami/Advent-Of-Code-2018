#lang racket

;; Advent of Code 2018
;; Day 2

(require math/statistics)

(struct box-class (double triple) #:transparent)
(struct similar-boxes (left-box right-box) #:transparent)

(define (classify-box box-id)
  (define-values (ltrs freqs) (count-samples box-id))
  (define (classify0 ltrs0 freqs0 class)
    (if (empty? ltrs0)
        class
        (let ([f (first freqs0)]
              [l (first ltrs0)])
          (classify0 (rest ltrs0) (rest freqs0) (box-class (or (box-class-double class) (= 2 f))
                                                           (or (box-class-triple class) (= 3 f)))))))
  (classify0 ltrs freqs (box-class #f #f)))

(define (solveA data)
  (define (solveA0 data0 doubles triples)
    (if (empty? data0)
        (* doubles triples)
        (let ([class (classify-box (first data0))])
          (solveA0
           (rest data0)
           (if (box-class-double class) (+ 1 doubles) doubles)
           (if (box-class-triple class) (+ 1 triples) triples)))))
  (solveA0 data 0 0))

(define (compare-box-ids box-id0 box-id1)
  (define id-length (string-length box-id0))
  (define (compare0 index delta)
    (cond [(> delta 1) #f]
          [(>= index id-length) (= 1 delta)]
          [(equal? (string-ref box-id0 index) (string-ref box-id1 index)) (compare0 (+ 1 index) delta)]
          [else (compare0 (+ 1 index) (+ 1 delta))]))
  (compare0 0 0))

(define (compare-box-to-rest box-id0 boxes)
  (if (empty? boxes)
      (similar-boxes #f #f)
      (if (compare-box-ids box-id0 (first boxes))
          (similar-boxes box-id0 (first boxes))
          (compare-box-to-rest box-id0 (rest boxes)))))

(define (find-similar-boxes data)   
  (define (find-similar-boxes0 box-id0 boxes)
    (if (empty? boxes)
        (similar-boxes #f #f)
        (let ([similar-boxes-result (compare-box-to-rest box-id0 boxes)])
          (if (equal? (similar-boxes-left-box similar-boxes-result) #f)
              (find-similar-boxes0 (first boxes) (rest boxes))
              similar-boxes-result))))
  (find-similar-boxes0 (first data) (rest data)))

(define (get-common-letters box-id0 box-id1)
  (define id-length (string-length box-id0))
  (define (get-common-letters0 index)
    (if (>= index id-length)
        '()
        (let ([a (string-ref box-id0 index)]
              [b (string-ref box-id1 index)])
          (if (equal? a b)
              (cons a (get-common-letters0 (+ 1 index)))
              (get-common-letters0 (+ 1 index))))))
  (list->string (get-common-letters0 0)))

(define (solveB data)
  (let ([similar-boxes-result (find-similar-boxes data)])
    (if (similar-boxes-left-box similar-boxes-result)
        (get-common-letters (similar-boxes-left-box similar-boxes-result)
                            (similar-boxes-right-box similar-boxes-result))
        "")))
                       
(module+ main
  (define main
    (let ([data (file->lines "../input02.txt")])
      (fprintf (current-output-port) "~a\n" (solveA data))
      (fprintf (current-output-port) "~a\n" (solveB data)))))

(module+ test
  (require rackunit)
  (define test-data-1 '("abcdef" "bababc" "abbcde" "abcccd" "aabcdd" "abcdee" "ababab"))
  (define test-data-2 '("abcde" "fghij" "klmno" "pqrst" "fguij" "axcye" "wvxyz"))
  (check-equal? (classify-box "abcdef") (box-class #f #f))
  (check-equal? (classify-box "bababc") (box-class #t #t))
  (check-equal? (classify-box "abbcde") (box-class #t #f))
  (check-equal? (classify-box "abcccd") (box-class #f #t))
  (check-equal? (classify-box "aabcdd") (box-class #t #f))
  (check-equal? (classify-box "abcdee") (box-class #t #f))
  (check-equal? (classify-box "ababab") (box-class #f #t))
  (check-equal? (solveA test-data-1) 12)
  (check-equal? (find-similar-boxes test-data-2) (similar-boxes "fghij" "fguij"))
  (check-equal? (get-common-letters "fghij" "fguij") "fgij")
  (check-equal? (solveB test-data-2) "fgij"))