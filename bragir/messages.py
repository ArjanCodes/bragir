from bragir.languages import Languages, to_output

PROMPT_HELP = {
    "file": "Path to file",
    "api_key": "Enter valid openai api key",
    "directory": "Enter one directory that contains the files that is going to be translated",
    "language": f"Enter one or more languages {to_output(Languages)}",
}


ACTIONS = {
    "translating": "Translating to following language/languages: {lanugages}",
}
