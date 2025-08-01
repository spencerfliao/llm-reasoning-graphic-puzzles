import pandas as pd


FUNCTION_NAMES = [
    "get_objects",
    "get_pixel_coords",
    "empty_grid",
    "crop_grid",
    "tight_fit",
    "combine_object",
    "rotate_clockwise",
    "horizontal_flip",
    "vertical_flip",
    "replace",
    "get_object_color",
    "change_object_color",
    "fill_object",
    "fill_row",
    "fill_col",
    "fill_between_coords",
    "fill_rect",
    "fill_value",
    "enclose_pixel",
    "enlarge_grid",
    "enlarge_object",
]


class KeywordSearch:
    def __init__(self, file_path):
        data = pd.read_csv(file_path, index_col=0)
        self.program_inst = data["Program Instructions"]
        self.helper_functions = data["Helper Functions"]
        self.file_name = data["Filename"]
        self.combined_texts = self.helper_functions + " " + self.program_inst
        self.function_names = FUNCTION_NAMES

    def search(self, keywords, relationship="OR", num_results="all"):
        if not isinstance(keywords, list):
            keywords = [keywords]
        if any(keyword not in self.function_names for keyword in keywords):
            return []
        results = []
        for i, combined_text in enumerate(self.combined_texts):
            if relationship == "AND":
                if all(keyword in combined_text for keyword in keywords):
                    results.append(self.file_name[i])
            elif relationship == "OR":
                if any(keyword in combined_text for keyword in keywords):
                    results.append(self.file_name[i])
            else:
                raise ValueError("Invalid relationship")
        unique_results = list(set(results))
        if num_results == "all":
            return unique_results
        return unique_results[: int(num_results)]


# How to use the keyword search
# file_path = "<Path to the combined_data.tsv file>"
# keyword_search = KeywordSearch(file_path)
# keyword = ["Function Name 1", "Function Name 2"]
# results = keyword_search.search(keyword, relationship="AND", num_results="all")
# This will return the n number of filenames that contain the given keywords.
