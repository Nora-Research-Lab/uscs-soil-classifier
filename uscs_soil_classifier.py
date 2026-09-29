from typing import Tuple

def classify_soil(gravel: float, sand: float, fines: float,
                  ll: float, pl: float, cu: float, cc: float,
                  organic: bool) -> str:
    """
    Classify a soil according to ASTM D2487 (USCS) given basic index properties.
    Returns a string with the group symbol, group name, and description.
    """
    # Handle organic soil -> Peat (PT)
    if organic:
        return ("Group Symbol: PT\n"
                "Group Name: Peat\n"
                "Description: Highly organic soil, dark color, fibrous.")

    pi = ll - pl
    total_coarse = gravel + sand
    is_coarse_grained = total_coarse >= 50.0
    is_fine_grained = not is_coarse_grained

    # Convert to percentages of the coarse fraction for fine content
    fines_pct_of_total = fines
    # For coarse soils, classify based on fines %
    if is_coarse_grained:
        # Determine if gravel or sand dominates
        if gravel >= sand:
            prefix = 'G'  # Gravel
            suffix_non_fines = ''
        else:
            prefix = 'S'  # Sand
            suffix_non_fines = ''

        # Fines classification
        if fines_pct_of_total < 5.0:
            # Less than 5% fines: use gradation
            if cu >= 4.0 and (1.0 <= cc <= 3.0):
                grade = 'W'
                grade_name = 'well-graded'
            else:
                grade = 'P'
                grade_name = 'poorly graded'
            symbol = prefix + grade
            coarse_root = 'Gravel' if prefix == 'G' else 'Sand'
            name = f"{grade_name} {coarse_root}"
            desc = name
        elif fines_pct_of_total <= 12.0:
            # 5% to 12% fines: dual symbols based on gradation and plasticity
            # Determine gradation symbol
            if cu >= 4.0 and (1.0 <= cc <= 3.0):
                grade = 'W'
                grade_name = 'well-graded'
            else:
                grade = 'P'
                grade_name = 'poorly graded'
            # Determine fines type from plasticity
            if is_fine_grained is False:  # we are still in coarse logic
                # Actually we need to decide based on fines < 0.075 (fines) and LL/PI
                fines_type = _classify_fines_type(ll, pi)
                symbol = prefix + grade + '-' + fines_type
                coarse_root = 'Gravel' if prefix == 'G' else 'Sand'
                fines_desc = 'silt' if fines_type == 'M' else 'clay'
                if fines_type in ('ML', 'MH'):
                    fines_desc = 'silt'
                elif fines_type in ('CL', 'CH'):
                    fines_desc = 'clay'
                elif fines_type == 'OL':
                    fines_desc = 'organic silt'
                elif fines_type == 'OH':
                    fines_desc = 'organic clay'
                name = f"{grade_name} {coarse_root} with {fines_desc}"
                desc = name
            else:
                symbol = prefix + grade
                name = f"{grade_name} {coarse_root}"
                desc = name
        else:
            # >12% fines: classify as fine-grained
            fines_symbol = _classify_fines_type(ll, pi)
            coarse_root = 'Gravelly' if gravel >= sand else 'Sandy'
            name = f"{coarse_root} {fines_symbol}"
            # Get full name based on fines symbol
            fines_full = _fines_full_name(fines_symbol)
            if 'silt' in fines_full:
                if 'organic' in fines_full:
                    desc = f"{coarse_root} {fines_full}"
                else:
                    desc = f"{coarse_root} {fines_full}"
            else:
                desc = f"{coarse_root} {fines_full}"
            symbol = fines_symbol  # Actually in USCS, >12% fines the soil is fine-grained, but if gravel/sand dominate, the symbol remains coarse prefix? Wait: For coarse with >12% fines, the group name uses the fine-grained symbol, but the primary symbol is the coarse prefix? Standard: e.g., >12% fines, use the coarse prefix with fine suffix? Actually ASTM says: For coarse-grained soils with >12% fines, the group symbol is the coarse prefix plus the fine suffix (e.g., SM, SC, GM, GC). The fines fraction determines the suffix. So it's not just fines_symbol, but prefix+ suffix (like SM, not M). Let's correct:
            # Actually the correct symbol: prefix (G or S) followed by the fine-grained suffix (M for silt, C for clay). So:
            suffix = fines_symbol[-1]  # M or C (for low/high? Actually symbols can be ML, CL, etc. But for coarse suffix it's just M or C, no L/H distinction? In USCS, the suffix for coarse is based on plasticity: if PI > 7 and on or above A-line -> C; else if PI < 4 or below A-line -> M; else dual if borderline. We'll simplify: use the fines type from _classify_fines_type which returns 'CL','CH','ML','MH','OL','OH'. Then map to suffix: C for CL/CH, M for ML/MH, O for OL/OH? Actually for coarse soils, organic fines use 'O' suffix? The standard uses 'SO' and 'GO'? Actually there are group symbols like SM, SC, SP-SM, etc. For organic fine-grained, the fine suffix is O? No, organic fine-grained soils are OL, OH. When mixed with coarse, the symbol becomes coarse prefix + organic suffix? USCS does not have a separate symbol for organic coarse; if fines are organic, the classification still uses the fine-grained symbol (GC-GM, SC-SM). For simplicity, we will treat organic as separate and if organic is indicated we already returned PT. So organic fines not common.
            # We'll adopt: if fines >12%, decide if silt or clay based on plasticity chart.
            # Use _classify_fines_type which returns a two-letter symbol.
            fine_letter = fines_symbol[-1]  # L or H actually not needed; we need M or C for suffix.
            # Determine if silt (M) or clay (C) based on A-line.
            # We'll have a simpler approach: use the _classify_fines_type_symbol that returns just 'M' or 'C' for low/high? Actually USCS uses M for silt (low to high plasticity) and C for clay.
            # So we need a separate function: _fines_type_for_coarse.
    else:
        # Fine-grained soil (coarse < 50%)
        fines_symbol = _classify_fines_type(ll, pi)
        symbol = fines_symbol
        name = _fines_full_name(fines_symbol)
        desc = name

    # Build final output
    # For coarse with >12% fines, we drifted; let's restructure with clear logic
    # Redo: Separate logic for coarse and fine.

    # Reorganize function to be more linear:

    # Start fresh logic:
    # Determine if organic
    if organic:
        return ("Group Symbol: PT\n"
                "Group Name: Peat\n"
                "Description: Highly organic soil, dark color, fibrous.")

    pi = ll - pl
    total_coarse = gravel + sand
    fines_pct = fines

    # Calculate percentage of gravel in coarse fraction
    if total_coarse > 0:
        gravel_pct_of_coarse = gravel / total_coarse * 100
    else:
        gravel_pct_of_coarse = 0

    if total_coarse >= 50:
        # COARSE-GRAINED SOIL
        # Determine if gravelly or sandy
        if gravel_pct_of_coarse >= 50:
            main = 'G'
            main_name = 'Gravel'
            secondary_name = 'Sand'
        else:
            main = 'S'
            main_name = 'Sand'
            secondary_name = 'Gravel'

        # Fines content
        if fines_pct < 5:
            # Use gradation
            if main == 'G':
                if cu >= 4 and 1 <= cc <= 3:
                    symbol = 'GW'
                    name = 'Well-graded Gravel'
                else:
                    symbol = 'GP'
                    name = 'Poorly graded Gravel'
            else:
                if cu >= 6 and 1 <= cc <= 3:
                    symbol = 'SW'
                    name = 'Well-graded Sand'
                else:
                    symbol = 'SP'
                    name = 'Poorly graded Sand'
        elif 5 <= fines_pct <= 12:
            # Dual symbol: gradation + fines type
            # Determine gradation symbol for coarse
            if main == 'G':
                if cu >= 4 and 1 <= cc <= 3:
                    grade = 'W'
                else:
                    grade = 'P'
            else:
                if cu >= 6 and 1 <= cc <= 3:
                    grade = 'W'
                else:
                    grade = 'P'
            # Determine fines type (silt or clay)
            fines_type = _get_fines_type_coarse(ll, pi)
            symbol = main + grade + '-' + fines_type
            if fines_type == 'M':
                fines_label = 'silt'
            else:
                fines_label = 'clay'
            name = f"{'Well' if grade=='W' else 'Poorly'} graded {main_name} with {fines_label}"
        else:  # >12% fines
            # Classify as fine-grained soil, but retain coarse prefix
            fines_type = _get_fines_type_coarse(ll, pi)
            symbol = main + fines_type  # e.g., SM, SC, GM, GC
            if fines_type == 'M':
                fines_label = 'silt'
            else:
                fines_label = 'clay'
            name = f"{main_name} with {fines_label}"
    else:
        # FINE-GRAINED SOIL (total coarse < 50%)
        fines_type = _get_fines_type_fine(ll, pi)
        symbol = fines_type
        name = _fines_full_name(fines_type)

    # Add description
    if symbol in ('PT',):
        description = "Peat, highly organic"
    else:
        description = name

    return (f"Group Symbol: {symbol}\n"
            f"Group Name: {name}\n"
            f"Description: {description}")


