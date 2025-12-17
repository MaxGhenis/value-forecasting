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
        "responses": {
            1: "Yes",
            2: "No",
        },
        "liberal_response": 1,  # "Yes"
        "first_year": 1977,
        "description": "Abortion for any reason support",
    },
}

# Known historical trajectories (for validation)
# Source: GSS Data Explorer
HISTORICAL_TRAJECTORIES = {
    "HOMOSEX": {
        # % saying "Not wrong at all"
        1973: 11,
        1980: 14,
        1990: 13,
        2000: 27,
        2010: 41,
        2018: 58,
        2021: 64,
    },
    "GRASS": {
        # % saying "Legal"
        1973: 19,
        1980: 25,
        1990: 16,
        2000: 31,
        2010: 44,
        2018: 61,
        2021: 68,
    },
    "FEPOL": {
        # % saying "Disagree" (women are suited)
        1974: 53,
        1980: 56,
        1990: 63,
        2000: 71,
        2010: 76,
        2018: 81,
    },
    "PREMARSX": {
        # % saying "Not wrong at all"
        1972: 26,
        1980: 33,
        1990: 36,
        2000: 38,
        2010: 42,
        2018: 49,
    },
    "CAPPUN": {
        # % saying "Oppose"
        1972: 42,
        1980: 27,
        1990: 22,
        2000: 28,
        2010: 35,
        2018: 39,
        2021: 40,
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
