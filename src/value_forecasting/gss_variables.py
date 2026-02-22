"""GSS variable definitions and historical data."""

# GSS variables with significant historical change
# Format: {var_name: {question, response_scale, direction, first_year}}

GSS_VARIABLES = {
    "HOMOSEX": {
        "question": "What about sexual relations between two adults of the same sex - do you think it is always wrong, almost always wrong, wrong only sometimes, or not wrong at all?",
        "responses": {
            1: "Always wrong",
            2: "Almost always wrong",
            3: "Sometimes wrong",
            4: "Not wrong at all",
        },
        "liberal_response": 4,  # "Not wrong at all"
        "first_year": 1973,
        "description": "Attitudes toward homosexual relations",
    },
    "GRASS": {
        "question": "Do you think the use of marijuana should be made legal or not?",
        "responses": {
            1: "Legal",
            2: "Not legal",
        },
        "liberal_response": 1,  # "Legal"
        "first_year": 1973,
        "description": "Marijuana legalization support",
    },
    "FEPOL": {
        "question": "Tell me if you agree or disagree with this statement: Most men are better suited emotionally for politics than are most women.",
        "responses": {
            1: "Agree",
            2: "Disagree",
        },
        "liberal_response": 2,  # "Disagree"
        "first_year": 1974,
        "description": "Women suited for politics",
    },
    "PREMARSX": {
        "question": "There's been a lot of discussion about the way morals and attitudes about sex are changing in this country. If a man and woman have sex relations before marriage, do you think it is always wrong, almost always wrong, wrong only sometimes, or not wrong at all?",
        "responses": {
            1: "Always wrong",
            2: "Almost always wrong",
            3: "Sometimes wrong",
            4: "Not wrong at all",
        },
        "liberal_response": 4,  # "Not wrong at all"
        "first_year": 1972,
        "description": "Premarital sex attitudes",
    },
    "CAPPUN": {
        "question": "Do you favor or oppose the death penalty for persons convicted of murder?",
        "responses": {
            1: "Favor",
            2: "Oppose",
        },
        "liberal_response": 2,  # "Oppose"
        "first_year": 1972,
        "description": "Death penalty support",
    },
    "GUNLAW": {
        "question": "Would you favor or oppose a law which would require a person to obtain a police permit before he or she could buy a gun?",
        "responses": {
            1: "Favor",
            2: "Oppose",
        },
        "liberal_response": 1,  # "Favor"
        "first_year": 1972,
        "description": "Gun permit requirement support",
    },
    "ABANY": {
        "question": "Please tell me whether or not you think it should be possible for a pregnant woman to obtain a legal abortion if the woman wants it for any reason?",
        "responses": {1: "Yes", 2: "No"},
        "liberal_response": 1,
        "first_year": 1977,
        "description": "Abortion for any reason support",
    },
    # Economic/spending variables
    "NATRACE": {
        "question": "Are we spending too much, too little, or about the right amount on improving the conditions of Blacks?",
        "responses": {1: "Too little", 2: "About right", 3: "Too much"},
        "liberal_response": 1,
        "first_year": 1973,
        "description": "Support for more spending on race issues",
    },
    "NATEDUC": {
        "question": "Are we spending too much, too little, or about the right amount on improving the nation's education system?",
        "responses": {1: "Too little", 2: "About right", 3: "Too much"},
        "liberal_response": 1,
        "first_year": 1973,
        "description": "Support for more spending on education",
    },
    "NATENVIR": {
        "question": "Are we spending too much, too little, or about the right amount on improving and protecting the environment?",
        "responses": {1: "Too little", 2: "About right", 3: "Too much"},
        "liberal_response": 1,
        "first_year": 1973,
        "description": "Support for more spending on environment",
    },
    "NATHEAL": {
        "question": "Are we spending too much, too little, or about the right amount on improving and protecting the nation's health?",
        "responses": {1: "Too little", 2: "About right", 3: "Too much"},
        "liberal_response": 1,
        "first_year": 1973,
        "description": "Support for more spending on health",
    },
    "EQWLTH": {
        "question": "Some people think that the government in Washington ought to reduce the income differences between the rich and the poor. Others think the government should not concern itself with reducing this income difference. (1=reduce, 7=no action)",
        "responses": {1: "Gov reduce", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "No action"},
        "liberal_response": [1, 2, 3],  # Top 3 = support redistribution
        "first_year": 1978,
        "description": "Support for government reducing inequality",
    },
    "HELPPOOR": {
        "question": "Some people think that the government in Washington should do everything possible to improve the standard of living of all poor Americans. Others think it is not the government's responsibility. (1=gov action, 5=not gov responsibility)",
        "responses": {1: "Gov action", 2: "2", 3: "3", 4: "4", 5: "Not gov"},
        "liberal_response": [1, 2],
        "first_year": 1975,
        "description": "Support for government helping poor",
    },
    # Trust variables
    "TRUST": {
        "question": "Generally speaking, would you say that most people can be trusted or that you can't be too careful in dealing with people?",
        "responses": {1: "Can trust", 2: "Can't be too careful", 3: "Depends"},
        "liberal_response": 1,  # Though "liberal" is a misnomer here
        "first_year": 1972,
        "description": "Social trust - most people can be trusted",
    },
    "FAIR": {
        "question": "Do you think most people would try to take advantage of you if they got a chance, or would they try to be fair?",
        "responses": {1: "Try to be fair", 2: "Take advantage"},
        "liberal_response": 1,
        "first_year": 1972,
        "description": "Believe people try to be fair",
    },
    # Political views
    "POLVIEWS": {
        "question": "We hear a lot of talk these days about liberals and conservatives. Where would you place yourself on this scale? (1=extremely liberal, 7=extremely conservative)",
        "responses": {1: "Ext liberal", 2: "Liberal", 3: "Slightly liberal", 4: "Moderate", 5: "Slightly conservative", 6: "Conservative", 7: "Ext conservative"},
        "liberal_response": [1, 2, 3],
        "first_year": 1974,
        "description": "Self-identified liberal",
    },
    "PRAYER": {
        "question": "The United States Supreme Court has ruled that no state or local government may require the reading of the Lord's Prayer or Bible verses in public schools. What are your views on this?",
        "responses": {1: "Approve", 2: "Disapprove"},
        "liberal_response": 1,  # Approve of banning school prayer
        "first_year": 1974,
        "description": "Approve of school prayer ban",
    },
}

