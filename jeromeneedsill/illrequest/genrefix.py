from django.shortcuts import render

from django.conf import settings

GENRE_NOT_SELECTED = "genrenotselected"

def param_list_has_genre_problem(paramlist):
    if not hasattr(settings, 'PROBLEM_GENRE_MATCH'):
        return False
    # if PROBLEM_GENRE_MATCH is defined, check for PROBLEM_GENRE_REPLACE_MAP
    elif not hasattr(settings, 'PROBLEM_GENRE_REPLACE_MAP'):
        raise Exception(
            "setting PROBLEM_GENRE_MATCH needs to be defined when "
            "PROBLEM_GENRE_MATCH is set")

    genre_found = False
    for key, value in paramlist:
        if key in settings.PROBLEM_GENRE_MATCH:
            genre_found = True
            if (value in settings.PROBLEM_GENRE_MATCH[key] or
                value==GENRE_NOT_SELECTED):
                return True

    # return False if we went through all params and didn't find a problematic
    # genre, but at least found one
    # return True if we didn't even find one, that means yes, we have a problem
    return not genre_found

def ask_for_genre_problem_fix(request, targeturl, paramlist):
    # this should have already been established by a
    # call to param_list_has_genre_problem
    assert( hasattr(settings, 'PROBLEM_GENRE_MATCH') )
    assert( hasattr(settings, 'PROBLEM_GENRE_REPLACE_MAP') )

    filtered_paramlist = [
        (key, value)
        for key, value in paramlist
        if key not in settings.PROBLEM_GENRE_MATCH
        ]
    return render(
        request, 'genrefix.html',
        {'targeturl': targeturl,
         # should we use rft.genre ? or perhaps pick what is called for
         'genrefieldname': 'genre',
         'genrenotselectedvalue': GENRE_NOT_SELECTED,
         'genreremap': list(settings.PROBLEM_GENRE_REPLACE_MAP.items()),
         'paramlist': filtered_paramlist} )
