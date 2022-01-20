# Copyright (c) 2021 University of Winnipeg
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
