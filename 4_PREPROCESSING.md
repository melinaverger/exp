

For the first experiment, we use the data table `'studentInfo.csv'` only, meaning that we analyse the results according to students' information and not courses information.

We work on a copy of the data table which contains all columns except 'code_module', 'code_presentation' and 'id_student', and where we keep the first instance of students' information duplicates (<span style="color: grey;">potential induced bias</span>).

## Protected attributes

We try to replicate the experiment of (Lee & Kizilcec, 2020) that focused on two binary protected attributes, the racial-ethnicity and gender of students. In our case, we have a gender attribute that is ready, as it is already binary like in the mentioned experiment. However, instead of having racial information on students, we will focus on their IMD and make 2 groups: students who have an IMD between 0 and 50% and the others. We encode the 2 features directly during this step (see following table).

An additional <span style="color: grey;">induced bias</span> is coming from how we will deal with the missing IMD values. We do not know why these values are missing (no associated IMD, not being collected, ..?). Thus, we make the decision to remove the 971 concerned students instead of replacing the missing IMDs by more meaningful values that we do not know.

## Target variable

The target variable is represented by the 'final_result' column ('Pass', 'Withdrawn', 'Fail', 'Distinction').

'Withdrawn' means that the result was removed afterwards and it is unclear what 'Distinction' means. Eventually, we remove the rows associated to a 'Withdrawn' or a 'Distinction' result (potential induced bias). It corresponds to 11,308 rows.

## Encoding attributes

'num_of_prev_attempts' and 'studied_credits' are both numerical variables (discrete). All the others are categorical variables, including 'gender' and 'imd_band' that were already encoded in a previous step. We thus convert the categorical variables that left into numerical variables.

As we will use a tree-based model afterwards, we do not need to scale the numerical variables and we can use ordinal encoding (even with an arbitrary order) instead of one-hot-encoding when it was needed for linear modeling. 'disability' and 'final_result' are turned into simple 0-or-1 variables, such as 'gender' and 'imd_band' protected attributes.

The encodings were explicitly made to retrieve the results of different groups after the predictions.

| Name              | Class (categorical) | Encoding (details in the code) |
|-------------------|---------------------|--------------------------------|
| gender*           | binary (could be nominal in general) | binary label {0, 1}|
| region            | nominal | ordinal encoding {0, 1, ..., 12}|
| highest_education | ordinal | ordinal encoding {0, 1, 2, 3, 4}|
| imd_band*         | ordinal | binary label {0, 1} (ordinal encoding if not protected)|
| age_band          | ordinal | ordinal encoding {0, 1, 2}|
| disability        | binary (could be nominal in general) | binary label {0, 1}|
| final_result      | binary (initially nominal) | binary label {0, 1}|

Attributes marked with a * are protected. They were encoded but not used in the prediction model.

## Train-test split

In the experiment of (Lee & Kizilcec, 2020), they put aside data from the most recent semester as a test set. This split is relevent with the application of their prediction model. In our case, we do not have such a "natural" split (it would be possible when taking account the courses information). Therefore, we apply the standard 70-30% train-test split randomly to avoid introducing additional bias.

Finally, we have 11,554 training instances, 4,952 test instances and 8 attributes. The training set is skewed toward the positive label (success), comprising 62.43% of the instances.

(Lee & Kizilcec, 2020) did not mention any additional preprocessing operations.
