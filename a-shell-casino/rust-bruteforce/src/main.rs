// def intrand32(last):
//     ret = last
//     h = ret / 127773
//     l = ret - 127773*h
//     t = 16807 * l - 2836 * h
//     ret = z3.If(t & (1 << 31) != 0, t + 0x7fffffff, t)
//     return ret

use std::mem::swap;

fn intrand32(last: u32) -> u32 {
    let ret = last;
    let h = ret / 127773;
    let l = ret - 127773 * h;
    let t = 16807 * l - 2836 * h;
    if t & (1 << 31) != 0 {
        t + 0x7fffffff
    } else {
        t
    }
}

// def brand(env):
//     env.rseed = intrand32(env.rseed)
//     ret = (env.rseed >> 16) ^ (env.rseed & 65535)
//     return ret & 32767

#[derive(Copy, Clone, Debug)]
struct Env {
    rseed: u32,
}
fn brand(env: &mut Env) -> u32 {
    env.rseed = intrand32(env.rseed);
    let ret = (env.rseed >> 16) ^ (env.rseed & 65535);
    return ret & 32767;
}

fn genseed(tv_sec: u64, tv_usec: u64) -> Env {
    let mut iv: u32 = 0x4bba20;
    let pid = 1;
    let ppid = 0;
    iv = (tv_sec as u32) ^ (tv_usec as u32) ^ pid ^ ppid ^ 1000 ^ iv;
    Env { rseed: iv }
}
const V: [bool; 50] = [true, false, false, false, false, false, true, true, false, true, true, false, false, false, false, true, false, false, true, true, false, false, false, false, true, false, true, false, true, false, false, false, false, false, false, false, false, false, true, false, false, true, true, false, false, true, false, false, false, false];

fn tv_guess(test_len: usize, out: bool) -> bool {
    let tv_sec = 1740151543;
    let mut pred_next: Option<u32> = None;
    'outer: for tv_usec in 0..1_000_000 {
        let mut env = genseed(tv_sec, tv_usec);
        for i in 0..test_len {
            let r = brand(&mut env);
            if (r % 3 == 1) != V[i] {
                continue 'outer;
            }
        }
        let pred = brand(&mut env);
        if let Some(p) = pred_next {
            if p != pred {
                return false;
            }
        } else {
            pred_next = Some(pred);
        }
        if out {
            println!("| tv_usec: {tv_usec}, predicted_next: {}", pred);
        }
    }
    true
}

fn straight_guess(test_len: usize, out: bool) -> bool {
    let mut pred_next: Option<u32> = None;
    'outer: for rseed in 0..u32::MAX {
        // let mut env = genseed((tv_sec + dt) as u64, tv_usec);
        let mut env = Env { rseed };
        let mut r;
        for i in 0..test_len {
            r = brand(&mut env);
            if (r % 3 == 1) != V[i] {
                continue 'outer;
            }
        }
        let pred = brand(&mut env);
        if let Some(p) = pred_next {
            if p != pred {
                return false;
            }
        } else {
            pred_next = Some(pred);
        }
        if out {
            println!("| rseed: {rseed}, predicted_next: {}", pred);
        }
    }
    true
}

fn check_testlen() {
    let fs = [("straight_guess", straight_guess as fn(usize, bool) -> bool), ("tv_guess", tv_guess as fn(usize, bool) -> bool)];
    for test_len in 10..V.len() {
        println!("test_len = {test_len}");
        for (s,f) in fs {
            if f(test_len, false) { 
                println!("{s} succeeded! ");
                f(test_len, true);
            }
        }
    }
}

fn main() {
    check_testlen();
}
