import pandas as pd
import os

file_path = os.path.join(os.path.dirname(__file__), "workload_data.csv")
data = pd.read_csv(file_path)
print("Training Dataset:\n")
print(data)

# Initialize the hypothesis
hypothesis = None

print("\nProcessing Training Examples...\n")

# Iterate through each training example
for index, row in data.iterrows():

    # Consider only positive examples
    if row["High-Performance Edge"] == "Yes":
        attributes = list(row[:-1])

        # First positive example initializes the hypothesis
        if hypothesis is None:
            hypothesis = attributes.copy()
        else:
            # Generalize the hypothesis
            for i in range(len(hypothesis)):
                if hypothesis[i] != attributes[i]:
                    hypothesis[i] = "?"

    # Print hypothesis after every row
    print(f"After Workload W{index + 1}:")
    if hypothesis is None:
        print(["∅"] * (len(data.columns) - 1))
    else:
        print(hypothesis)
    print()

# Final hypothesis
print("Final Specific Hypothesis:")
print(hypothesis)