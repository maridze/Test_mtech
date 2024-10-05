import streamlit as st
import pandas as pd

def data_upload_interface():
    """
    Создает интерфейс для загрузки CSV-файла с данными.

    Эта функция отображает заголовок страницы и виджет для загрузки файла.
    Если файл успешно загружен, она отображает первые несколько строк данных.

    Returns:
        pd.DataFrame или None: Загруженный датафрейм, если файл был успешно загружен,
                               в противном случае None.
    """
    st.title("Анализ больничных дней")
    uploaded_file = st.file_uploader("Загрузите файл с данными (CSV)", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        return df
    return None

def filter_data(df, work_days, group_type, age=None):
    """
    Фильтрует данные по количеству больничных дней и типу группы (пол или возраст).
    
    Аргументы:
    df (pd.DataFrame): Датафрейм с данными.
    work_days (int): Порог количества рабочих дней для фильтрации.
    group_type (str): Тип группы для анализа ('sex' или 'age').
    age (int): Возраст, используемый для разделения на молодых и взрослых (только если group_type='age').
    
    Возвращает:
    pd.DataFrame: Отфильтрованный датафрейм.
    pd.Series: Дни больничных для группы 1.
    pd.Series: Дни больничных для группы 2.
    str: Метка для группы 1.
    str: Метка для группы 2.
    """
    df_filtered = df[df['Количество больничных дней'] > work_days].copy()
    
    if group_type == 'sex':
        group1_days = df_filtered[df_filtered['Пол'] == 'М']['Количество больничных дней']
        group2_days = df_filtered[df_filtered['Пол'] == 'Ж']['Количество больничных дней']
        group1_label = 'Мужчины'
        group2_label = 'Женщины'
        
    elif group_type == 'age':
        if age is None:
            raise ValueError("Для анализа по возрасту необходимо указать параметр 'age'.")
        
        df_filtered.loc[:, 'Возрастная группа'] = df_filtered['Возраст'].apply(lambda x: 'Взрослые' if x > age else 'Молодые')
        group1_days = df_filtered[df_filtered['Возрастная группа'] == 'Взрослые']['Количество больничных дней']
        group2_days = df_filtered[df_filtered['Возрастная группа'] == 'Молодые']['Количество больничных дней']
        group1_label = 'Взрослые'
        group2_label = 'Молодые'
    
    else:
        raise ValueError("group_type должен быть 'sex' или 'age'.")
    
    return df_filtered, group1_days, group2_days, group1_label, group2_label
