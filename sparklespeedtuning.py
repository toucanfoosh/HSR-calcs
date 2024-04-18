from numpy import exp

# You can find detailed information about speed values of your characters with decimal values here:
# https://fribbels.github.io/hsr-optimizer#scorer

# NOTE: AV in game always rounds up when being displayed (at least from my testing)

# SPARKLE DUAL HYPERSPEED TUNING
# Speed needed to:
# - Have carry act
# - Have Sparkle action advance
# - Have carry act
# - Have carry act again (BEFORE SPARKLE GOES AGAIN)
# - Have Sparkle action advance


def sparkle_dual_hyperspeed_tuning(teammates):
    if len(teammates) == 0:
        print("No teammates given")
        return
    elif not any(teammate.name == "sparkle" for teammate in teammates):
        print("No Sparkle in the team")
        return
    elif not any(teammate.carry for teammate in teammates):
        print("No carry in the team")
        return

    action_gauge = 10000
    carry = None
    sparkle = None
    for teammate in teammates:
        if teammate.carry:
            if carry is not None:
                print("This function only supports one carry in the team")
                return
            carry = teammate
        elif teammate.name == "sparkle":
            if sparkle is not None:
                print("The given team has more than one Sparkle")
                return
            sparkle = teammate

    # ------ COMBAT START ------

    # Immediate passive speed boosts
    carry_base_speed_mult = 1
    team_base_speed_mult = 1

    for teammate in teammates:
        carry_base_speed_mult = (
            carry_base_speed_mult + teammate.passive_carry_speed_mult
        )
        team_base_speed_mult = team_base_speed_mult + teammate.passive_speed_mult

    carry_speed = (
        carry.base_speed * (carry_base_speed_mult + (team_base_speed_mult - 1))
        + carry.flat_speed
    )
    sparkle_speed = sparkle.base_speed * team_base_speed_mult + sparkle.flat_speed

    carry_av = action_gauge / carry_speed
    sparkle_av = action_gauge / sparkle_speed

    concurrent_carry_av = 0
    total_carry_av = 0
    concurrent_sparkle_av = 0
    total_sparkle_av = 0

    print("\n------ Combat Start ------")
    print(
        "Carry speed: "
        + str(round(carry_speed, 2))
        + " || Carry concurrent action value: "
        + str(round(carry_av, 2))
    )
    print(
        "Sparkle speed: "
        + str(round(sparkle_speed, 2))
        + " || Sparkle concurrent action value: "
        + str(round(sparkle_av, 2))
    )
    if carry_av < sparkle_av:  # Carry goes first
        print(
            "On combat start carry acts first with "
            + str(-round(carry_av - sparkle_av, 2))
            + " less concurrent action value and "
            + str(round(carry_speed - sparkle_speed, 2))
            + " more speed"
        )
        total_sparkle_av += sparkle_av - carry_av
        concurrent_sparkle_av = sparkle_av - carry_av
    else:  # Sparkle goes first
        print(
            "On combat start Sparkle acts first with "
            + str(-round(sparkle_av - carry_av, 2))
            + " less concurrent action value and "
            + str(round(sparkle_speed - carry_speed, 2))
            + " more speed"
        )
        total_carry_av += carry_av - sparkle_av
        concurrent_carry_av = carry_av - sparkle_av

    # ------ ACTIONS ------
    sparkle_skill = 0

    # if Sparkle is faster than carry:
    if concurrent_sparkle_av < concurrent_carry_av:
        # Sparkle action advances our carry

        # Sparkle turn
        total_sparkle_av += sparkle_av
        concurrent_sparkle_av = sparkle_av
        # Carry action advanced
        concurrent_carry_av = max(0, concurrent_carry_av - carry_av / 2)
        sparkle_skill += 1

        print("\n------ After Sparkle First Action ------")
        print(
            "Carry speed: "
            + str(round(carry_speed, 2))
            + " || Concurrent Carry action value: "
            + str(round(concurrent_carry_av, 2))
            + " || Total Carry action value: "
            + str(round(total_carry_av, 2))
        )
        print(
            "Sparkle speed: "
            + str(round(sparkle_speed, 2))
            + " || Concurrent Sparkle action value: "
            + str(round(concurrent_sparkle_av, 2))
            + " || Total Sparkle action value: "
            + str(round(total_sparkle_av, 2))
        )

        if concurrent_sparkle_av < concurrent_carry_av:
            print(
                "Sparkle acts next with "
                + str(-round(concurrent_sparkle_av - concurrent_carry_av, 2))
                + " less action value"
            )
        else:
            print(
                "Carry acts next with "
                + str(-round(concurrent_carry_av - concurrent_sparkle_av, 2))
                + " less action value"
            )

    if concurrent_carry_av < concurrent_sparkle_av:

        # Carry first action
        carry_speed = (
            carry.base_speed
            * (
                carry_base_speed_mult
                + (team_base_speed_mult - 1)
                + carry.action_carry_speed_mult
            )
            + carry.flat_speed
        )
        concurrent_carry_av += action_gauge / carry_speed
        total_carry_av += action_gauge / carry_speed
        concurrent_sparkle_av = max(0, concurrent_sparkle_av - concurrent_carry_av)

        # ------ AFTER CARRY FIRST ACTION ------
        print("\n------ After Carry First Action ------")
        print(
            "Carry speed: "
            + str(round(carry_speed, 2))
            + " || Concurrent Carry action value: "
            + str(round(concurrent_carry_av, 2))
            + " || Total Carry action value: "
            + str(round(total_carry_av, 2))
        )
        print(
            "Sparkle speed: "
            + str(round(sparkle_speed, 2))
            + " || Concurrent Sparkle action value: "
            + str(round(concurrent_sparkle_av, 2))
            + " || Total Sparkle action value: "
            + str(round(total_sparkle_av, 2))
        )

        if concurrent_sparkle_av < concurrent_carry_av:
            print(
                "Sparkle acts next with "
                + str(-round(concurrent_sparkle_av - concurrent_carry_av, 2))
                + " less action value"
            )
        else:
            print(
                "Carry acts next with "
                + str(-round(concurrent_carry_av - concurrent_sparkle_av, 2))
                + " less action value"
            )

    # if Sparkle has already skilled we can calculate the speed needed for the carry to act again before Sparkle
    if sparkle_skill < 1 and concurrent_sparkle_av < concurrent_carry_av:
        # Sparkle action advances our carry

        # Sparkle turn
        total_sparkle_av += sparkle_av
        concurrent_sparkle_av = sparkle_av
        # Carry action advanced
        concurrent_carry_av = max(0, concurrent_carry_av - carry_av / 2)
        sparkle_skill += 1

        print("\n------ After Sparkle First Action ------")
        print(
            "Carry speed: "
            + str(round(carry_speed, 2))
            + " || Concurrent Carry action value: "
            + str(round(concurrent_carry_av, 2))
            + " || Total Carry action value: "
            + str(round(total_carry_av, 2))
        )
        print(
            "Sparkle speed: "
            + str(round(sparkle_speed, 2))
            + " || Concurrent Sparkle action value: "
            + str(round(concurrent_sparkle_av, 2))
            + " || Total Sparkle action value: "
            + str(round(total_sparkle_av, 2))
        )

        if concurrent_sparkle_av < concurrent_carry_av:
            print(
                "Sparkle acts next with "
                + str(-round(concurrent_sparkle_av - concurrent_carry_av, 2))
                + " less action value"
            )
        else:
            print(
                "Carry acts next with "
                + str(-round(concurrent_carry_av - concurrent_sparkle_av, 2))
                + " less action value"
            )

        if concurrent_carry_av < concurrent_sparkle_av:

            # Carry second action
            carry_speed = (
                carry.base_speed
                * (
                    carry_base_speed_mult
                    + (team_base_speed_mult - 1)
                    + carry.action_carry_speed_mult
                )
                + carry.flat_speed
            )
            concurrent_carry_av += action_gauge / carry_speed
            total_carry_av += action_gauge / carry_speed
            concurrent_sparkle_av = max(0, concurrent_sparkle_av - concurrent_carry_av)

            # ------ AFTER CARRY SECOND ACTION ------
            print("\n------ After Carry Second Action ------")
            print(
                "Carry speed: "
                + str(round(carry_speed, 2))
                + " || Concurrent Carry action value: "
                + str(round(concurrent_carry_av, 2))
                + " || Total Carry action value: "
                + str(round(total_carry_av, 2))
            )
            print(
                "Sparkle speed: "
                + str(round(sparkle_speed, 2))
                + " || Concurrent Sparkle action value: "
                + str(round(concurrent_sparkle_av, 2))
                + " || Total Sparkle action value: "
                + str(round(total_sparkle_av, 2))
            )

            if concurrent_sparkle_av < concurrent_carry_av:
                print(
                    "Sparkle acts next with "
                    + str(-round(concurrent_sparkle_av - concurrent_carry_av, 2))
                    + " less action value"
                )
            else:
                print(
                    "Carry acts next with "
                    + str(-round(concurrent_carry_av - concurrent_sparkle_av, 2))
                    + " less action value"
                )

    # ------ FINAL RESULTS ------
    print("\n------ Final Results ------")

    if concurrent_carry_av < concurrent_sparkle_av:
        print("Carry successfully acts twice before Sparkle acts again")
    else:
        concurrent_carry_av = max(0, concurrent_carry_av - concurrent_sparkle_av)
        print("concurrent_carry_av: " + str(round(concurrent_carry_av, 2)))
        speed_diff = (concurrent_carry_av / 10000) ** -1  # IDK HOW TO DO THIS MATH
        print("Carry speed diff " + str(round(speed_diff, 2)))
        print(
            "Carry needs "
            + str(round(123))
            + " more speed to act twice before Sparkle acts again"
        )


