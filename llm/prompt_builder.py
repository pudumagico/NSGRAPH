from typing import Iterator, Tuple
import json
import os


class PromptBuilder:
    __FILE_NAME = "graph_related_question_dataset_answers"
    __prompt_setup = "You are now a Question Parser that translates natural language questions into ASP ground truths about different stations.\n\
Output only the ground truths and nothing else.\n\
The stations to be selected from are arbitrary.\n\
I now provide you with some examples on how to parse Questions:\n\n"

    __question_data = [
        {
            "solution": "end(3).countNodesBetween(2).shortestPath(1).station(0,{}).station(0,{}).",
            "examples": [
                {
                    "question": "How many stations are between Inzersdorf and Mainstation?",
                    "parameters": ["Inzersdorf", "Mainstation"]
                },
                {
                    "question": "What is the amount of stations between Station A and Station B?",
                    "parameters": ["Station A", "Station B"]
                },
                {
                    "question": "How many stations does it take to go from Johnsen to St. Galeen?",
                    "parameters": ["Johnsen", "St. Galeen"]
                }
            ],
            "validation": [
                "How many stations are between Lamabad and Geizhoven?",
                "How many stations does it take to go from Weizhofen to Greekenland?",
                "How many stations do I need to travel when going from Grünberg to St. Galeen?"
            ]
        },
        {
            "solution": "end(2).withinHops(1, 2).station(0,{}).",
            "examples": [
                {
                    "question": "How many other stations are two stops or closer to Kriau?",
                    "parameters": ["Kriau"]
                },
                {
                    "question": "How many stations are within at most three stops to Währingen?",
                    "parameters": ["Währingen"]
                },
                {
                    "question": "How many stations can I reach within four stops from Johannesburg?",
                    "parameters": ["Johannesburg"]
                }
            ],
            "validation": [
                "How many other stations are two stops or closer to Fossilio?",
                "What is the number of stations that are within three stops to Birming?",
                "How many stations can I reach from Jugenda in a maximum of two stops?"
            ]
        },
        {
            "solution": "end(2).paths(1).station(0,{}).station(0,{}).",
            "examples": [
                {
                    "question": "How many distinct routes are there between Wien and Linz?",
                    "parameters": ["Wien", "Linz"]
                },
                {
                    "question": "How many different routes can I take from Wurzbach to Saarlein?",
                    "parameters": ["Wurzbach", "Saarlein"]
                },
                {
                    "question": "What is the number of distinct ways I can reach Fortright from Sortfeit?",
                    "parameters": ["Fortright", "Sortfeit"]
                }
            ],
            "validation": [
                "How many distinct routes are there between Norwef and Ingruid?",
                "What is the amount of different routes between Gerasdorf and Deutsch-Wagram?",
                "What is the amount of route options that I have, going from Vatik zu Gratik?"
            ]
        },
        {
            "solution": "end(2).cycle(1).station(0,{}).",
            "examples": [
                {
                    "question": "Is Klingon part of a cycle?",
                    "parameters": ["Klingon"]
                },
                {
                    "question": "Is Sortfeit part of a loop?",
                    "parameters": ["Sortfeit"]
                },
                {
                    "question": "Can I reach Genf from itself?",
                    "parameters": ["Genf"]
                }
            ],
            "validation": [
                "Is Saschosen part of a cycle?",
                "Is there a cycle that Fortright is part of?",
                "Can I reach Fortline from itself with any line?"
            ]
        },
        {
            "solution": "end(2).adjacent(1).station(0,{}).station(0,{}).",
            "examples": [
                {
                    "question": "Are Solomon and Kyrgistan adjacent?",
                    "parameters": ["Solomon", "Kyrgistan"]
                },
                {
                    "question": "Are Bahrain and India next to each other?",
                    "parameters": ["Bahrein", "India"]
                },
                {
                    "question": "Is Belemeth next to Sigualen?",
                    "parameters": ["Belemeth", "Sigualen"]
                }
            ],
            "validation": [
                "Are Pedingero and Falige adjacent?",
                "Is Veranda adjacent to Peura?",
                "Are Pillipo and Stilkosi next to each other?"
            ]
        },
        {
            "solution": "end(2).adjacentTo(1).station(0,{}).station(0,{}).",
            "examples": [
                {
                    "question": "Which station is adjacent to Westbahnhof and Station T",
                    "parameters": ["Westbahnhof", "Station T"]
                },
                {
                    "question": "Which station is directly next to Hausberg and Fortright",
                    "parameters": ["Hausberg", "Fortright"]
                },
                {
                    "question": "Which station is adjacent to Greenville and St. Georgen",
                    "parameters": ["Greenville", "St. Georgen"]
                }
            ],
            "validation": [
                "Which station is adjacent to Hauptbain and Origos",
                "What is the name of the station that is adjacent to Firaun and Firas?",
                "Which station is next to Folikon and Bertikon?"
            ]
        },
        {
            "solution": "end(2).commonStation(1).station(0,{}).station(0,{}).",
            "examples": [
                {
                    "question": "Are the green line and line 5 connected by the same station?",
                    "parameters": ["line green", "line 5"]
                },
                {
                    "question": "Is there a common station between line 8 and the yellow line?",
                    "parameters": ["line 8", "line yellow"]
                },
                {
                    "question": "Are the following lines connected: line 8, line 2?",
                    "parameters": ["line 8", "line 2"]
                }
            ],
            "validation": [
                "Are line 6 and line 5 connected by the same station?",
                "Are the following two lines connected ba a station: Line 9, Line red",
                "Is there a station connecting line 5 and line 9?"
            ]
        },
        {
            "solution": "end(2).exist(1).station(0,{}).",
            "examples": [
                {
                    "question": "Is there a station called Wurzbach?",
                    "parameters": ["Wurzbach"]
                },
                {
                    "question": "Does the station named Gerasdorf exist?",
                    "parameters": ["Gerasdorf"]
                },
                {
                    "question": "Is the station St. Gallen real?",
                    "parameters": ["St. Gallen"]
                }
            ],
            "validation": [
                "Is there a station called Marge?",
                "Does the Station named Zimbabwe exist?",
                "Is the Station Grünberg really existent?"
            ]
        },
        {
            "solution": "end(2).linesOnNames(1).station(0,{}).",
            "examples": [
                {
                    "question": "Which lines is Vorgartenstraße on?",
                    "parameters": ["Vorgartenstraße"]
                },
                {
                    "question": "Which lines are connected to Gro. Lorelai?",
                    "parameters": ["Gro. Lorelai"]
                },
                {
                    "question": "Tell me the lines on which Bern is on?",
                    "parameters": ["Bern"]
                }
            ],
            "validation": [
                "Which lines is Sonita on?",
                "What are the lines that Beru is connected to?",
                "Tell me the lines that are connected to Dietikon?"
            ]
        },
        {
            "solution": "end(2).linesOnCount(1).station(0,{}).",
            "examples": [
                {
                    "question": "How many lines is Station Z on?",
                    "parameters": ["Station Z"]
                },
                {
                    "question": "How many lines is Hauptbahnhof connected to?",
                    "parameters": ["Hauptbahnhof"]
                },
                {
                    "question": "What is the number of lines that are connected to Kleinbühl?",
                    "parameters": ["Kleinbühl"]
                }
            ],
            "validation": [
                "How many lines is Kalbus on?",
                "How many lines are connected to Souga?",
                "What is the number of lines that are connected to Dietikon?"
            ]
        },
        {
            "solution": "end(2).sameLine(1).station(0,{}).station(0,{}).",
            "examples": [
                {
                    "question": "Are Station A and Station B on the same line?",
                    "parameters": ["Station A", "Station B"]
                },
                {
                    "question": "Do Hauptbahnhof and St. Margarethen share the same line?",
                    "parameters": ["Hauptbahnhof", "St. Margarethen"]
                },
                {
                    "question": "Can I reach Basel from Zürich without changing the line?",
                    "parameters": ["Basel", "Zürich"]
                }
            ],
            "validation": [
                "Are Benedigten and Sashiko on the same line?",
                "Are the following two stations on the same line: Fasano, Sonafa",
                "Can I reach Adamsberg from Briau without a linechange?"
            ]
        },
        {
            "solution": "end(2).stations(1).line(0,{}).",
            "examples": [
                {
                    "question": "Which stations does Line 5 pass through?",
                    "parameters": ["line 5"]
                },
                {
                    "question": "Which stations does the green line pass through?",
                    "parameters": ["line green"]
                },
                {
                    "question": "Which stations are connected to the red line?",
                    "parameters": ["line red"]
                }
            ],
            "validation": [
                "Which stations does Line 9 pass through?",
                "What are the stations that Line 4 passes through?",
                "What are the stations that lie on line 7?"
            ]
        }
    ]

    def survey_prompts(self, example_amount: int, skip_amount: int = 0) -> Iterator[Tuple[str, int, str, int]]:
        fileindex = 0
        while os.path.exists(self.__FILE_NAME + str(fileindex+1) + ".json"): fileindex += 1
        if not fileindex: raise FileNotFoundError("Run survey_extractor first")

        with open(self.__FILE_NAME + str(fileindex) + ".json") as qf:
            for prompt_index, question_class in enumerate(json.load(qf)):
                if prompt_index < skip_amount: continue
                for question in question_class["questions"]:
                    yield self.__build_preprompt(example_amount) + question, prompt_index, question_class["solution"], 0

    def generated_prompts(self, example_amount: int, skip_amount: int = 0) -> Iterator[Tuple[str, int, str, int]]:
        for prompt_index, q in enumerate(self.__question_data):
            if prompt_index < skip_amount: continue
            for difficulty, validation in enumerate(q["validation"]):
                yield self.__build_preprompt(example_amount) + validation, prompt_index, q['solution'], difficulty

    def __build_preprompt(self, example_amount):
        if not 0 < example_amount <= 3:
            raise ValueError("example_amount needs to be between 1 and 3 (inclusive)")
        prompt = self.__prompt_setup
        for question in self.__question_data:
            for i in range(example_amount):
                prompt += f"Q: \"{question['examples'][i]['question']}\"\n"
                answer = f"A: {question['solution']}\n\n"
                for parameter in question["examples"][i]["parameters"]:
                    answer = answer.replace("{}", f"\"{parameter}\"", 1)
                prompt += answer
        prompt += "Now provide the output for the following question:\n"
        return prompt
