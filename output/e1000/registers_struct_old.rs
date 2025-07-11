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
        self.ctrl.read() && 0x7DFFFCFE 
    }

    pub fn ctrl_write(&mut self, value: u32) {
        self.ctrl.write(value && 0x5D031C04) 
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
        self.rctl.read() && 0xA7FFFDFF 
    }

    pub fn rctl_write(&mut self, value: u32) {
        self.rctl.write(value && 0x26DFE47E) 
    }

    pub fn tctl_read(&self) -> u32 {
        self.tctl.read() && 0x94A01805 
    }

    pub fn tctl_write(&mut self, value: u32) {
        self.tctl.write(value && 0x4A01801) 
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
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum CtrlFd {
    HalfDuplex = 0,
    FullDuplex = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum CtrlSpeed {
    10mbS = 00b,
    100mbS = 01b,
    1000mbS = 10b,
    NotUsed = 11b,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum CtrlLcdRst {
    Normal = 0,
    ResetToPhyIsAsserted = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusFd {
    X = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusLu {
    X = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusPhytype {
    82579 = 00,
    Reserved = 01,
    Reserved = 10,
    Reserved = 11,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusTxoff {
    X = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusPhypwr {
    0 = ThePhyIsPoweredOnInTheActiveState,
    1 = ThePhyIsInThePowerDownState,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusSpeed {
    10mbS = 00,
    100mbS = 01,
    1000mbS = 10,
    1000mbS = 11,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusMasterReadCompletionsBlocked {
    X = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusLanInitDone {
    0 = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusPhyra {
    X = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusMasterEnableStatus {
    1 = Na,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum StatusClkCnt14 {
    1 = ,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlSpeed {
    00 = 10mbS,
    01 = 100mbS,
    10 = 1000mbS,
    11 = NotUsed,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlFrcspd {
    Frcspd = 0,
    Frcspd = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlFrcdplx {
    Frcdplx = 0,
    Frcdplx = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlLcdpd {
    Lcdpd = 0,
    Lcdpd = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlRfce {
    Rfce = 0,
    Rfce = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlTfce {
    Tfce = 0,
    Tfce = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlVme {
    Vme = 0,
    Vme = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RctlLcdRst {
    LcdRst = 0,
    LcdRst = 1,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum TctlEnable {
    0 = DisableTransmitter,
    1 = EnableTransmitter,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum TctlPadShortPackets {
    0 = DoNotPad,
    1 = Pad,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum TctlSoftwareXoffTransmission {
    0 = NoXoff,
    1 = TransmitXoff,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum TctlReTransmitOnLateCollision {
    0 = DonTRetransmit,
    1 = Retransmit,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum TctlReadRequestThreshold {
    00 = 2Lines,
    01 = 4Lines,
    10 = 8Lines,
    11 = NoThreshold,
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum RdbalRdbal {
    Reserved = 0,
}
impl Registers {
    pub fn ctrl_fd_write(&mut self, value: CtrlFd) {
        self.ctrl.write(value as u32) 
    }

    pub fn ctrl_speed_write(&mut self, value: CtrlSpeed) {
        self.ctrl.write(value as u32) 
    }

    pub fn ctrl_lcd_rst_write(&mut self, value: CtrlLcdRst) {
        self.ctrl.write(value as u32) 
    }

    pub fn status_fd_write(&mut self, value: StatusFd) {
        self.status.write(value as u32) 
    }

    pub fn status_lu_write(&mut self, value: StatusLu) {
        self.status.write(value as u32) 
    }

    pub fn status_phytype_write(&mut self, value: StatusPhytype) {
        self.status.write(value as u32) 
    }

    pub fn status_txoff_write(&mut self, value: StatusTxoff) {
        self.status.write(value as u32) 
    }

    pub fn status_phypwr_write(&mut self, value: StatusPhypwr) {
        self.status.write(value as u32) 
    }

    pub fn status_speed_write(&mut self, value: StatusSpeed) {
        self.status.write(value as u32) 
    }

    pub fn status_master_read_completions_blocked_write(&mut self, value: StatusMasterReadCompletionsBlocked) {
        self.status.write(value as u32) 
    }

    pub fn status_lan_init_done_write(&mut self, value: StatusLanInitDone) {
        self.status.write(value as u32) 
    }

    pub fn status_phyra_write(&mut self, value: StatusPhyra) {
        self.status.write(value as u32) 
    }

    pub fn status_master_enable_status_write(&mut self, value: StatusMasterEnableStatus) {
        self.status.write(value as u32) 
    }

    pub fn status_clk_cnt_1_4_write(&mut self, value: StatusClkCnt14) {
        self.status.write(value as u32) 
    }

    pub fn rctl_speed_write(&mut self, value: RctlSpeed) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_frcspd_write(&mut self, value: RctlFrcspd) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_frcdplx_write(&mut self, value: RctlFrcdplx) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_lcdpd_write(&mut self, value: RctlLcdpd) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_rfce_write(&mut self, value: RctlRfce) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_tfce_write(&mut self, value: RctlTfce) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_vme_write(&mut self, value: RctlVme) {
        self.rctl.write(value as u32) 
    }

    pub fn rctl_lcd_rst_write(&mut self, value: RctlLcdRst) {
        self.rctl.write(value as u32) 
    }

    pub fn tctl_enable_write(&mut self, value: TctlEnable) {
        self.tctl.write(value as u32) 
    }

    pub fn tctl_pad_short_packets_write(&mut self, value: TctlPadShortPackets) {
        self.tctl.write(value as u32) 
    }

    pub fn tctl_software_xoff_transmission_write(&mut self, value: TctlSoftwareXoffTransmission) {
        self.tctl.write(value as u32) 
    }

    pub fn tctl_re_transmit_on_late_collision_write(&mut self, value: TctlReTransmitOnLateCollision) {
        self.tctl.write(value as u32) 
    }

    pub fn tctl_read_request_threshold_write(&mut self, value: TctlReadRequestThreshold) {
        self.tctl.write(value as u32) 
    }

    pub fn rdbal_rdbal_write(&mut self, value: RdbalRdbal) {
        self.rdbal.write(value as u32) 
    }

}
