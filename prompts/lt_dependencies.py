from pydantic import BaseModel

def lt_dependencies(dependencies_json):
    """ Prompt for extracting per-register section headers """

    prompt = f"""
       Given a file of JSON entries of dependee and dependent registers, look at the relevant sentence and assess if the dependency is an ordering dependency that can be encoded using linear types.
       With linear type, you can encode ordering by making the return of one function the argument of another, ensuring the previous function has to be run first.
       You can query the datasheet to understand more about each register.

       Here is an example of Rust code outline using linear types RxCtrlDisabled and FilterCtrlSet to enforce an ordering between rxctrl and fctrl registers:
       As fctrl can only be set when rxctrl is disabled, it consumes a linear type that is only created by rxctrl_disable.
       ``` 
        pub struct RxCtrlDisabled(());
        pub struct FilterCtrlSet(())

        pub fn rxctrl_rx_disable(&mut self) -> RxCtrlDisabled;
        pub fn fctrl_write(&mut self, val: FilterCtrlFlags, rx_disabled: RxCtrlDisabled) -> FilterCtrlSet;
        pub fn rxctrl_rx_enable(&mut self, fctrl_set: FilterCtrlSet)
       ```
       Return the list of JSON objects with two extra fields at the end. One which categorizes the dependency as a linear type enforceable or not, and the next which gives an explanation for the classification.
       Each json object should be in one line with correcr formatting. There should be no outher text in the output
       The list is: : {dependencies_json}
    """
    return prompt


def lt_dependency(dependency_json, vs_info):
    """ Prompt for extracting per-register section headers """

    prompt = f"""
       Given a JSON entry of a dependee and dependent register, look at the relevant sentence and assess if the dependency is an ordering dependency that can be encoded using linear types.
       With linear types, you can encode ordering by making the return of one function the argument of another, ensuring the previous function has to be run first.

       Here is an example of Rust code outline using linear types: 
       {examples[0]},

       Another example:
       {examples[1]}

       Return the JSON object with two extra fields at the end. One which categorizes the dependency as a linear type enforceable or not, and the next which gives an explanation for the classification.
       It should be in one line. There should be no outher text in the output
       Related information from the datasheet is: {vs_info}.
       The object is: {dependency_json}
    """
    return prompt


linear_types_in_rust = "Linear types"

examples = [
      {
         "dependency": "As fctrl can only be set when rxctrl is disabled, it consumes a linear type RxCtrlDisabled that is only created by rxctrl_disable. It then returns FilterCtrlSet which is used to enable rxctrl",
         "code outline": """
            pub struct RxCtrlDisabled(());
            pub struct FilterCtrlSet(());

            pub fn rxctrl_rx_disable(&mut self) -> RxCtrlDisabled;
            pub fn fctrl_write(&mut self, val: FilterCtrlFlags, rx_disabled: RxCtrlDisabled) -> FilterCtrlSet;
            pub fn rxctrl_rx_enable(&mut self, fctrl_set: FilterCtrlSet)
         """
      },
      {
         "dependency": "MTQC can only be programmed when RTTDCS.ARBDIS is set.",
         "code outline": """
            pub struct ARBDISSet();

            pub fn rttdcs_set_arbdis(&mut self) -> ARBDISSet;
            pub fn mtqc_write(&mut self, val: u8, _arbdis_set: ARBDISSet)
         """
      },
]


# {
#    "dependency": "Software should not set the descriptor RS bit when TXDCTL.WTHRESH is greater than zero",
#    "code outline": """
#       pub struct ReportStatusBit(u64);

#       pub fn txdctl_write_wthresh(&mut self, wthresh: U7) -> ReportStatusBit {
#          let val = self.txdctl.read() & !0x7F_0000;
#          self.txdctl.write(val | ((wthresh.bits() as u32) << 16));

#          if wthresh.bits() > 0 {
#                ReportStatusBit::zero()
#          } else { // if wthresh is set to zero then we should set the RS bit in the descriptor
#                ReportStatusBit::one()
#          }
#       }
#    """
# }
