extern crate volatile;
use volatile::{Volatile, ReadOnly, WriteOnly};

#[repr(C)]
pub struct Registers {
    ctrl: Volatile<u32>, //0x0
    _padding0: [u8; 4], // 0x8 - 0x4
    status: ReadOnly<u32>, //0x8
    _padding1: [u8; 196], // 0xD0 - 0xC
    ims: Volatile<u32>, //0xD0
    _padding2: [u8; 44], // 0x100 - 0xD4
    rctl: Volatile<u32>, //0x100
    _padding3: [u8; 764], // 0x400 - 0x104
    tctl: Volatile<u32>, //0x400
    _padding4: [u8; 12], // 0x410 - 0x404
    tipg: Volatile<u32>, //0x410
    _padding5: [u8; 9196], // 0x2800 - 0x414
    rdbal: Volatile<u32>, //0x2800
    rdbah: Volatile<u32>, //0x2804
    rdlen: Volatile<u32>, //0x2808
    _padding6: [u8; 4], // 0x2810 - 0x280C
    rdh: Volatile<u32>, //0x2810
    _padding7: [u8; 4], // 0x2818 - 0x2814
    rdt: Volatile<u32>, //0x2818
    _padding8: [u8; 4], // 0x2820 - 0x281C
    rdtr: Volatile<u32>, //0x2820
    _padding9: [u8; 4], // 0x2828 - 0x2824
    rxdctl: Volatile<u32>, //0x2828
    radv: Volatile<u32>, //0x282C
    _padding10: [u8; 976], // 0x2C00 - 0x2830
    rsrpd: Volatile<u32>, //0x2C00
    _padding11: [u8; 3068], // 0x3800 - 0x2C04
    tdbal: Volatile<u32>, //0x3800
    tdbah: Volatile<u32>, //0x3804
    tdlen: Volatile<u32>, //0x3808
    _padding12: [u8; 4], // 0x3810 - 0x380C
    tdh: Volatile<u32>, //0x3810
    _padding13: [u8; 4], // 0x3818 - 0x3814
    tdt: Volatile<u32>, //0x3818
    _padding14: [u8; 2020], // 0x4000 - 0x381C
    crcerrs: ReadOnly<u32>, //0x4000
    _padding15: [u8; 4604], // 0x5200 - 0x4004
    mta: Volatile<u32>, //0x5200
}
impl Registers {
    pub fn ctrl_read(&self) -> u32 {
        self.ctrl.read() & 0xFDFFFCFF 
    }

    pub fn ctrl_write(&mut self, value: u32) {
        self.ctrl.write(value & 0xDD031805) 
    }

    pub fn status_read(&self) -> u32 {
        self.status.read() & 0xFFFFFFF3 
    }

    pub fn ims_read(&self) -> u32 {
        self.ims.read() & 0xFFFFFFFF 
    }

    pub fn ims_write(&mut self, value: u32) {
        self.ims.write(value & 0x5FD3F7) 
    }

    pub fn rctl_read(&self) -> u32 {
        self.rctl.read() & 0xFFFCC3FF 
    }

    pub fn rctl_write(&mut self, value: u32) {
        self.rctl.write(value & 0x7EC0C3FE) 
    }

    pub fn tctl_read(&self) -> u32 {
        self.tctl.read() & 0x9FFFFFFF 
    }

    pub fn tctl_write(&mut self, value: u32) {
        self.tctl.write(value & 0xFFFFFFB) 
    }

    pub fn tipg_read(&self) -> u32 {
        self.tipg.read() & 0xFFFFFFFF 
    }

    pub fn tipg_write(&mut self, value: u32) {
        self.tipg.write(value & 0x3FFFFFFF) 
    }

    pub fn rdbal_read(&self) -> u32 {
        self.rdbal.read() & 0xFFFFFFFF 
    }

    pub fn rdbal_write(&mut self, value: u32) {
        self.rdbal.write(value & 0xFFFFFFF0) 
    }

    pub fn rdbah_read(&self) -> u32 {
        self.rdbah.read() & 0xFFFFFFFF 
    }

    pub fn rdbah_write(&mut self, value: u32) {
        self.rdbah.write(value & 0xFFFFFFFF) 
    }

    pub fn rdlen_read(&self) -> u32 {
        self.rdlen.read() & 0xFFFFFFFF 
    }

    pub fn rdlen_write(&mut self, value: u32) {
        self.rdlen.write(value & 0xFFF80) 
    }

    pub fn rdh_read(&self) -> u32 {
        self.rdh.read() & 0xFFFFFFFF 
    }

    pub fn rdh_write(&mut self, value: u32) {
        self.rdh.write(value & 0xFFFF) 
    }

