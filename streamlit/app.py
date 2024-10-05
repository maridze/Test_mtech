import streamlit as st
from data_processing import data_upload_interface, filter_data
from stat_test import perform_statistical_test
from visualization import print_results, visualize_data
from utils import analysis_parameters_interface, sidebar_description

def test_sick_days_hypothesis(df, work_days, group_type, age=None):
    """
    Проводит анализ гипотезы о различиях в количестве больничных дней между группами.

    Args:
        df (pd.DataFrame): Исходный датафрейм с данными.
        work_days (int): Минимальное количество рабочих дней для включения в анализ.
        group_type (str): Тип группировки ('sex' или 'age').
        age (int, optional): Пороговое значение возраста для группировки по возрасту. По умолчанию None.

    """
    df_filtered, group1_days, group2_days, group1_label, group2_label = filter_data(df, work_days, group_type, age)
    test_used, stat, p_value, additional_info = perform_statistical_test(group1_days, group2_days)
    
    print_results(test_used, stat, p_value, group1_label, group2_label, additional_info)
    
    visualize_data(df_filtered, group1_days, group2_days, group1_label, group2_label, group_type)

def main():
    """
    Основная функция приложения Streamlit.

    Управляет потоком выполнения приложения, включая загрузку данных,
    выбор параметров анализа и запуск анализа гипотезы.

    """
    df = data_upload_interface()
    
    if df is not None:
        work_days, group_type, age = analysis_parameters_interface()
        
        if st.button("Запустить анализ"):
            if group_type in ['sex', 'age']:
                st.info(f"Анализ по {group_type}. Порог рабочих дней: {work_days}.")
                
                try:
                    test_sick_days_hypothesis(df, work_days, group_type, age)
                except Exception as e:
                    st.error(f"Произошла ошибка при выполнении анализа: {e}")
            else:
                st.warning("Выберите правильный тип анализа (пол или возраст).")

if __name__ == "__main__":
    sidebar_description()
    main()