from scipy.stats import shapiro, ttest_ind, mannwhitneyu, levene

def perform_statistical_test(group1_days, group2_days):
    """
    Выполняет статистические тесты для сравнения двух групп.
    
    Аргументы:
    group1_days (pd.Series): Дни больничных для группы 1.
    group2_days (pd.Series): Дни больничных для группы 2.
    
    Возвращает:
    str: Название использованного теста.
    float: Статистика теста.
    float: p-значение теста.
    """
    shapiro_group1 = shapiro(group1_days)
    shapiro_group2 = shapiro(group2_days)
    
    additional_info = {
        "shapiro_group1": shapiro_group1.pvalue,
        "shapiro_group2": shapiro_group2.pvalue,
        "levene_p": None
    }

    if shapiro_group1.pvalue > 0.05 and shapiro_group2.pvalue > 0.05:
        levene_stat, levene_p = levene(group1_days, group2_days)
        additional_info["levene_p"] = levene_p

        if levene_p > 0.05:
            stat, p_value = ttest_ind(group1_days, group2_days, alternative='greater', equal_var=True)
            test_used = "t-test (equal variances)"
        else:
            stat, p_value = ttest_ind(group1_days, group2_days, alternative='greater', equal_var=False)
            test_used = "Welch's t-test (unequal variances)"
    else:
        stat, p_value = mannwhitneyu(group1_days, group2_days, alternative='greater')
        test_used = "Mann-Whitney U test"

    return test_used, stat, p_value, additional_info
