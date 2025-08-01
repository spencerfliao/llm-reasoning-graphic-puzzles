# COLX 523 - Advanced Corpus Linguistics

# Milestone 3                   

## Annotation + explanation + code

The original ARC dataset is stored in JSON format and designed to be compatible with various machine-learning tools. It is divided into three folders: training, evaluation and test. Each contains multiple JSON files representing distinct reasoning problems, including inputs and outputs designed to test abstract reasoning abilities. To make the annotation task more accessible, we converted the JSON files to PNG images. The code for that is present in the `src/utils.py` file. The images, on the other hand, are located in the `data/images` directory. To prevent any data leakage problems, we only converted the training and evaluation  JSON files to images since these are the only files we will be annotating. This aligns with our overall goal: to fine-tune an LLM to automatically generate the annotations for the test set and then use them to solve the ARC reasoning tasks. 
Out of the 800 examples (400 training and 400 evaluation), we took 200 and annotated 50. Each annotation consisted of four components: reflections, pixel/object changes, helper functions, and program instructions.
1. Reflections: This part outlines the underlying logic or pattern of the problem, providing a high-level understanding of the solution. It describes how a human might generally approach solving the problem based on the observations made from the inputs and outputs.
2. Pixel/Object Changes: Here, we detail the specific alterations made to the objects or pixels within the grid. This includes identifying relevant objects or groups of pixels and describing the changes they undergo, such as movements, colour changes, expansions, or contractions, to achieve the desired output.
3. Helper Functions: We list the predefined helper functions used in the solution. These functions perform object detection, colour replacement, grid manipulation, object merging, and so on. These functions serve as building blocks for constructing the step-by-step solution for the reasoning task.
4. Program Instructions: This section provides a sequential guide for executing the solution using the previously mentioned helper functions. It is a detailed algorithm that, when followed, would lead from the input grid to the output grid.

We decided to store the annotations as TSV files. They are located in the `data/annotations` directory.
These annotations will fine-tune an LLM using Chain of Thought Prompting and Thought Cloning. The goal is that for the test set, it can generate its annotations and use them to solve each reasoning task. 

## Interannotator agreement study

Interannotator agreement data files are located at `/data/interannotator_agreement`.

### Interannotator agreement measure
We calculate our interannotator agreement by manually inspecting each data point and giving a correct/incorrect label to each annotation. For each annotation we assign two other annotators for doing the inspection. The interannotator agreement score is calculated by the percentage of correct labels.

This form of agreement is chosen because the nature of our annotation are natural language sentences. We cannot use n-gram or language model based similarities because the focus of our data is in logical deduction, not statistical similarities or semantic similarities. There are no existing model that can evaluate the logical similarity of two annotations realiably. Therefore we choose to annotate a binary agreement score to each annotation, and use the average as the overall score. Moreover the annotators are already well trained and familiar with the dataset, so we can confidently trust the scores given by the annotators.

### Interannotator score
Using the script at `/src/inter_annotator_agreement.py`, we obtained a score of 0.85 out of 1. Which means the annotators agree 85% of our data is accurate.

### Annotation realiability
85% is fairly reasonable as our data annotation involves mentally demanding logical deductions in writing appropriate psuedocode using predefined functions. Some details in the thought process might be missed, or the usage of predefined functions might introduce bugs.


## Experimenting with annotation options (Optional)

We experimented different forms of annotation during milestone2. Originally our annotation contain the fields `Filename`, `Reflections`, `Pixel Changes`, `Object Changes`, `Helper Functions`, `Overall Pattern` and `Program Instructions`. However during our initial annotations, as seen at `/data/annotations/archived`,  we discovered some of the fields are redundant or unclear in purpose. For example, `Reflections` and `Overall Pattern` are quite similar. They differ in detailness but the difference is not important in downstream tasks. Therefore we choosed to merge them together. We also merged `Pixel Changes` and `Objects Changes` to `Pixel/Object Changes` because most tasks is best described by either one of them. 

## Plan for the interface

1. **Search by Description of Reflection:**
   - **Note:** Users will be able to search the corpus by entering keywords or phrases related to the ARC tasks.
2. **Search by Helper Function:**
   - **Note:** Another feature will be accessing detailed annotations for ARC tasks by helper functions. This allows users to find tasks that are of similar patterns and solutions, which aids in understanding the reasoning behind each task's solution and to see examples of how to programmatically approach problem-solving.

### Implementation

   - **User Interface:** A simple text box will enable users to enter their search terms, with a toggle indicating whether the user wants to search by either options. Results that include the original task image and annotations would be displayed in the order of relevance. (Optional filters, e.g., difficulty level, if we deem it necessary and have the time to develop, could refine searches, enhancing discoverability of relevant tasks.)

### Justification of Choices

Our choice to focus on reflection and helper functions for the annotated search functionality comes from the desire to showcase the depth of human understanding and computational strategies required to solve ARC tasks. "Reflections" give a quick, abstract insight into the problem-solving required, appealing to users interested in the cognitive aspects of the dataset. In contrast, helper functions cater to those more interested in the programming challenge, providing a bridge between abstract reasoning and practical coding exercises.
