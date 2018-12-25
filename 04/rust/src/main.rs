// Advent of Code 2018
// Day 4

use std::fs;

#[derive(Debug)]
struct Observation {
    month: u8,
    day: u8,
    hour: u8,
    minute: u8,
    event: String
}

fn parse_observation(input: &String) -> Observation {
    let month: u8 = (&input[6..8]).parse().unwrap();
    let month: u8 = (&input[6..8]).parse().unwrap();
    let month: u8 = (&input[6..8]).parse().unwrap();
    let month: u8 = (&input[6..8]).parse().unwrap();
    let month: u8 = (&input[6..8]).parse().unwrap();
    let month: u8 = (&input[6..8]).parse().unwrap();
    let month: u8 = (&input[6..8]).parse().unwrap();

}

fn main() {
    let input = fs::read_to_string("../input04.txt").expect("File read error.");
    println!("{}", input);
}