# Character class works as follows:
#
# --- BASE STATS ---
# name: name of the character
# base_speed: the base speed of the character with nothing
# total_speed: the speed of the character with all substats and bonuses, but before battle
#
# --- PASSIVE SPEED MULTIPLIERS ---
# passive_speed_mult: any passive speed multipliers that apply to the whole team
# passive_carry_speed_mult: any passive speed multipliers that only apply to the carry
#
# --- ACTION SPEED MULTIPLIERS ---
# action_speed_mult: any speed multipliers that apply to the whole team after an action is performed (assumed on skill)
# action_carry_speed_mult: any speed multipliers that apply to the carry after an action is performed (assumed on skill)
#
# --- ULTIMATE SPEED MULTIPLIERS ---
# ult_speed_mult: any speed multipliers that apply to the whole team after an ultimate is performed
# ult_carry_speed_mult: any speed multipliers that apply to the carry after an ultimate is performed
# ult_speed_flat: any flat speed bonuses that apply to the whole team after an ultimate is performed
# ult_carry_speed_flat: any flat speed bonuses that apply to the carry after an ultimate is performed
#
# --- CARRY ---
# carry: whether the character is the carry or not


class Character(object):
    def __init__(
        self,
        name,
        base_speed,
        total_speed,
        passive_speed_mult=0,
        passive_carry_speed_mult=0,
        action_speed_mult=0,
        action_carry_speed_mult=0,
        ult_speed_mult=0,
        ult_carry_speed_mult=0,
        ult_speed_flat=0,
        ult_carry_speed_flat=0,
        carry=False,
    ):
        self.name = name
        self.base_speed = base_speed
        self.total_speed = total_speed
        self.flat_speed = total_speed - base_speed
        self.passive_speed_mult = passive_speed_mult
        self.passive_carry_speed_mult = passive_carry_speed_mult
        self.action_speed_mult = action_speed_mult
        self.action_carry_speed_mult = action_carry_speed_mult
        self.ult_speed_mult = ult_speed_mult
        self.ult_carry_speed_mult = ult_carry_speed_mult
        self.ult_speed_flat = ult_speed_flat
        self.ult_carry_speed_flat = ult_carry_speed_flat
        self.carry = carry


# The following characters are mine, feel free to change for your personal uses

yanqing = Character("yanqing", 109, 157.2, action_carry_speed_mult=0.1, carry=True)
sparkle = Character("sparkle", 101, 164.5)
ruan_mei = Character("ruan_mei", 104, 118.8, passive_speed_mult=0.1)


def main():
    sparkle_dual_hyperspeed_tuning([yanqing, sparkle, ruan_mei])


if __name__ == "__main__":
    main()