# Known historical trajectories (for validation)
# Source: GSS cumulative data file gss7224_r2.dta
# All values are % giving the "liberal" response
# Full time series extracted from microdata (not just selected years)
HISTORICAL_TRAJECTORIES = {
    # === SOCIAL VALUES - Strong liberalization ===
    "HOMOSEX": {
        # % saying "Not wrong at all"
        1973: 11, 1974: 13, 1976: 16, 1977: 15, 1980: 15,
        1982: 13, 1984: 14, 1985: 14, 1987: 12, 1988: 13,
        1989: 16, 1990: 13, 1991: 16, 1993: 22, 1994: 23,
        1996: 28, 1998: 29, 2000: 29, 2002: 33, 2004: 31,
        2006: 33, 2008: 38, 2010: 42, 2012: 45, 2014: 49,
        2016: 52, 2018: 57, 2021: 62, 2022: 61, 2024: 55,
    },
    "GRASS": {
        # % saying "Should be legal"
        1973: 19, 1975: 21, 1976: 29, 1978: 31, 1980: 26,
        1983: 21, 1984: 24, 1986: 18, 1987: 17, 1988: 18,
        1989: 17, 1990: 17, 1991: 19, 1993: 23, 1994: 24,
        1996: 27, 1998: 29, 2000: 34, 2002: 36, 2004: 36,
        2006: 37, 2008: 40, 2010: 48, 2012: 47, 2014: 55,
        2016: 61, 2018: 65, 2022: 70, 2024: 69,
    },
    "PREMARSX": {
        # % saying "Not wrong at all"
        1972: 27, 1974: 31, 1975: 33, 1977: 37, 1978: 39,
        1982: 43, 1983: 39, 1985: 43, 1986: 40, 1988: 41,
        1989: 41, 1990: 40, 1991: 44, 1993: 42, 1994: 44,
        1996: 44, 1998: 43, 2000: 42, 2002: 45, 2004: 46,
        2006: 46, 2008: 54, 2010: 53, 2012: 56, 2014: 58,
        2016: 59, 2018: 62, 2021: 66, 2022: 69, 2024: 65,
    },
    "ABANY": {
        # % supporting abortion for any reason
        1977: 38, 1978: 33, 1980: 41, 1982: 39, 1983: 34,
        1984: 39, 1985: 37, 1987: 39, 1988: 36, 1989: 40,
        1990: 43, 1991: 43, 1993: 45, 1994: 46, 1996: 45,
        1998: 41, 2000: 40, 2002: 43, 2004: 41, 2006: 40,
        2008: 42, 2010: 44, 2012: 44, 2014: 45, 2016: 46,
        2018: 50, 2021: 56, 2022: 59, 2024: 60,
    },
    "FEPOL": {
        # % disagreeing women unsuited for politics
        1974: 53, 1975: 50, 1977: 51, 1978: 56, 1982: 62,
        1983: 64, 1985: 61, 1986: 63, 1988: 67, 1989: 70,
        1990: 73, 1991: 74, 1993: 79, 1994: 79, 1996: 78,
        1998: 77, 2000: 77, 2002: 78, 2004: 75, 2006: 77,
        2008: 73, 2010: 79, 2012: 80, 2014: 82, 2016: 80,
        2018: 86, 2022: 85, 2024: 82,
    },

    # === ECONOMIC/SPENDING - Moderate liberalization ===
    "NATRACE": {
        # % saying too little spending on race
        1973: 35, 1974: 33, 1975: 29, 1976: 29, 1977: 27,
        1978: 26, 1980: 26, 1982: 42, 1983: 32, 1984: 37,
        1985: 33, 1986: 36, 1987: 47, 1988: 38, 1989: 36,
        1990: 40, 1991: 37, 1993: 39, 1994: 34, 1996: 35,
        1998: 38, 2000: 38, 2002: 33, 2004: 35, 2006: 39,
        2008: 40, 2010: 34, 2012: 38, 2014: 36, 2016: 52,
        2018: 56, 2021: 52, 2022: 56, 2024: 51,
    },
    "NATEDUC": {
        # % saying too little spending on education
        1973: 51, 1974: 53, 1975: 51, 1976: 52, 1977: 49,
        1978: 54, 1980: 55, 1982: 62, 1983: 62, 1984: 65,
        1985: 62, 1986: 62, 1987: 66, 1988: 66, 1989: 69,
        1990: 73, 1991: 69, 1993: 69, 1994: 72, 1996: 70,
        1998: 71, 2000: 72, 2002: 74, 2004: 72, 2006: 74,
        2008: 71, 2010: 72, 2012: 74, 2014: 72, 2016: 72,
        2018: 75, 2021: 73, 2022: 75, 2024: 76,
    },
    "NATENVIR": {
        # % saying too little spending on environment
        1973: 65, 1974: 63, 1975: 57, 1976: 57, 1977: 51,
        1978: 55, 1980: 51, 1982: 56, 1983: 58, 1984: 61,
        1985: 59, 1986: 63, 1987: 69, 1988: 68, 1989: 75,
        1990: 75, 1991: 70, 1993: 59, 1994: 61, 1996: 61,
        1998: 63, 2000: 63, 2002: 60, 2004: 63, 2006: 69,
        2008: 68, 2010: 57, 2012: 58, 2014: 59, 2016: 63,
        2018: 68, 2021: 70, 2022: 69, 2024: 66,
    },
    "NATHEAL": {
        # % saying too little spending on health
        1973: 63, 1974: 66, 1975: 65, 1976: 63, 1977: 59,
        1978: 58, 1980: 57, 1982: 62, 1983: 60, 1984: 60,
        1985: 59, 1986: 61, 1987: 73, 1988: 68, 1989: 71,
        1990: 74, 1991: 71, 1993: 74, 1994: 67, 1996: 68,
        1998: 69, 2000: 73, 2002: 75, 2004: 78, 2006: 75,
        2008: 77, 2010: 60, 2012: 62, 2014: 59, 2016: 65,
        2018: 73, 2021: 67, 2022: 70, 2024: 74,
    },
    "EQWLTH": {
        # % supporting gov reducing inequality (1-3 on 7-point scale)
        1978: 48, 1980: 48, 1983: 46, 1984: 48, 1986: 48,
        1987: 49, 1988: 48, 1989: 52, 1990: 51, 1991: 52,
        1993: 53, 1994: 48, 1996: 49, 1998: 49, 2000: 48,
        2002: 49, 2004: 47, 2006: 46, 2008: 45, 2010: 42,
        2012: 44, 2014: 44, 2016: 48, 2018: 50, 2021: 54,
        2022: 55, 2024: 54,
    },
    "HELPPOOR": {
        # % saying gov should help poor (1-2 on 5-point scale)
        1975: 40, 1983: 33, 1984: 29, 1986: 31, 1987: 35,
        1988: 31, 1989: 32, 1990: 35, 1991: 34, 1993: 27,
        1994: 27, 1996: 26, 1998: 26, 2000: 27, 2002: 28,
        2004: 27, 2006: 29, 2008: 33, 2010: 28, 2012: 28,
        2014: 29, 2016: 33, 2018: 32, 2021: 38, 2022: 40,
        2024: 39,
    },
    "CAPPUN": {
        # % opposing death penalty
        1974: 34, 1975: 36, 1976: 31, 1977: 28, 1978: 30,
        1980: 28, 1982: 27, 1983: 23, 1984: 25, 1985: 20,
        1986: 25, 1987: 31, 1988: 24, 1989: 22, 1990: 21,
        1991: 24, 1993: 23, 1994: 21, 1996: 23, 1998: 27,
        2000: 31, 2002: 31, 2004: 32, 2006: 33, 2008: 34,
        2010: 32, 2012: 35, 2014: 36, 2016: 40, 2018: 37,
        2021: 44, 2022: 40, 2024: 40,
    },

    # === STABLE/MIXED ===
    "GUNLAW": {
        # % favoring gun permits
        1972: 72, 1973: 75, 1974: 76, 1975: 76, 1976: 73,
        1977: 73, 1980: 71, 1982: 74, 1984: 72, 1985: 73,
        1987: 73, 1988: 76, 1989: 79, 1990: 80, 1991: 82,
        1993: 82, 1994: 79, 1996: 82, 1998: 84, 2000: 82,
        2002: 80, 2004: 80, 2006: 80, 2008: 79, 2010: 75,
        2012: 74, 2014: 72, 2016: 72, 2018: 72, 2021: 67,
        2022: 71, 2024: 70,
    },
    "POLVIEWS": {
        # % self-identifying as liberal (1-3 on 7-point scale)
        1974: 30, 1975: 30, 1976: 29, 1977: 29, 1978: 28,
        1980: 26, 1982: 30, 1983: 24, 1984: 24, 1985: 25,
        1986: 24, 1987: 30, 1988: 28, 1989: 28, 1990: 27,
        1991: 28, 1993: 27, 1994: 27, 1996: 25, 1998: 29,
        2000: 26, 2002: 26, 2004: 24, 2006: 27, 2008: 27,
        2010: 29, 2012: 28, 2014: 27, 2016: 29, 2018: 29,
        2021: 33, 2022: 31, 2024: 29,
    },
    "PRAYER": {
        # % approving of school prayer ban
        1974: 32, 1975: 36, 1977: 34, 1982: 35, 1983: 41,
        1985: 44, 1986: 38, 1988: 39, 1989: 42, 1990: 42,
        1991: 40, 1993: 41, 1994: 39, 1996: 42, 1998: 45,
        2000: 39, 2002: 40, 2004: 36, 2006: 42, 2008: 41,
        2010: 44, 2012: 41, 2014: 41, 2016: 42, 2018: 47,
        2022: 52, 2024: 46,
    },

    # === COUNTER-TREND - Declining ===
    "TRUST": {
        # % saying most people can be trusted
        1972: 46, 1973: 46, 1975: 40, 1976: 44, 1978: 39,
        1980: 46, 1983: 37, 1984: 48, 1986: 38, 1987: 39,
        1988: 39, 1989: 41, 1990: 38, 1991: 38, 1993: 36,
        1994: 34, 1996: 34, 1998: 38, 2000: 35, 2002: 34,
        2004: 36, 2006: 32, 2008: 33, 2010: 33, 2012: 32,
        2014: 31, 2016: 32, 2018: 32, 2022: 25, 2024: 25,
    },
    "FAIR": {
        # % saying people would try to be fair
        1972: 60, 1973: 58, 1975: 62, 1976: 59, 1978: 65,
        1980: 61, 1983: 60, 1984: 62, 1986: 63, 1987: 54,
        1988: 61, 1989: 58, 1990: 58, 1991: 58, 1993: 56,
        1994: 54, 1996: 50, 1998: 53, 2000: 52, 2002: 50,
        2004: 51, 2006: 49, 2008: 52, 2010: 53, 2012: 52,
        2014: 52, 2016: 53, 2018: 49, 2022: 44, 2024: 42,
    },
}


def get_historical_context(variable: str, cutoff_year: int) -> str:
    """Generate historical context for prompting up to cutoff year."""
    if variable not in GSS_VARIABLES:
        raise ValueError(f"Unknown variable: {variable}")

    var_info = GSS_VARIABLES[variable]
    trajectory = HISTORICAL_TRAJECTORIES.get(variable, {})

    # Filter to pre-cutoff years
    pre_cutoff = {y: v for y, v in trajectory.items() if y <= cutoff_year}

    context = f"""Question: {var_info['question']}

The General Social Survey has tracked American opinions on this question since {var_info['first_year']}.

Historical data (% giving the liberal/progressive response):
"""
    for year in sorted(pre_cutoff.keys()):
        context += f"- {year}: {pre_cutoff[year]}%\n"

    return context
