from __future__ import unicode_literals
from newscatcherapi import const

import sys

def validate_language(language):
    if is_valid_list(language):
        for each_lang in language:
            if each_lang.strip().lower() not in const.allowed_languages:
                raise ValueError(f"{each_lang} - is an invalid language. Language should be one of this list => {str(const.allowed_languages)}")
        return ','.join([i.strip().lower() for i in language])
    elif is_valid_string(language):
        language_clean = [i.strip().lower() for i in language.split(',')]
        for each_lang in language_clean:
            if each_lang not in const.allowed_languages:
                raise ValueError(f"{each_lang} - is an invalid language. Language should be one of this list => {str(const.allowed_languages)}")
        return ','.join(language_clean)
    else:
        raise TypeError("lang parameter should be of type str or list")


def validate_countries(list_countries, name_parameter):
    if is_valid_list(list_countries):
        valid_countries = [i.strip().upper() for i in list_countries]
        return ','.join(valid_countries)
    elif is_valid_string(list_countries):
        valid_countries = [i.strip().upper() for i in list_countries.split(',')]
        return ','.join(valid_countries)
    else:
        raise TypeError(f"{name_parameter} parameter should be of type str or list")

def validate_topic(topic):
    if is_valid_string(topic):
        if topic in const.allowed_topics:
            return topic
        else:
            raise ValueError(
                f"{topic} - is an unsupported topic. Topic should be one of this list => {str(const.allowed_topics)}")
    else:
        raise TypeError(f"topic parameter should be of type str")


def validate_sources(list_sources, name_parameter):
    if is_valid_list(list_sources):
        valid_sources = [i.strip().lower() for i in list_sources]
        return ','.join(valid_sources)
    elif is_valid_string(list_sources):
        valid_sources = [i.strip().lower() for i in list_sources.split(',')]
        return ','.join(valid_sources)
    else:
        raise TypeError(f"{name_parameter} parameter should be of type str or list")

def validate_when(when, name_parameter):
    if is_valid_string(when):
        if when[len(when)-1] in ['d', 'h']:
            return when
        else:
            raise TypeError(f"{name_parameter} parameter should be the next form: 30d or 24h ")
    else:
        raise TypeError(f"{name_parameter} parameter should be of type str")


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:

    def is_valid_string(var):
        return isinstance(var, str)

    def is_valid_num(var):
        return isinstance(var, (int, float))

    def is_valid_list(var):
        return isinstance(var, list)

    def is_valid_boolean(var):
        return isinstance(var, bool)

elif PY2:

    def is_valid_string(var):
        return isinstance(var, basestring)

    def is_valid_num(var):
        return isinstance(var, (int, float, long))


else:

    def is_valid_string(var):
        raise SystemError("unsupported version of python detected (supported versions: 2, 3)")
