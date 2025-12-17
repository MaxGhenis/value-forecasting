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
HISTORICAL_TRAJECTORIES = {
    # === SOCIAL VALUES - Strong liberalization ===
    "HOMOSEX": {
        # % saying "Not wrong at all" (+40 pts over 44 years)
        1980: 15, 1990: 13, 2000: 29, 2010: 42,
        2018: 57, 2021: 62, 2022: 61, 2024: 55,
    },
    "GRASS": {
        # % saying "Legal" (+43 pts over 44 years)
        1980: 26, 1990: 17, 2000: 34, 2010: 48,
        2018: 65, 2022: 70, 2024: 68,
    },
    "PREMARSX": {
        # % saying "Not wrong at all" (+38 pts over 52 years)
        1972: 27, 1990: 40, 2000: 42, 2010: 53,
        2018: 62, 2021: 66, 2022: 69, 2024: 65,
    },
    "ABANY": {
        # % supporting abortion for any reason (+19 pts over 44 years)
        1980: 41, 1990: 43, 2000: 40, 2010: 44,
        2018: 50, 2021: 56, 2022: 59, 2024: 60,
    },
    "FEPOL": {
        # % disagreeing women unsuited for politics (+9 pts over 34 years)
        1990: 73, 2000: 77, 2010: 79, 2018: 86, 2022: 85, 2024: 82,
    },

    # === ECONOMIC/SPENDING - Moderate liberalization ===
    "NATRACE": {
        # % saying too little spending on race (+25 pts over 44 years)
        1980: 26, 1990: 40, 2000: 38, 2010: 34,
        2018: 56, 2021: 52, 2022: 56, 2024: 51,
    },
    "NATEDUC": {
        # % saying too little spending on education (+22 pts over 44 years)
        1980: 55, 1990: 73, 2000: 72, 2010: 72,
        2018: 75, 2021: 73, 2022: 75, 2024: 76,
    },
    "NATENVIR": {
        # % saying too little spending on environment (+15 pts over 44 years)
        1980: 51, 1990: 75, 2000: 63, 2010: 57,
        2018: 68, 2021: 70, 2022: 69, 2024: 66,
    },
    "NATHEAL": {
        # % saying too little spending on health (+17 pts over 44 years)
        1980: 57, 1990: 74, 2000: 73, 2010: 60,
        2018: 73, 2021: 67, 2022: 70, 2024: 74,
    },
    "EQWLTH": {
        # % supporting gov reducing inequality (+11 pts over 44 years)
        1980: 44, 1990: 52, 2000: 44, 2010: 42,
        2018: 50, 2021: 54, 2022: 55, 2024: 54,
    },
    "HELPPOOR": {
        # % saying gov should help poor (+4 pts over 34 years)
        1990: 34, 2000: 27, 2010: 28, 2018: 32,
        2021: 38, 2022: 40, 2024: 39,
    },
    "CAPPUN": {
        # % opposing death penalty (+12 pts over 44 years)
        1980: 28, 1990: 21, 2000: 31, 2010: 32,
        2018: 37, 2021: 44, 2022: 40, 2024: 40,
    },

    # === STABLE/MIXED ===
    "GUNLAW": {
        # % favoring gun permits (-3 pts, essentially stable)
        1972: 72, 1980: 71, 1990: 80, 2000: 82, 2010: 74,
        2018: 72, 2021: 67, 2022: 71, 2024: 70,
    },
    "POLVIEWS": {
        # % self-identifying as liberal (+4 pts, stable)
        1980: 26, 1990: 27, 2000: 26, 2010: 29,
        2018: 29, 2021: 33, 2022: 32, 2024: 29,
    },
    "PRAYER": {
        # % opposing school prayer (-5 pts over 34 years)
        1990: 58, 2000: 61, 2010: 56, 2018: 53, 2022: 48, 2024: 54,
    },

    # === COUNTER-TREND - Declining ===
    "TRUST": {
        # % saying most people can be trusted (-21 pts over 52 years!)
        1972: 46, 1980: 46, 1990: 38, 2000: 35,
        2010: 33, 2018: 32, 2022: 25, 2024: 25,
    },
    "FAIR": {
        # % saying people try to be fair (+12 pts over 52 years)
        1972: 34, 1980: 35, 1990: 36, 2000: 38,
        2010: 38, 2018: 43, 2022: 47, 2024: 46,
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