    pub fn rdt_read(&self) -> u32 {
        self.rdt.read() & 0xFFFFFFFF 
    }

    pub fn rdt_write(&mut self, value: u32) {
        self.rdt.write(value & 0xFFFF) 
    }

    pub fn rdtr_read(&self) -> u32 {
        self.rdtr.read() & 0x7FFFFFFF 
    }

    pub fn rdtr_write(&mut self, value: u32) {
        self.rdtr.write(value & 0x8000FFFF) 
    }

    pub fn rxdctl_read(&self) -> u32 {
        self.rxdctl.read() & 0xFFFFFFFF 
    }

    pub fn rxdctl_write(&mut self, value: u32) {
        self.rxdctl.write(value & 0x13FFF3F) 
    }

    pub fn radv_read(&self) -> u32 {
        self.radv.read() & 0xFFFFFFFF 
    }

    pub fn radv_write(&mut self, value: u32) {
        self.radv.write(value & 0xFFFF) 
    }

    pub fn rsrpd_read(&self) -> u32 {
        self.rsrpd.read() & 0xFFFFFFFF 
    }

    pub fn rsrpd_write(&mut self, value: u32) {
        self.rsrpd.write(value & 0xFFF) 
    }

    pub fn tdbal_read(&self) -> u32 {
        self.tdbal.read() & 0xFFFFFFFF 
    }

    pub fn tdbal_write(&mut self, value: u32) {
        self.tdbal.write(value & 0xFFFFFFF0) 
    }

    pub fn tdbah_read(&self) -> u32 {
        self.tdbah.read() & 0xFFFFFFFF 
    }

    pub fn tdbah_write(&mut self, value: u32) {
        self.tdbah.write(value & 0xFFFFFFFF) 
    }

    pub fn tdlen_read(&self) -> u32 {
        self.tdlen.read() & 0xFFFFFFFF 
    }

    pub fn tdlen_write(&mut self, value: u32) {
        self.tdlen.write(value & 0xFFF80) 
    }

    pub fn tdh_read(&self) -> u32 {
        self.tdh.read() & 0xFFFFFFFF 
    }

    pub fn tdh_write(&mut self, value: u32) {
        self.tdh.write(value & 0xFFFF) 
    }

    pub fn tdt_read(&self) -> u32 {
        self.tdt.read() & 0xFFFFFFFF 
    }

    pub fn tdt_write(&mut self, value: u32) {
        self.tdt.write(value & 0xFFFF) 
    }

    pub fn crcerrs_read(&self) -> u32 {
        self.crcerrs.read() & 0xFFFFFFFF 
    }

    pub fn mta_read(&self) -> u32 {
        self.mta.read() & 0xFFFFFFFF 
    }

    pub fn mta_write(&mut self, value: u32) {
        self.mta.write(value & 0xFFFFFFFF) 
    }

}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum CtrlSpeed {
    Tenmbs = 0,
    Hundredmbs = 1,
    Thousandmbs = 2,
    Notused = 3,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusPhytype {
    Device00 = 0,
    Reserved01 = 1,
    Reserved10 = 10,
    Reserved11 = 11,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlDtyp {
    Legacyorextended = 0,
    Packetsplit = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlMo {
    Bits47to38 = 0,
    Bits46to37 = 1,
    Bits45to36 = 2,
    Bits43to34 = 3,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlBsize {
    Twothousandandfortyeight = 0,
    Onethousandandtwentyfour = 1,
    Fivetwelve = 2,
    Twofiftysix = 3,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum TctlRrthresh {
    Twolines = 0,
    Fourlines = 1,
    Eightlines = 2,
    Nothreshold = 3,
}
impl Registers {
    pub fn ctrl_speed_write(&mut self, value: CtrlSpeed) {
        self.ctrl.write((self.ctrl.read() & !0x300) | ((value as u32) << 8))
    }

    pub fn rctl_dtyp_write(&mut self, value: RctlDtyp) {
        self.rctl.write((self.rctl.read() & !0xC00) | ((value as u32) << 10))
    }

    pub fn rctl_mo_write(&mut self, value: RctlMo) {
        self.rctl.write((self.rctl.read() & !0x3000) | ((value as u32) << 12))
    }

    pub fn rctl_bsize_write(&mut self, value: RctlBsize) {
        self.rctl.write((self.rctl.read() & !0x30000) | ((value as u32) << 16))
    }

    pub fn tctl_rrthresh_write(&mut self, value: TctlRrthresh) {
        self.tctl.write((self.tctl.read() & !0x60000000) | ((value as u32) << 29))
    }

}
