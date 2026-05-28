"""Модуль для очистки и нормализации данных."""

from typing import Union, Dict, List
import pandas as pd

# Словарь синонимов для propertyType
PROPERTY_SYNONYMS: Dict[str, str] = {
    'mobile': 'manufactured',
    'mobile home': 'manufactured',
    'mo2le': 'manufactured',
    'mo2 le': 'manufactured',
    'prefab': 'manufactured',
    'modular': 'manufactured',
    'manufactured': 'manufactured',
    'manufactured home': 'manufactured',
    'cabin': 'cabin',
    'ca2n': 'cabin',
    'ca2 n': 'cabin',
    'midcentury': 'mid-century',
    'mid century': 'mid-century',
    'mid-century modern': 'mid-century',
    'single family': 'single-family',
    'single-family home': 'single-family',
    'single family home': 'single-family',
    'single-family residential': 'single-family',
    'sfr': 'single-family',
    'detached': 'single-family',
    'townhome': 'townhouse',
    'town house': 'townhouse',
    'townhome/townhouse': 'townhouse',
    'condo': 'condo',
    'condominium': 'condo',
    'apartment': 'apartment',
    'co-op': 'co-op',
    'cooperative': 'co-op',
    'ranch': 'ranch',
    'craftsman': 'craftsman',
    'victorian': 'victorian',
    'colonial': 'colonial',
    'contemporary': 'contemporary',
    'cottage': 'cottage',
    'farmhouse': 'farmhouse',
    'tudor': 'tudor',
    'log home': 'log home'
}

# Группировка статусов
STATUS_GROUPS: Dict[str, List[str]] = {
    'active': [
        'active', 'activated', 'active with contract', 'active with offer',
        'active auction', 'auction active', 'for sale'
    ],
    'under_contract': [
        'under contract', 'under contract showing', 'under contract show',
        'active under contract', 'under contract backups', 'active backup',
        'backup contract', 'pending escape clause', 'pending backup wanted',
        'pending take backups', 'pending continue show'
    ],
    'contingency': [
        'contingency', 'contingency contract', 'active contingency',
        'insp inspection contingency'
    ],
    'pending': ['pending', 'pending inspection', 'due diligence period'],
    'foreclosed': [
        'foreclosed', 'foreclosure', 'pre foreclosure', 'pre foreclosure auction'
    ],
    'sold': ['sold', 'closed']
}


def normalize_property_type(property_type: Union[str, float]) -> Union[str, None]:
    """
    Нормализует тип недвижимости по словарю синонимов.

    Parameters
    ----------
    property_type : str or float
        Исходное значение типа недвижимости.

    Returns
    -------
    str or None
        Нормализованное значение или None при ошибке.
    """
    if pd.isna(property_type):
        return None

    type_str = str(property_type).lower().strip()

    # Прямое попадание
    if type_str in PROPERTY_SYNONYMS:
        return PROPERTY_SYNONYMS[type_str]

    # Поиск по ключевым словам
    for key, value in PROPERTY_SYNONYMS.items():
        if key in type_str:
            return value

    return type_str


def normalize_status(status: Union[str, float]) -> Union[str, None]:
    """
    Нормализует статус продажи по словарю групп.

    Parameters
    ----------
    status : str or float
        Исходное значение статуса.

    Returns
    -------
    str or None
        Группа статуса или None при ошибке.
    """
    if pd.isna(status):
        return None

    status_str = str(status).lower().strip()

    for group, keywords in STATUS_GROUPS.items():
        for keyword in keywords:
            if keyword in status_str:
                return group

    return 'other'


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """
    Безопасное преобразование серии в числовой тип.

    Parameters
    ----------
    series : pd.Series
        Входная серия данных.

    Returns
    -------
    pd.Series
        Серия с числовыми значениями (ошибки преобразования -> NaN).
    """
    return pd.to_numeric(series, errors='coerce')


def remove_outliers(
    dataframe: pd.DataFrame,
    column: str,
    lower_quantile: float = 0.01,
    upper_quantile: float = 0.99
) -> pd.DataFrame:
    """
    Удаляет выбросы по указанному столбцу на основе квантилей.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Исходный DataFrame.
    column : str
        Название колонки для фильтрации.
    lower_quantile : float
        Нижний квантиль (по умолчанию 0.01).
    upper_quantile : float
        Верхний квантиль (по умолчанию 0.99).

    Returns
    -------
    pd.DataFrame
        DataFrame без выбросов.
    """
    lower = dataframe[column].quantile(lower_quantile)
    upper = dataframe[column].quantile(upper_quantile)

    before_count = len(dataframe)
    filtered_df = dataframe[
        (dataframe[column] >= lower) & (dataframe[column] <= upper)
    ]
    after_count = len(filtered_df)

    print(f"  {column}: удалено {before_count - after_count} строк "
          f"({before_count} -> {after_count})")

    return filtered_df
