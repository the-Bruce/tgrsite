import random

def diceCaptcha():
    dice = [4,6,8,10,12,20]
    d1, d2 = random.choice(dice), random.choice(dice)
    question = ["What is ",
            random.choice(["the maximum total ", "the largest sum "]),
            "when rolling ",
            "a d{}".format(d1),
            random.choice([" and a ", " plus a "]),
            "d{}?".format(d2)
            ]
    chelp = "(dX means an X-sided die, e.g. d4 means a four sided die with numbers 1 to 4 on it.)"
    return ("".join(question), d1+d2, chelp)

def sitenameCaptcha():
    sitename = "warwicktabletop"
    nums = orderedDifferentRandoms(list(range(7)))
    question = ["What are the ",
            "{}, {} and {} ".format(ordinal(nums[0]+1), ordinal(nums[1]+1), ordinal(nums[2]+1)),
            "letters of our ",
            random.choice(["site name ", "domain name "]),
            "(excluding the 'www.' at the start of it)?"
            ]
    chelp = "(Just write each of the letters one after the other - don't separate them with a comma or similar!)"
    return ("".join(question), "".join(map(lambda x: sitename[x], nums)), chelp)

def ordinal(number):
    # Converts a number into its ordinal (e.g. 1 -> 1st)
    ordinals = ["th","st","nd","rd","th","th","th","th","th","th"]
    return str(number)+ordinals[number % 10]

def orderedDifferentRandoms(choices):
    # To make a list of ordered, different random numbers:
    # Take your choices, shuffle and take the first three (will all be different choices).
    # Then sort.
    random.shuffle(choices)
    nums = choices[0:3]
    nums.sort()
    return nums

def makeCaptcha():
    return random.choice([diceCaptcha, sitenameCaptcha])()
