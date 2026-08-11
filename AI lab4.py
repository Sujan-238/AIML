# Candidate Elimination Algorithm
# Experiment: Implementation of Candidate Elimination Algorithm

# Training Dataset
data = [
    ["Sunny", "Warm", "Normal", "Strong", "Yes"],  # D1
    ["Sunny", "Warm", "High", "Strong", "Yes"],    # D2
    ["Rainy", "Cold", "High", "Strong", "No"],     # D3
    ["Sunny", "Warm", "High", "Weak", "Yes"]       # D4
]

# Attribute names
attributes = ["Sky", "AirTemp", "Humidity", "Wind"]

# Special symbols
ANY = "?"
NULL = "Ø"


# ---------------------------------------------------------
# Function to display a hypothesis
# ---------------------------------------------------------
def display_hypothesis(h):
    return "<" + ", ".join(h) + ">"


# ---------------------------------------------------------
# Check whether hypothesis covers an instance
# ---------------------------------------------------------
def covers(h, instance):
    for h_value, x_value in zip(h, instance):
        if h_value != ANY and h_value != x_value:
            return False
    return True


# ---------------------------------------------------------
# Check whether hypothesis is more general than another
# ---------------------------------------------------------
def more_general_or_equal(h1, h2):
    """
    Returns True if h1 is more general than or equal to h2.
    """
    for a, b in zip(h1, h2):

        # h1 is ANY -> always more general
        if a == ANY:
            continue

        # h1 is NULL -> only equal to NULL
        if a == NULL:
            if b != NULL:
                return False

        # Specific value
        else:
            if b == ANY:
                return False

            if b == NULL:
                return False

            if a != b:
                return False

    return True


# ---------------------------------------------------------
# Minimal Generalization of S
# ---------------------------------------------------------
def minimal_generalization(s, instance):
    new_s = s.copy()

    for i in range(len(s)):

        # If S is empty for this attribute
        if new_s[i] == NULL:
            new_s[i] = instance[i]

        # If values are different, generalize to ?
        elif new_s[i] != instance[i]:
            new_s[i] = ANY

    return new_s


# ---------------------------------------------------------
# Minimal Specializations of G
# ---------------------------------------------------------
def minimal_specializations(g, instance, domains, s):

    specializations = []

    for i in range(len(g)):

        # We can specialize only if G has ?
        if g[i] == ANY:

            for value in domains[i]:

                # Do not use the value occurring in negative example
                if value != instance[i]:

                    new_g = g.copy()
                    new_g[i] = value

                    # It must still be more general than S
                    if more_general_or_equal(new_g, s):
                        specializations.append(new_g)

    return specializations


# ---------------------------------------------------------
# Remove duplicate hypotheses
# ---------------------------------------------------------
def remove_duplicates(boundary):
    unique = []

    for h in boundary:
        if h not in unique:
            unique.append(h)

    return unique


# ---------------------------------------------------------
# Remove hypotheses from G that are not general enough
# ---------------------------------------------------------
def remove_less_general_hypotheses(G, S):

    new_G = []

    for g in G:

        valid = True

        for s in S:
            if not more_general_or_equal(g, s):
                valid = False
                break

        if valid:
            new_G.append(g)

    return new_G


# ---------------------------------------------------------
# Candidate Elimination Algorithm
# ---------------------------------------------------------

# Attribute domains
domains = [
    ["Sunny", "Rainy"],          # Sky
    ["Warm", "Cold"],            # AirTemp
    ["Normal", "High"],          # Humidity
    ["Strong", "Weak"]           # Wind
]


# Initial Most Specific Boundary S
S = [[NULL, NULL, NULL, NULL]]

# Initial Most General Boundary G
G = [[ANY, ANY, ANY, ANY]]


print("=" * 70)
print("       CANDIDATE ELIMINATION ALGORITHM")
print("=" * 70)

print("\nInitial Boundaries:")
print("S =", [display_hypothesis(h) for h in S])
print("G =", [display_hypothesis(h) for h in G])


# ---------------------------------------------------------
# Process each training example
# ---------------------------------------------------------

for step, row in enumerate(data, start=1):

    instance = row[:4]
    target = row[4]

    print("\n" + "-" * 70)
    print(f"Processing D{step}: {instance} -> {target}")
    print("-" * 70)

    # -----------------------------------------------------
    # Positive Example
    # -----------------------------------------------------
    if target == "Yes":

        print("\nPositive Instance")

        # Generalize S
        new_S = []

        for s in S:

            # If S does not cover positive example,
            # minimally generalize it
            if not covers(s, instance):
                s = minimal_generalization(s, instance)

            new_S.append(s)

        S = remove_duplicates(new_S)

        # Remove G hypotheses that do not cover positive example
        new_G = []

        for g in G:

            if covers(g, instance):
                new_G.append(g)

        G = new_G

        # Remove S hypotheses that are not more specific than
        # at least one member of G
        new_S = []

        for s in S:

            valid = False

            for g in G:

                if more_general_or_equal(g, s):
                    valid = True
                    break

            if valid:
                new_S.append(s)

        S = new_S

    # -----------------------------------------------------
    # Negative Example
    # -----------------------------------------------------
    else:

        print("\nNegative Instance")

        # Remove S hypotheses that cover negative instance
        new_S = []

        for s in S:

            if not covers(s, instance):
                new_S.append(s)

        S = new_S

        # Specialize G
        new_G = []

        for g in G:

            # If G covers the negative example,
            # specialize it
            if covers(g, instance):

                specializations = minimal_specializations(
                    g, instance, domains, S
                )

                new_G.extend(specializations)

            else:
                new_G.append(g)

        G = remove_duplicates(new_G)

        # Remove G hypotheses that are not more general
        # than any member of S
        G = remove_less_general_hypotheses(G, S)

    # -----------------------------------------------------
    # Display boundaries after current instance
    # -----------------------------------------------------

    print("\nS Boundary (Most Specific):")

    if len(S) == 0:
        print("S = {}")
    else:
        for s in S:
            print(" ", display_hypothesis(s))

    print("\nG Boundary (Most General):")

    if len(G) == 0:
        print("G = {}")
    else:
        for g in G:
            print(" ", display_hypothesis(g))


# ---------------------------------------------------------
# Final Version Space
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("                 FINAL VERSION SPACE")
print("=" * 70)

print("\nFinal S Boundary:")

for s in S:
    print(display_hypothesis(s))

print("\nFinal G Boundary:")

for g in G:
    print(display_hypothesis(g))

print("\n" + "=" * 70)
print("Candidate Elimination Algorithm Completed")
print("=" * 70)