# ---------- Helper functions ----------

def _get_fines_type_coarse(ll: float, pi: float) -> str:
    """Return 'M' for silt or 'C' for clay based on plasticity for coarse-grained soils."""
    # Use A-line: PI = 0.73*(LL-20)
    a_line_pi = 0.73 * (ll - 20)
    if ll < 50:
        if pi < 4 or (pi < a_line_pi):
            return 'M'  # silt
        else:
            return 'C'  # clay
    else:  # high plasticity
        if pi < a_line_pi:
            return 'M'  # silt
        else:
            return 'C'  # clay


def _get_fines_type_fine(ll: float, pi: float) -> str:
    """Return USCS symbol for fine-grained soil (e.g., CL, ML, CH, MH)."""
    a_line_pi = 0.73 * (ll - 20)
    if ll < 50:
        if pi < 4:
            return 'ML'
        elif pi < 7:  # 4 <= PI < 7 and on or above A-line -> CL, else ML
            if pi >= a_line_pi:
                return 'CL'
            else:
                return 'ML'
        else:  # PI >=7
            if pi >= a_line_pi:
                return 'CL'
            else:
                return 'ML'
    else:  # LL >= 50
        if pi >= a_line_pi:
            return 'CH'
        else:
            return 'MH'


def _fines_full_name(symbol: str) -> str:
    """Return full soil name from USCS fine-grained symbol."""
    mapping = {
        'ML': 'Silt (low plasticity)',
        'CL': 'Lean Clay (low plasticity)',
        'OL': 'Organic Silt (low plasticity)',
        'MH': 'Silt (high plasticity)',
        'CH': 'Fat Clay (high plasticity)',
        'OH': 'Organic Clay (high plasticity)',
        'PT': 'Peat'
    }
    return mapping.get(symbol, 'Unknown')
