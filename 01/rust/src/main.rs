// Advent of Code 2018
// Day 1

use std::fs;
use std::collections::HashSet;

fn solve_a(data: &Vec<i32>) -> i32 {
    data.iter().sum()
}

fn solve_b(data: &Vec<i32>) -> i32 {
    let mut memo = HashSet::new();
    let mut freq: i32 = 0;
    for delta in data.iter().cycle() {
        freq = freq + delta;
        if memo.contains(&freq) {
            return freq;
        }
        memo.insert(freq);
    }
    freq
}

fn main() {
    // Why couldn't this whole thing be done with an iterator
    // using map and collect?
    let input = fs::read_to_string("../input01.txt").unwrap();
    let mut data: Vec<i32> = Vec::new();
    for line in input.lines() {
        let i = line.parse::<i32>().unwrap();
        data.push(i);
    }
    println!("{:?}", solve_a(&data));
    println!("{:?}", solve_b(&data));
}
