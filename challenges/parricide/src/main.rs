#![feature(lang_items)]
#![feature(core_intrinsics)]
#![feature(rustc_private)]
#![feature(start)]
#![feature(asm)]

#![no_std]
#![no_main]


use core::intrinsics;
use core::panic::PanicInfo;


extern crate libc;


#[inline(always)]
#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub unsafe fn getppid() -> i32 {
    let ppid: i32;
    asm!("syscall" : "={eax}"(ppid) 
         :"{rax}"(0x6e)
         :"rcx", "r11", "memory"
         :"volatile"
        );
    ppid
}

#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub unsafe fn kill(pid: i32, sig: i32) -> i32 {
    let ret: i32;
    asm!("syscall" : "={eax}"(ret) 
         :"{rax}"(0x3e), "{rdi}"(pid), "{rsi}"(sig)
         :"rcx", "r11", "memory"
         :"volatile"
        );
    ret
}

#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub unsafe fn write(fd: i32, buf: *const u8, size: usize) -> i32 {
    let ret: i32;
    asm!("syscall" : "={eax}"(ret) 
         :"{rax}"(0x01), "{rdi}"(fd), "{rsi}"(buf), "{rdx}"(size)
         :"rcx", "r11", "memory"
         :"volatile"
        );
    ret
}

#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub unsafe fn read(fd: i32, buf: *mut u8, size: usize) -> i32 {
    let ret: i32;
    asm!("syscall" : "={eax}"(ret) 
         :"{rax}"(0x00), "{rdi}"(fd), "{rsi}"(buf), "{rdx}"(size)
         :"rcx", "r11", "memory"
         :"volatile"
        );
    ret
}

#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
pub unsafe fn open(filename: *const u8, flags: isize, mode :isize) -> i32 {
    let ret: i32;
    asm!("syscall" : "={eax}"(ret) 
         :"{rax}"(0x02), "{rdi}"(filename), "{rsi}"(flags), "{rdx}"(mode)
         :"rcx", "r11", "memory"
         :"volatile"
        );
    ret
}

const STDIN: i32 = 0;
const STDOUT: i32 = 1;

pub fn print(string: &str) {
    unsafe { write(STDOUT, string.as_ptr(), string.len()); }
}
/*
pub fn readstr(fd: i32, size: usize) -> Box<str> {
    let buff: &mut [u8] = &mut [0; size]; 
    unsafe { read(fd, buff.as_mut_ptr(), buff.len()); }
    &str::from_utf8(buff)
}
*/
const SIGKILL: i32 = 9;
const SIGTERM: i32 = 15;

#[no_mangle]
pub fn main(_argc: i32, _argv: *const *const u8) -> i32 {
    let parent : i32;
    unsafe {
        parent = getppid();
        kill(parent, SIGTERM);
        kill(parent, SIGKILL);
        let buff: &mut [u8] = &mut [0; 100];
        let fd = open("/dev/urandom\x00".as_ptr(), 0, 0);
        read(fd, buff.as_mut_ptr(), buff.len());
        print("if you can tell me the ones complement of the following i'll tell you a flag ;)\n");
        write(STDOUT,  buff.as_ptr(), buff.len());
        let user_buff: &mut [u8] = &mut [0; 100];
        read(STDIN, user_buff.as_mut_ptr(), user_buff.len());
        for i in 0..buff.len() {
            buff[i] = !buff[i];
        }
        let mut is_good = true;
        for i in 0..buff.len() {
            if buff[i] != user_buff[i] {
                is_good = false;
            }
        }
        if is_good {
            let flag_fd = open("flag.txt\x00".as_ptr(), 0, 0);
            let flag_buff: &mut [u8] = &mut [0; 32];
            read(flag_fd, flag_buff.as_mut_ptr(), flag_buff.len());
            write(STDOUT, flag_buff.as_ptr(), flag_buff.len());
        }
    }
    0
}

#[lang = "eh_personality"] extern fn eh_personality() { } 
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    unsafe { intrinsics::abort() }
}

