import re

def guardrail_overlapping_masks(ro: int, wo: int, rw: int, reg_name: str = "UNKNOWN"):
    """
    Guardrail: Ensure RO, WO, and RW masks do not overlap.
    If any overlap, print a warning and clear the overlap from WO and RW masks (RO takes precedence).
    Returns possibly updated (wo, rw).
    """
    overlap_wo = ro & wo
    overlap_rw = ro & rw
    if overlap_wo or overlap_rw:
        print(f"Warning: Register '{reg_name}' has overlapping RO/WO or RO/RW mask bits. "
              f"RO mask: 0x{ro:X}, WO mask: 0x{wo:X}, RW mask: 0x{rw:X}. "
              f"Overlapping bits: 0x{(overlap_wo | overlap_rw):X}. Removing overlap from WO and RW masks.")
        if overlap_wo:
            wo = wo & ~ro
        if overlap_rw:
            rw = rw & ~ro
    return wo, rw

def guardrail_valid_bitrange(s: str, reg_name: str = "UNKNOWN", subfield_name: str = "UNKNOWN") -> bool:
    """
    Guardrail: Ensure bitrange is either a number or in the form x:y or x-y or x,y
    """
    s = s.strip()
    # Fix regex to allow single numbers or two numbers separated by :, -, or ,
    ret = bool(re.fullmatch(r"\d+([:\-,]\d+)?", s))
    if not ret:
        print(f"Warning: Invalid bit range for register '{reg_name}', subfield '{subfield_name}', not a digit or in the form x:y or x-y or x,y: {s}")
    
    return ret


    