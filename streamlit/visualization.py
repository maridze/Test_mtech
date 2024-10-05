import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def print_results(test_used, stat, p_value, group1_label, group2_label, additional_info):
    """
    Выводит результаты статистического теста в красивом формате.

    Аргументы:
    test_used (str): Название использованного статистического теста.
    stat (float): Значение статистики теста.
    p_value (float): P-значение теста.
    group1_label (str): Метка первой группы.
    group2_label (str): Метка второй группы.
    additional_info (dict): Дополнительная информация о промежуточных тестах (Шапиро-Уилка и Левена).

    """
    st.subheader("Результаты статистического анализа")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Использованный тест", test_used)
        st.metric("Значение статистики", f"{stat:.4f}")
    
    with col2:
        st.metric("P-значение", f"{p_value:.4f}")
        
        if p_value < 0.05:
            st.success("Результат: Статистически значимая разница")
        else:
            st.info("Результат: Статистически значимой разницы не обнаружено")

    st.write(f"Сравнение групп: {group1_label} vs {group2_label}")

    if "t-test" in test_used:
        st.write(f"""
        **Нулевая гипотеза (H₀):** Среднее количество больничных дней в группе "{group1_label}" меньше или равно среднему количеству больничных дней в группе "{group2_label}".
        
        **Альтернативная гипотеза (H₁):** Среднее количество больничных дней в группе "{group1_label}" больше, чем в группе "{group2_label}".
        """)
    elif "Mann-Whitney" in test_used:
        st.write(f"""
        **Нулевая гипотеза (H₀):** Распределение количества больничных дней в группе "{group1_label}" не смещено вправо относительно распределения в группе "{group2_label}".
        
        **Альтернативная гипотеза (H₁):** Распределение количества больничных дней в группе "{group1_label}" смещено вправо относительно распределения в группе "{group2_label}".
        """)
    
    interpretation = f"""
    **Интерпретация результатов:**
    
    - Если p-значение < 0.05, мы отвергаем нулевую гипотезу. 
      Это означает, что есть статистически значимая разница между {group1_label} и {group2_label}.
    
    - Если p-значение ≥ 0.05, мы не можем отвергнуть нулевую гипотезу. 
      Это означает, что нет достаточных доказательств статистически значимой разницы между {group1_label} и {group2_label}.
    
    Текущий результат: {"Есть" if p_value < 0.05 else "Нет"} статистически значимой разницы между группами.
    """
    
    st.markdown(interpretation)
    st.subheader("Дополнительная информация о тесте:")
    st.write(f"""
    Использованный тест: {test_used}
    
    Результаты промежуточных тестов:
    - Тест Шапиро-Уилка для группы "{group1_label}": p-значение = {additional_info['shapiro_group1']:.4f}
    - Тест Шапиро-Уилка для группы "{group2_label}": p-значение = {additional_info['shapiro_group2']:.4f}
    """)
    
    if additional_info['levene_p'] is not None:
        st.write(f"- Тест Левена: p-значение = {additional_info['levene_p']:.4f}")
    
    st.write("""
    Логика выбора теста:
    - Если данные в обеих группах нормально распределены (p > 0.05 для теста Шапиро-Уилка) и имеют равные дисперсии (p > 0.05 для теста Левена), используется t-тест для независимых выборок.
    - Если данные нормально распределены, но дисперсии неравны, используется тест Уэлча (модификация t-теста).
    - Если данные не нормально распределены, используется U-тест Манна-Уитни.
    
    Все тесты проводятся с односторонней альтернативой (группа 1 > группа 2).
    """)

def visualize_data(df_filtered, group1_days, group2_days, group1_label, group2_label, group_type):
    """
    Создает визуализации данных для дашборда.

    Аргументы:
    df_filtered (pd.DataFrame): Отфильтрованный датафрейм с данными.
    group1_days (pd.Series): Данные о больничных днях для первой группы.
    group2_days (pd.Series): Данные о больничных днях для второй группы.
    group1_label (str): Метка первой группы (например, 'Мужчины' или 'Взрослые').
    group2_label (str): Метка второй группы (например, 'Женщины' или 'Молодые').
    group_type (str): Тип группы для анализа ('sex' или 'age').

    """

    st.subheader("Визуализация данных")
    
    # Boxplot
    st.subheader("Boxplot количества больничных дней")
    fig_box, ax_box = plt.subplots(figsize=(10, 6))
    if group_type == 'sex':
        sns.boxplot(x='Пол', y='Количество больничных дней', data=df_filtered, ax=ax_box)
    elif group_type == 'age':
        sns.boxplot(x='Возрастная группа', y='Количество больничных дней', data=df_filtered, ax=ax_box)
    ax_box.set_title("Распределение больничных дней по группам")
    ax_box.set_xlabel("Группа")
    ax_box.set_ylabel("Количество больничных дней")
    st.pyplot(fig_box)

    # KDE plot
    st.subheader("Распределение количества больничных дней")
    fig_kde, ax_kde = plt.subplots(figsize=(10, 6))
    sns.kdeplot(group1_days, label=group1_label, fill=True, alpha=0.5, ax=ax_kde)
    sns.kdeplot(group2_days, label=group2_label, fill=True, alpha=0.5, ax=ax_kde)
    ax_kde.set_title("Распределение больничных дней")
    ax_kde.set_xlabel("Количество больничных дней")
    ax_kde.set_ylabel("Плотность")
    ax_kde.legend()
    st.pyplot(fig_kde)