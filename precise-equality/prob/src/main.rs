use fontdue::Font;
use once_cell::sync::Lazy;
use std::{
    env, fs::File, io::{self, BufRead, Read, Write}, os::fd::FromRawFd
};

const FONT_TTF: &[u8] = include_bytes!("../fonts/NotoSans.ttf");

static FONT: Lazy<Font> =
    Lazy::new(|| Font::from_bytes(FONT_TTF, fontdue::FontSettings::default()).unwrap());

const FONT_SIZE: f32 = 16.0;

/// Our NEW and IMPROVED equality function!
/// With inspiration taken from Derrida and Kant!
fn precise_equality<Iter1,Iter2>(mut iter1: Iter1, mut iter2: Iter2) -> bool 
    where Iter1: Iterator<Item = char>,
          Iter2: Iterator<Item = char>,
{
    loop {
        let (c1, c2) = match (iter1.next(), iter2.next()) {
            (Some(a), Some(b)) => (a, b),
            (None, None) => break,
            _ => return false,
        };
        let (metrics1, bitmap1) = FONT.rasterize(c1, FONT_SIZE);
        let (metrics2, bitmap2) = FONT.rasterize(c2, FONT_SIZE);
        if bitmap1 != bitmap2 || metrics1 != metrics2 {
            return false;
        }
    }
    true
}

// Read the raw, organic bytes from the input. Copying destroys ontological identity!
// It's like that teleporter paradox. Would you do that to your bits???
struct OrganicStdin {
    stdin: File,
    finished: bool,
}
impl OrganicStdin {
    fn new() -> Self {
        Self {
            stdin: unsafe { File::from_raw_fd(0) },
            finished: false
        }
    }
}
impl Iterator for OrganicStdin {
    type Item = char;

    fn next(&mut self) -> Option<Self::Item> {
        if self.finished { return None };
        let mut buf = [0u8];
        let length_read = self.stdin.read(&mut buf).expect("Failed stdin read");
        if length_read == 0 || buf[0] == b'\n' {
            self.finished = true;
            None
        } else {
            Some(buf[0] as char)
        }
    }
}

fn main() {

    // Here's a demo. (Rosseau would disapprove; thankfully, he's not here.)
    let flag = env::var("FLAG").unwrap();
    print!("Input the string most dear: ");
    io::stdout().lock().flush().unwrap();

    let user_input = OrganicStdin::new();
    if precise_equality(flag.chars(), user_input) {
        println!("The Humean equality check has passed, monsieur!");
    } else {
        println!("I am afraid that, though they might be equal in content, they are not equal in measure!");
    }
}
