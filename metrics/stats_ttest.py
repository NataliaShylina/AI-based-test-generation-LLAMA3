from scipy.stats import ttest_ind, f_oneway
import numpy as np


def run_ttest(ai_basic, ai_adv, mbt):
    """
    Inputs:
    - ai_basic = list of test counts per run
    - ai_adv = list of test counts per run
    - mbt = list of test counts per run
    """

    results = {}

    # =========================
    # pairwise t-tests
    # =========================
    results["AI_BASIC_vs_AI_ADV"] = ttest_ind(ai_basic, ai_adv, equal_var=False)
    results["AI_BASIC_vs_MBT"] = ttest_ind(ai_basic, mbt, equal_var=False)
    results["AI_ADV_vs_MBT"] = ttest_ind(ai_adv, mbt, equal_var=False)

    # =========================
    # ANOVA (global difference)
    # =========================
    results["ANOVA"] = f_oneway(ai_basic, ai_adv, mbt)

    # =========================
    # summary stats
    # =========================
    results["summary"] = {
        "AI_BASIC_mean": float(np.mean(ai_basic)),
        "AI_ADV_mean": float(np.mean(ai_adv)),
        "MBT_mean": float(np.mean(mbt)),
        "AI_BASIC_std": float(np.std(ai_basic)),
        "AI_ADV_std": float(np.std(ai_adv)),
        "MBT_std": float(np.std(mbt)),
    }

    return results