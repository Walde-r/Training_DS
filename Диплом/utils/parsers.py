"""Модуль для парсинга сложных полей homeFacts и schools."""

import re
import ast
from typing import Dict, Any, Union
import pandas as pd
import numpy as np


def _safe_float_conversion(value: Any, default: float = np.nan) -> float:
    """
    Безопасное преобразование в float.

    Parameters
    ----------
    value : Any
        Значение для преобразования.
    default : float
        Значение по умолчанию при ошибке.

    Returns
    -------
    float
        Преобразованное значение или default.
    """
    try:
        if value and not pd.isna(value):
            return float(value)
        return default
    except (ValueError, TypeError):
        return default


def _parse_price_per_sqft(value: Any) -> float:
    """
    Парсит значение Price/sqft, убирая $ и запятые.

    Parameters
    ----------
    value : Any
        Значение цены за квадратный фут.

    Returns
    -------
    float
        Числовое значение или NaN.
    """
    if not value or pd.isna(value) or not isinstance(value, str):
        return np.nan
    try:
        cleaned = value.replace('$', '').replace(',', '')
        return float(cleaned)
    except (ValueError, TypeError):
        return np.nan


def _extract_fact_value(fact: dict) -> tuple:
    """
    Извлекает label и value из одного fact.

    Parameters
    ----------
    fact : dict
        Один элемент списка atAGlanceFacts.

    Returns
    -------
    tuple
        (label, value) где label - str, value - Any.
    """
    label = fact.get('factLabel', '')
    value = fact.get('factValue', '')
    return label, value


def parse_homefacts(hf_str: Union[str, float]) -> Dict[str, Any]:
    """
    Извлекает полезные признаки из homeFacts.

    Parameters
    ----------
    hf_str : str or float
        Строка с данными homeFacts или NaN.

    Returns
    -------
    dict
        Словарь с извлеченными признаками.
    """
    # Проверка на пустые значения
    if pd.isna(hf_str) or hf_str == '' or hf_str == '{}':
        return {}

    try:
        # Парсинг строки в словарь
        if isinstance(hf_str, str):
            hf_dict = ast.literal_eval(hf_str)
        else:
            hf_dict = hf_str

        result: Dict[str, Any] = {}
        facts = hf_dict.get('atAGlanceFacts', [])

        for fact in facts:
            label, value = _extract_fact_value(fact)

            # Обработка по типу поля
            if label == 'Year built':
                result['year_built'] = _safe_float_conversion(value)

            elif label == 'Price/sqft':
                result['price_per_sqft'] = _parse_price_per_sqft(value)

            elif label == 'Heating':
                result['heating'] = value if value else np.nan

            elif label == 'Parking':
                result['parking'] = value if value else np.nan

            elif label == 'lotsize':
                result['lot_size'] = _safe_float_conversion(value)

        return result

    except (SyntaxError, ValueError, TypeError):
        return {}


def _extract_ratings_from_school(item: dict) -> list:
    """
    Извлекает рейтинги школ из одного элемента.

    Parameters
    ----------
    item : dict
        Элемент списка школ.

    Returns
    -------
    list
        Список числовых рейтингов.
    """
    ratings = []
    rating_list = item.get('rating', [])
    for rating_value in rating_list:
        if rating_value and rating_value != 'NR':
            try:
                ratings.append(float(rating_value))
            except (ValueError, TypeError):
                pass
    return ratings


def _extract_distances_from_school(item: dict) -> list:
    """
    Извлекает расстояния до школ из одного элемента.

    Parameters
    ----------
    item : dict
        Элемент списка школ.

    Returns
    -------
    list
        Список числовых расстояний в милях.
    """
    distances = []
    dist_data = item.get('data', {}).get('Distance', [])
    for distance_value in dist_data:
        if distance_value and isinstance(distance_value, str):
            match = re.search(r'(\d+\.?\d*)', distance_value)
            if match:
                distances.append(float(match.group(1)))
    return distances


def parse_schools(schools_str: Union[str, float]) -> Dict[str, Any]:
    """
    Извлекает агрегированные признаки о школах.

    Parameters
    ----------
    schools_str : str or float
        Строка с данными schools или NaN.

    Returns
    -------
    dict
        Словарь с признаками: schools_count, avg_school_rating,
        nearest_school_dist.
    """
    default_result = {
        'schools_count': 0,
        'avg_school_rating': np.nan,
        'nearest_school_dist': np.nan
    }

    if pd.isna(schools_str) or schools_str == '':
        return default_result

    try:
        if isinstance(schools_str, str):
            schools_data = ast.literal_eval(schools_str)
        else:
            schools_data = schools_str

        if not schools_data or len(schools_data) == 0:
            return default_result

        all_ratings = []
        all_distances = []

        for item in schools_data:
            all_ratings.extend(_extract_ratings_from_school(item))
            all_distances.extend(_extract_distances_from_school(item))

        return {
            'schools_count': len(schools_data),
            'avg_school_rating': np.mean(all_ratings) if all_ratings else np.nan,
            'nearest_school_dist': min(all_distances) if all_distances else np.nan
        }

    except (SyntaxError, ValueError, TypeError):
        return default_result
