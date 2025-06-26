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
    _padding4: [u8; 9212], // 0x2800 - 0x404
    rdbal: Volatile<u32>, //0x2800
    rdbah: Volatile<u32>, //0x2804
    rdlen: Volatile<u32>, //0x2808
    _padding5: [u8; 4], // 0x2810 - 0x280C
    rdh: Volatile<u32>, //0x2810
    _padding6: [u8; 4], // 0x2818 - 0x2814
    rdt: Volatile<u32>, //0x2818
    _padding7: [u8; 4068], // 0x3800 - 0x281C
    tdbal: Volatile<u32>, //0x3800
    tdbah: Volatile<u32>, //0x3804
    tdlen: Volatile<u32>, //0x3808
    _padding8: [u8; 4], // 0x3810 - 0x380C
    tdh: Volatile<u32>, //0x3810
    _padding9: [u8; 4], // 0x3818 - 0x3814
    tdt: Volatile<u32>, //0x3818
}
impl Registers {
    pub fn ctrl_read(&self) -> u32 {
        self.ctrl.read() && 0xFDFFFEFF 
    }

    pub fn ctrl_write(&mut self, value: u32) {
        self.ctrl.write(value && 0xDD031E05) 
    }

    pub fn status_read(&self) -> u32 {
        self.status.read() && 0xFFFFFFFF 
    }

    pub fn status_write(&mut self, value: u32) {
        self.status.write(value && 0x0) 
    }

    pub fn ims_read(&self) -> u32 {
        self.ims.read() && 0x787FFF 
    }

    pub fn ims_write(&mut self, value: u32) {
        self.ims.write(value && 0x4057F7) 
    }

    pub fn rctl_read(&self) -> u32 {
        self.rctl.read() && 0xFFFFFFFF 
    }

    pub fn rctl_write(&mut self, value: u32) {
        self.rctl.write(value && 0x7EDFF67E) 
    }

    pub fn tctl_read(&self) -> u32 {
        self.tctl.read() && 0xF5E0180F 
    }

    pub fn tctl_write(&mut self, value: u32) {
        self.tctl.write(value && 0x65E0180B) 
    }

    pub fn rdbal_read(&self) -> u32 {
        self.rdbal.read() && 0xFFFFFFF0 
    }

    pub fn rdbal_write(&mut self, value: u32) {
        self.rdbal.write(value && 0xFFFFFFF0) 
    }

    pub fn rdbah_read(&self) -> u32 {
        self.rdbah.read() && 0xFFFFFFFF 
    }

    pub fn rdbah_write(&mut self, value: u32) {
        self.rdbah.write(value && 0xFFFFFFFF) 
    }

    pub fn rdlen_read(&self) -> u32 {
        self.rdlen.read() && 0xFFF80 
    }

    pub fn rdlen_write(&mut self, value: u32) {
        self.rdlen.write(value && 0xFFF80) 
    }

    pub fn rdh_read(&self) -> u32 {
        self.rdh.read() && 0xFFFF 
    }

    pub fn rdh_write(&mut self, value: u32) {
        self.rdh.write(value && 0xFFFF) 
    }

    pub fn rdt_read(&self) -> u32 {
        self.rdt.read() && 0xFFFF 
    }

    pub fn rdt_write(&mut self, value: u32) {
        self.rdt.write(value && 0xFFFF) 
    }

    pub fn tdbal_read(&self) -> u32 {
        self.tdbal.read() && 0xFFFFFFF0 
    }

    pub fn tdbal_write(&mut self, value: u32) {
        self.tdbal.write(value && 0xFFFFFFF0) 
    }

    pub fn tdbah_read(&self) -> u32 {
        self.tdbah.read() && 0xFFFFFFFF 
    }

    pub fn tdbah_write(&mut self, value: u32) {
        self.tdbah.write(value && 0xFFFFFFFF) 
    }

    pub fn tdlen_read(&self) -> u32 {
        self.tdlen.read() && 0xFFF80 
    }

    pub fn tdlen_write(&mut self, value: u32) {
        self.tdlen.write(value && 0xFFF80) 
    }

    pub fn tdh_read(&self) -> u32 {
        self.tdh.read() && 0xFFFF 
    }

    pub fn tdh_write(&mut self, value: u32) {
        self.tdh.write(value && 0xFFFF) 
    }

    pub fn tdt_read(&self) -> u32 {
        self.tdt.read() && 0xFFFF 
    }

    pub fn tdt_write(&mut self, value: u32) {
        self.tdt.write(value && 0xFFFF) 
    }

}
