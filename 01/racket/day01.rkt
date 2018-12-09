#lang racket

;; Advent of Code 2018
;; Day 1

(require racket/set)

(define (solveB data)
  (define (solveB0 data0 freq memo)
    (cond [(empty? data0) (solveB0 data freq memo)]
          [(set-member? memo freq) freq]
          [ else (solveB0 (rest data0) (+ freq (first data0)) (set-add memo freq))]))
  (solveB0 data 0 (list->seteq '())))
        
(define (solveA data)
  (foldl + 0 data))

(define main
  (let ([data (map string->number (file->lines "../input01.txt"))])
    (fprintf (current-output-port) "~a\n" (solveA data))
    (fprintf (current-output-port) "~a\n" (solveB data))))